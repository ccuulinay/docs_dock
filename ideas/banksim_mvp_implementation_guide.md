# BankSim MVP 实施指南：世界模型构建与引擎搭建
## ——基于已有数据的最小可行方案（LightGBM基线 + LLM Agent）

---

## 1. 数据盘点与MVP可用性分析

你已有的三类数据，在MVP阶段可以这样使用：

| 数据资产 | MVP用途 | 关键加工 | 优先级 |
|---------|--------|---------|--------|
| **客户特征数据** | 世界模型特征输入 | 标准化、分箱、One-Hot | P0 |
| **Take-up数据及时间** | 监督学习标签 | 构建响应标签+时间标签 | P0 |
| **历史营销活动数据** | 策略特征(Treatment) | 活动编码、优惠力度量化 | P0 |

### 1.1 数据加工流水线（MVP版）

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class MVPDataPipeline:
    """MVP数据加工：将原始数据转化为模型可消费的特征矩阵"""

    def process_customer_features(self, df_customer):
        """
        输入: 客户特征表
        输出: 客户特征矩阵 X_customer [n_customers, n_features]
        """
        # 数值特征：标准化
        numeric_cols = ['age', 'aum', 'income', 'tenure_months', 'transaction_freq']
        scaler = StandardScaler()
        df_customer[numeric_cols] = scaler.fit_transform(df_customer[numeric_cols])

        # 类别特征：Label编码（MVP用Label，生产用Target编码）
        cat_cols = ['gender', 'region', 'occupation', 'risk_preference', 'customer_tier']
        for col in cat_cols:
            df_customer[col] = LabelEncoder().fit_transform(df_customer[col].astype(str))

        # 关键：构建金融人格标签（基于规则，无监督）
        df_customer['financial_persona'] = self._derive_persona(df_customer)

        return df_customer

    def _derive_persona(self, df):
        """基于规则推导金融人格（MVP快速方案）"""
        conditions = [
            (df['risk_preference'] == 'conservative') & (df['aum'] > df['aum'].median()),
            (df['risk_preference'] == 'balanced'),
            (df['risk_preference'] == 'aggressive'),
            (df['digital_score'] > 0.7),
            (df['transaction_freq'] < df['transaction_freq'].quantile(0.2)),
        ]
        choices = ['稳健保值型', '平衡配置型', '进取投资型', '便利优先型', '价格敏感型']
        return np.select(conditions, choices, default='关系驱动型')

    def process_campaign_history(self, df_campaign):
        """
        输入: 历史活动表
        输出: 策略特征矩阵 T_campaign [n_campaigns, n_treatment_features]
        """
        # 优惠力度量化
        df_campaign['offer_value'] = self._quantify_offer(
            df_campaign['offer_type'], df_campaign['offer_detail']
        )

        # 渠道编码（One-Hot）
        channel_dummies = pd.get_dummies(df_campaign['channel'], prefix='ch')

        # 文案特征：MVP用简单关键词匹配，后续用Embedding
        df_campaign['copy_urgency'] = df_campaign['copy'].str.contains('限时|截止|仅剩').astype(int)
        df_campaign['copy_safety'] = df_campaign['copy'].str.contains('稳健|安全|保本').astype(int)
        df_campaign['copy_yield'] = df_campaign['copy'].str.contains('高收益|利率|回报').astype(int)

        # 客群策略编码
        df_campaign['target_aum_min'] = df_campaign['targeting_rule'].str.extract('AUM>=([0-9]+)').astype(float)
        df_campaign['target_tier'] = df_campaign['targeting_rule'].str.extract('tier:([A-Z]+)')

        return pd.concat([df_campaign, channel_dummies], axis=1)

    def _quantify_offer(self, offer_type, offer_detail):
        """将优惠转化为可比较的数值"""
        # 利率上浮: bp
        # 积分: 积分价值/1000
        # 费率折扣: 折扣比例
        # 礼品: 礼品价值
        pass

    def build_training_matrix(self, df_customer, df_campaign, df_takeup):
        """
        构建训练矩阵: 每个客户-活动对为一个样本
        正样本: 客户参与了活动并响应
        负样本: 客户被触达但未响应
        """
        # 合并客户特征和活动特征
        df = df_takeup.merge(df_customer, on='customer_id')
        df = df.merge(df_campaign, on='campaign_id')

        # 特征列
        feature_cols = (
            [c for c in df_customer.columns if c != 'customer_id'] +
            [c for c in df_campaign.columns if c not in ['campaign_id', 'copy', 'targeting_rule']]
        )

        X = df[feature_cols]
        y_response = df['responded']  # 0/1 是否响应
        y_value = df['response_value']  # 响应金额（仅响应者有值）
        y_time = df['response_time_days']  # 响应时间

        return X, y_response, y_value, y_time, feature_cols
```

---

## 2. MVP世界模型：LightGBM Quantile Baseline

MVP阶段不追求因果Transformer的复杂度，先用**LightGBM分位数回归**快速建立可解释的基线预测能力。这是Oransim开源版本也采用的MVP策略。

### 2.1 模型架构（MVP三头预测）

```python
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import joblib

class MVPWorldModel:
    """
    MVP世界模型：三头LightGBM预测
    - 响应概率头 (Response Head): 二分类
    - 响应金额头 (Value Head): 回归（仅对响应者）
    - 响应时间头 (Time Head): 回归
    """

    def __init__(self):
        self.response_model = None
        self.value_model = None
        self.time_model = None
        self.feature_cols = None
        self.quantiles = [0.35, 0.50, 0.65]  # P35/P50/P65置信区间

    def train(self, X, y_response, y_value, y_time):
        """训练三个预测头"""
        X_train, X_val, y_resp_train, y_resp_val = train_test_split(
            X, y_response, test_size=0.2, random_state=42
        )

        # === Head 1: 响应概率 ===
        print('Training Response Head...')
        self.response_model = lgb.LGBMClassifier(
            objective='binary',
            n_estimators=500,
            learning_rate=0.05,
            num_leaves=31,
            feature_fraction=0.8,
            bagging_fraction=0.8,
            bagging_freq=5,
            verbose=-1
        )
        self.response_model.fit(
            X_train, y_resp_train,
            eval_set=[(X_val, y_resp_val)],
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
        )

        # === Head 2: 响应金额（仅训练响应者）===
        print('Training Value Head...')
        responded_mask = y_response == 1
        X_responded = X[responded_mask]
        y_value_responded = y_value[responded_mask]

        self.value_models = {}  # 每个分位数一个模型
        for q in self.quantiles:
            model = lgb.LGBMRegressor(
                objective='quantile', alpha=q,
                n_estimators=300,
                learning_rate=0.05,
                num_leaves=31,
                verbose=-1
            )
            model.fit(X_responded, y_value_responded)
            self.value_models[q] = model

        # === Head 3: 响应时间 ===
        print('Training Time Head...')
        # 仅对响应者训练，未响应者设为极大值或单独处理
        y_time_filled = y_time.copy()
        y_time_filled[y_response == 0] = 999  # 未响应标记

        self.time_model = lgb.LGBMRegressor(
            objective='regression',
            n_estimators=300,
            learning_rate=0.05,
            verbose=-1
        )
        self.time_model.fit(X, y_time_filled)

        self.feature_cols = list(X.columns)
        print('Training complete!')

    def predict(self, X_new):
        """
        预测新活动方案下的响应指标
        返回: 每个客户的预测结果
        """
        # 响应概率
        response_prob = self.response_model.predict_proba(X_new)[:, 1]

        # 响应金额分位数
        value_preds = {}
        for q, model in self.value_models.items():
            value_preds[q] = model.predict(X_new)

        # 响应时间
        time_pred = self.time_model.predict(X_new)

        return {
            'response_prob': response_prob,
            'value_p35': value_preds[0.35],
            'value_p50': value_preds[0.50],
            'value_p65': value_preds[0.65],
            'expected_time': time_pred,
            'expected_value': value_preds[0.50] * response_prob  # 期望金额
        }

    def explain_prediction(self, X_single, top_n=5):
        """
        解释单个客户的预测（SHAP风格特征重要性）
        MVP用LightGBM内置的feature_importances
        """
        importances = self.response_model.feature_importances_
        feature_importance = pd.Series(
            importances, index=self.feature_cols
        ).sort_values(ascending=False).head(top_n)
        return feature_importance

    def save(self, path='world_model_mvp.pkl'):
        joblib.dump(self, path)

    @classmethod
    def load(cls, path='world_model_mvp.pkl'):
        return joblib.load(path)
```

### 2.2 训练数据构造（关键！）

```python
def build_mvp_training_data(raw_data, lookback_months=12):
    """
    核心逻辑：将历史活动数据构造为监督学习样本

    对于每个历史活动：
    - 正样本：被触达且响应的客户 (y=1)
    - 负样本：被触达但未响应的客户 (y=0)
    - 注意：未被触达的客户不能作为负样本（选择偏差！）
    """
    samples = []

    for campaign in raw_data.campaigns:
        # 获取该活动的触达客户列表
        touched_customers = campaign.touched_customer_ids
        responded_customers = campaign.responded_customer_ids

        for cid in touched_customers:
            customer = raw_data.get_customer(cid)

            # 构建特征向量：客户特征 + 活动策略特征
            features = {
                # 客户特征
                'age': customer.age,
                'aum': customer.aum,
                'income': customer.income,
                'risk_preference': customer.risk_preference,
                'digital_score': customer.digital_score,
                'tenure_months': customer.tenure_months,
                'product_count': customer.product_count,
                'last_transaction_days': customer.last_transaction_days,
                'financial_persona': customer.persona,

                # 活动策略特征（Treatment）
                'offer_value': campaign.offer_value,
                'offer_type': campaign.offer_type,
                'channel_sms': int('sms' in campaign.channels),
                'channel_app': int('app_push' in campaign.channels),
                'channel_call': int('outbound_call' in campaign.channels),
                'channel_visit': int('rm_visit' in campaign.channels),
                'copy_urgency': campaign.copy_urgency_score,
                'copy_safety': campaign.copy_safety_score,
                'target_aum_min': campaign.target_aum_min,
                'campaign_month': campaign.launch_month,
                'campaign_day_of_week': campaign.launch_dow,

                # 历史交互特征（关键！）
                'past_response_rate': customer.past_response_rate,
                'days_since_last_campaign': customer.days_since_last_campaign,
                'fatigue_score': customer.fatigue_score,
                'brand_affinity': customer.brand_affinity,
            }

            # 标签
            responded = 1 if cid in responded_customers else 0
            response_value = campaign.get_response_value(cid) if responded else 0
            response_time = campaign.get_response_time(cid) if responded else None

            samples.append({
                **features,
                'responded': responded,
                'response_value': response_value,
                'response_time': response_time,
                'customer_id': cid,
                'campaign_id': campaign.id,
            })

    return pd.DataFrame(samples)
```

### 2.3 关键特征工程（MVP必做）

| 特征类别 | 具体特征 | 为什么重要 |
|---------|---------|-----------|
| **客户基础** | age, aum, income, tenure | 基础区分度 |
| **风险画像** | risk_preference, product_count | 产品匹配度 |
| **行为活跃** | digital_score, last_transaction_days | 活跃度预测响应 |
| **历史响应** | past_response_rate | 最强预测因子之一 |
| **营销疲劳** | days_since_last_campaign, fatigue_score | 避免过度营销 |
| **优惠力度** | offer_value, offer_type | 激励效果 |
| **渠道组合** | channel_sms/app/call/visit | 渠道偏好 |
| **文案情感** | copy_urgency, copy_safety | 内容匹配 |
| **时机** | campaign_month, day_of_week | 季节性 |
| **品牌关系** | brand_affinity | 长期关系价值 |

---

## 3. MVP LLM Agent：客户决策模拟

MVP阶段不模拟全量客户（成本太高），采用**两阶段策略**：统计模型筛选关键客户 -> LLM深度模拟。

### 3.1 人格卡片生成（Prompt Engineering核心）

```python
import openai
from typing import List, Dict

class MVPCustomerAgent:
    """
    MVP客户智能体：基于GPT-5.4模拟客户对营销活动的反应
    只模拟高价值/高不确定性客户，控制成本
    """

    def __init__(self, api_key: str, model: str = 'gpt-5.4'):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.temperature = 0.3  # 低温度保证一致性

    def generate_persona_card(self, customer: Dict) -> str:
        """
        将结构化客户数据转化为自然语言人格描述
        这是Prompt Engineering的关键：让LLM"入戏"
        """

        # 根据金融人格调整语气
        persona_tones = {
            '稳健保值型': '你非常谨慎，优先考虑资金安全，对高收益承诺持怀疑态度。你信任大银行和长期口碑。',
            '平衡配置型': '你愿意在专业建议下尝试不同产品，重视资产配置的合理性。',
            '进取投资型': '你对市场热点敏感，愿意承担风险以换取更高回报。',
            '便利优先型': '你重视操作便利性，偏好手机App完成所有操作。',
            '价格敏感型': '你对费率、优惠非常敏感，会货比三家。',
            '关系驱动型': '你高度依赖客户经理的建议，人情关系影响你的决策。'
        }

        tone = persona_tones.get(customer['financial_persona'], '')

        card = f"""
你是一位{customer['age']}岁的{customer['gender']}客户，居住在{customer['region']}。
你的职业是{customer['occupation']}，家庭月收入约{customer['income']}元。
你在本行的总资产（AUM）约为{customer['aum']}元，已开户{customer['tenure_months']}个月。
你的投资风险偏好为：{customer['risk_preference']}。
目前持有本行{customer['product_count']}个产品。
你最近{customer['last_transaction_days']}天有过交易。

{tone}

重要：请始终保持这个人设，基于你的真实金融状况和性格做出决策。
不要扮演一个"理想客户"，要扮演一个真实的、有顾虑的、有偏好的普通人。
"""
        return card.strip()

    def evaluate_campaign(self, customer: Dict, campaign: Dict) -> Dict:
        """
        让LLM模拟客户对具体营销活动的反应
        返回结构化决策结果
        """

        persona = self.generate_persona_card(customer)

        prompt = f"""
{persona}

---

你现在收到了一条来自银行的营销信息：
- 渠道：{campaign['channel']}
- 产品：{campaign['product_name']}
- 文案："{campaign['copy']}"
- 优惠：{campaign['offer']}
- 期限：{campaign['duration']}

请基于你的人设，模拟你的真实反应。请按以下JSON格式输出：

```json
{{
  "attention": "你会注意到这条消息吗？为什么？",
  "emotion": "你的第一反应是什么？（积极/中性/消极）",
  "intent": "你会考虑采取行动吗？（强烈考虑/可能考虑/不太可能/完全不会）",
  "barriers": ["如果犹豫，你的顾虑是什么？列出1-3条"],
  "decision": "最终决策：respond / ignore / reject",
  "expected_amount": "如果响应，预计投入金额（元）",
  "reasoning": "用第一人称解释你的决策理由，50字以内"
}}
```
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一位银行客户模拟器。请严格基于提供的人设做出反应，不要给出通用建议。只输出JSON。"},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            response_format={"type": "json_object"}
        )

        import json
        result = json.loads(response.choices[0].message.content)

        # 标准化输出
        return {
            "will_respond": result["decision"] == "respond",
            "emotion": result["emotion"],
            "intent_level": result["intent"],
            "barriers": result.get("barriers", []),
            "expected_amount": float(result.get("expected_amount", 0)),
            "reasoning": result["reasoning"],
            "attention": result["attention"]
        }

    def batch_simulate(self, customers: List[Dict], campaign: Dict, 
                       sample_size: int = 100) -> List[Dict]:
        """
        批量模拟，但只采样关键客户

        采样策略：
        - 前30%高预测响应概率（验证模型）
        - 后30%低预测响应概率（发现盲区）
        - 中间40%随机采样（探索不确定性）
        """
        # 这里假设已有世界模型的预测分数
        # 实际实现中传入预测概率

        import random
        random.shuffle(customers)
        sampled = customers[:sample_size]

        results = []
        for customer in sampled:
            result = self.evaluate_campaign(customer, campaign)
            result['customer_id'] = customer['customer_id']
            results.append(result)

        return results
```

### 3.2 LLM Agent结果聚合与洞察提取

```python
class AgentInsightAggregator:
    """聚合LLM Agent模拟结果，提取业务洞察"""

    def aggregate(self, agent_results: List[Dict]) -> Dict:
        total = len(agent_results)
        responded = sum(1 for r in agent_results if r['will_respond'])

        # 情感分布
        emotions = [r['emotion'] for r in agent_results]
        emotion_dist = pd.Series(emotions).value_counts(normalize=True).to_dict()

        # 决策分布
        decisions = [r['decision'] for r in agent_results]
        decision_dist = pd.Series(decisions).value_counts(normalize=True).to_dict()

        # 顾虑聚类（用LLM或简单关键词）
        all_barriers = []
        for r in agent_results:
            all_barriers.extend(r.get('barriers', []))

        # MVP用简单关键词聚类，后续用Embedding聚类
        barrier_categories = self._categorize_barriers(all_barriers)

        # 典型客户反馈（采样展示）
        positive_examples = [r for r in agent_results 
                           if r['emotion'] == '积极'][:3]
        negative_examples = [r for r in agent_results 
                           if r['emotion'] == '消极'][:3]

        return {
            "simulated_response_rate": responded / total,
            "emotion_distribution": emotion_dist,
            "decision_distribution": decision_dist,
            "top_barriers": barrier_categories,
            "positive_examples": positive_examples,
            "negative_examples": negative_examples,
            "avg_expected_amount": np.mean([r['expected_amount'] for r in agent_results])
        }

    def _categorize_barriers(self, barriers: List[str]) -> Dict:
        """MVP：简单关键词匹配分类顾虑"""
        categories = {
            '收益担忧': ['收益', '利率', '回报', '不如'],
            '信任顾虑': ['信任', '靠谱', '风险', '安全'],
            '流程繁琐': ['麻烦', '复杂', '流程', '去网点'],
            '已有类似': ['已经有', '不需要', '类似'],
            '营销疲劳': ['太多', '骚扰', '频繁', '反感'],
            '资金约束': ['没钱', '资金', '周转', '紧张'],
        }

        counts = {k: 0 for k in categories}
        for barrier in barriers:
            for cat, keywords in categories.items():
                if any(kw in barrier for kw in keywords):
                    counts[cat] += 1
                    break

        # 排序返回
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
```

---

## 4. MVP因果推断：简化版反事实

MVP阶段不构建完整的SCM，用**倾向得分匹配（PSM）+ 简单对比**实现基础反事实能力。

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

class MVPCausalEngine:
    """
    MVP因果引擎：基于PSM的简化反事实
    回答："如果改变策略X，响应率会如何变化？"
    """

    def __init__(self, world_model: MVPWorldModel):
        self.world_model = world_model

    def compare_strategies(self, df, treatment_col, outcome_col='responded'):
        """
        对比两种策略的效果（如 SMS vs App Push）
        使用PSM控制选择偏差
        """
        # 1. 估计倾向得分
        confounders = [c for c in df.columns if c not in [treatment_col, outcome_col]]
        X = df[confounders]
        T = df[treatment_col]

        ps_model = LogisticRegression(max_iter=1000)
        ps_model.fit(X, T)
        df['propensity_score'] = ps_model.predict_proba(X)[:, 1]

        # 2. 匹配
        treated = df[df[treatment_col] == 1]
        control = df[df[treatment_col] == 0]

        nn = NearestNeighbors(n_neighbors=1)
        nn.fit(control['propensity_score'].values.reshape(-1, 1))
        distances, indices = nn.kneighbors(treated['propensity_score'].values.reshape(-1, 1))

        matched_control = control.iloc[indices.flatten()]

        # 3. 计算ATE
        treated_outcome = treated[outcome_col].mean()
        control_outcome = matched_control[outcome_col].mean()
        ate = treated_outcome - control_outcome

        return {
            'treated_response_rate': treated_outcome,
            'control_response_rate': control_outcome,
            'ate': ate,  # Average Treatment Effect
            'lift': ate / control_outcome if control_outcome > 0 else 0
        }

    def what_if_offer_increase(self, X_base, offer_increase_pct=0.1):
        """
        反事实：如果优惠力度增加10%，响应率如何变化？
        MVP简化版：直接在特征上修改并重新预测
        """
        X_modified = X_base.copy()
        X_modified['offer_value'] *= (1 + offer_increase_pct)

        pred_base = self.world_model.predict(X_base)
        pred_modified = self.world_model.predict(X_modified)

        base_rate = pred_base['response_prob'].mean()
        modified_rate = pred_modified['response_prob'].mean()

        return {
            'base_response_rate': base_rate,
            'modified_response_rate': modified_rate,
            'delta': modified_rate - base_rate,
            'relative_lift': (modified_rate - base_rate) / base_rate if base_rate > 0 else 0
        }
```

---

## 5. MVP ROI引擎

```python
class MVPROIEngine:
    """MVP ROI计算：简化但覆盖核心要素"""

    def __init__(self, config):
        # 银行内部参数，需业务确认
        self.config = {
            'aum_yield_rate': 0.015,      # AUM综合收益率 1.5%
            'aum_retention_years': 3,     # AUM平均留存3年
            'product_margin': 0.02,       # 产品利润率 2%
            'cross_sell_value': 5000,     # 交叉销售平均价值
            'new_customer_ltv': 20000,    # 新客户LTV
            'channel_costs': {           # 单次触达成本
                'sms': 0.05,
                'app_push': 0.02,
                'outbound_call': 5.0,
                'rm_visit': 50.0
            },
            'labor_hour_rate': 100,       # 客户经理时薪
        }
        self.config.update(config)

    def calculate(self, campaign_config, predictions):
        """
        campaign_config: 活动配置（客群大小、渠道、优惠等）
        predictions: 世界模型预测结果（响应率、金额等）
        """
        n_customers = campaign_config['target_size']
        response_rate = predictions['response_prob'].mean()
        n_responders = int(n_customers * response_rate)

        # 收入侧
        avg_response_value = predictions['value_p50'].mean()
        total_aum_increase = n_responders * avg_response_value

        aum_revenue = (total_aum_increase * 
                      self.config['aum_yield_rate'] * 
                      self.config['aum_retention_years'])

        product_revenue = n_responders * avg_response_value * self.config['product_margin']

        total_revenue = aum_revenue + product_revenue

        # 成本侧
        touch_cost = sum(
            campaign_config['channel_volumes'].get(ch, 0) * cost
            for ch, cost in self.config['channel_costs'].items()
        )

        offer_cost = n_responders * campaign_config.get('offer_cost_per_head', 0)
        labor_cost = campaign_config.get('labor_hours', 0) * self.config['labor_hour_rate']
        system_cost = campaign_config.get('system_cost', 5000)

        total_cost = touch_cost + offer_cost + labor_cost + system_cost

        # ROI
        roi = (total_revenue - total_cost) / total_cost if total_cost > 0 else 0

        # 边际分析：每增加一个触达客户的成本vs收益
        marginal_cost = total_cost / n_customers
        marginal_revenue = total_revenue / n_customers

        return {
            'n_target': n_customers,
            'n_predicted_responders': n_responders,
            'predicted_response_rate': response_rate,
            'total_aum_increase': total_aum_increase,
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'roi': roi,
            'marginal_cost': marginal_cost,
            'marginal_revenue': marginal_revenue,
            'break_even_rate': total_cost / (total_revenue / n_responders) if n_responders > 0 else float('inf'),
            'cost_breakdown': {
                'touch': touch_cost,
                'offer': offer_cost,
                'labor': labor_cost,
                'system': system_cost
            }
        }
```

---

## 6. MVP端到端流程

```python
class BankSimMVP:
    """MVP端到端流程：从活动设计到预测输出"""

    def __init__(self, api_key: str, model_path: str = None):
        self.data_pipeline = MVPDataPipeline()
        self.world_model = MVPWorldModel.load(model_path) if model_path else MVPWorldModel()
        self.causal_engine = MVPCausalEngine(self.world_model)
        self.roi_engine = MVPROIEngine(config={})
        self.agent = MVPCustomerAgent(api_key=api_key)
        self.aggregator = AgentInsightAggregator()

    def simulate_campaign(self, campaign_design, customer_pool):
        """
        主入口：输入活动设计，输出预测结果

        campaign_design = {
            'product_name': '大额存单',
            'offer': '利率上浮20bp',
            'offer_value': 20,  # bp
            'channels': ['sms', 'app_push'],
            'copy': '限时优惠！大额存单利率上浮20bp，稳健增值...',
            'target_size': 10000,
            'targeting_rule': 'AUM>=50万',
            'duration_days': 30
        }
        """

        # Step 1: 数据加工
        print("Step 1: 数据加工...")
        # 将campaign_design转化为特征矩阵
        # 将customer_pool与campaign_design合并

        # Step 2: 世界模型预测（统计层面）
        print("Step 2: 世界模型预测...")
        # X = self._build_features(customer_pool, campaign_design)
        # predictions = self.world_model.predict(X)

        # Step 3: LLM Agent模拟（定性层面）
        print("Step 3: LLM Agent模拟...")
        # sampled_customers = self._sample_customers(customer_pool, predictions)
        # agent_results = self.agent.batch_simulate(sampled_customers, campaign_design)
        # insights = self.aggregator.aggregate(agent_results)

        # Step 4: ROI计算
        print("Step 4: ROI计算...")
        # roi_result = self.roi_engine.calculate(campaign_design, predictions)

        # Step 5: 反事实对比（简化）
        print("Step 5: 反事实对比...")
        # what_if = self.causal_engine.what_if_offer_increase(X, offer_increase_pct=0.1)

        # Step 6: 输出报告
        return {
            'predicted_response_rate': 0.032,  # 示例
            'predicted_responders': 320,
            'predicted_aum_increase': 12000000,
            'roi': 1.85,
            'confidence_interval': [0.028, 0.036],
            'agent_insights': {},
            'what_if_analysis': {}
        }
```

---

## 7. MVP实施Checklist

### Week 1-2: 数据准备
- [ ] 梳理客户特征表字段，完成数据质量检查
- [ ] 构建客户-活动-响应的关联表（核心！）
- [ ] 计算历史响应率、疲劳度、品牌亲和度等衍生特征
- [ ] 完成特征标准化和编码

### Week 3-4: 世界模型训练
- [ ] 构建训练样本（客户-活动对）
- [ ] 训练LightGBM三头模型（响应/金额/时间）
- [ ] 验证集评估：AUC、MAPE、校准曲线
- [ ] 特征重要性分析，理解模型学到了什么

### Week 5-6: LLM Agent接入
- [ ] 设计人格卡片Prompt模板
- [ ] 测试不同金融人格的决策一致性
- [ ] 实现批量模拟和结果聚合
- [ ] 对比LLM模拟响应率 vs 统计模型预测率，校准偏差

### Week 7-8: 产品化封装
- [ ] 构建FastAPI服务
- [ ] 设计活动配置输入接口
- [ ] 设计预测报告输出格式
- [ ] 接入内部营销平台（可选）

---

## 8. 关键注意事项

### 8.1 数据陷阱
1. **选择偏差**：未被触达的客户不能作为负样本！只能用在触达客户中对比响应/未响应
2. **时间泄漏**：不能用活动之后的客户行为来预测该活动（特征必须在活动前）
3. **幸存者偏差**：历史活动可能只覆盖了特定客群，模型外推需谨慎

### 8.2 模型验证
- 用**时间切分**验证：用2024年Q1-Q3训练，Q4测试
- 用**活动切分**验证：留出一批活动完全不参与训练，作为最终测试
- 关注**校准度**：预测概率30%的客户群体，实际响应率是否接近30%

### 8.3 LLM Agent校准
- LLM可能系统性地高估响应率（因为Prompt要求"做出反应"）
- 建议：对比LLM模拟响应率 vs 统计模型响应率，建立校准系数
- 或者：在Prompt中明确加入"大部分人会忽略营销信息"的上下文

### 8.4 成本估算
- GPT-5.4 API：假设每次调用$0.01，模拟100个客户 = $1/次活动
- 如果每天模拟10次活动 = $10/天 = $300/月（可控）
- 统计模型：零额外成本

---

*MVP版本 v0.1*  
*目标：4-6周内建立可运行的预测基线*
