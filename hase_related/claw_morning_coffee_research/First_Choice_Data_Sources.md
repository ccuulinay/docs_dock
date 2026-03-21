# 可靠首选数据源清单 (First Choice Data Sources)

> **适用项目**: OpenClaw 智能调研报告系统  
> **筛选标准**: 权威性、稳定性、免费/低成本、API/RSS 可访问性  
> **整理日期**: 2026-03-21

---

## 1. Andrej Karpathy 推荐的高质量 RSS 源

Andrej Karpathy（前 Tesla AI 总监、OpenAI 创始成员）在 2026 年初公开推荐回归 RSS 订阅以获取高质量长文内容。他特别分享了一个**2025 年 Hacker News 上最受欢迎的 92 个博客**的订阅源列表，涵盖深度技术、编程、数学及科学研究 [^1^][^2^][^3^]。

### 核心推荐列表 (Hacker News 热门博客 Top 92)

**原始 OPML 文件下载地址**（可直接导入 RSS 阅读器）：
```
https://gist.github.com/emschwartz/e6d2bf860ccc367fe37ff953ba6de66b#file-hn-popular-blogs-2025-opml
```

**代表性高质量博客（部分）：**

| 作者/博客 | 领域 | RSS Feed URL | 特点 |
|----------|------|-------------|------|
| **Paul Graham** (Y Combinator 创始人) | 创业/技术哲学 | http://paulgraham.com/rss.html | 篇篇精华 |
| **Simon Willison** (Django 联合创始人) | AI 应用/代码实践 | https://simonwillison.net/atom/everything/ | 不写空论，只发代码实测 |
| **Julia Evans** | 底层技术/漫画解释 | https://jvns.ca/atom.xml | 用漫画解释 Linux 内核 |
| **Terence Tao (陶哲轩)** | 数学研究 | https://terrytao.wordpress.com/feed/ | 菲尔兹奖得主 |
| **John Gruber** (Daring Fireball) | 苹果生态/科技评论 | https://daringfireball.net/feeds/main | 长期关注苹果 |
| **Neal Agarwal** | 创意编程 | 通过 RSS 聚合 | 代表作《The Password Game》《Infinite Craft》 |

**推荐 RSS 阅读器工具：**
- **NetNewsWire** (macOS/iOS, 开源免费): https://github.com/Ranchero-Software/NetNewsWire
- **Folo** (跨平台, 开源): https://github.com/RSSNext/Folo
- **Reeder** (iOS/macOS, 付费但体验佳)

---

## 2. Google News RSS 与新闻聚合源

### Google News RSS Feed（官方，免费）

**基础搜索 RSS URL 结构** [^13^][^15^]：
```
https://news.google.com/rss/search?q={keywords}&hl={language}&ceid={region}
```

**常用参数组合示例：**

| 用途 | URL 示例 |
|------|----------|
| **英文通用搜索** | `https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&ceid=US:en` |
| **中文通用搜索** | `https://news.google.com/rss/search?q=人工智能&hl=zh-CN&ceid=CN:zh` |
| **科技主题** | `https://news.google.com/rss/search?q=technology&hl=en-US&ceid=US:en` |
| **特定公司** | `https://news.google.com/rss/search?q=Tesla+OR+OpenAI&hl=en-US&ceid=US:en` |
| **金融领域** | `https://news.google.com/rss/search?q=stock+market+OR+trading&hl=en-US&ceid=US:en` |

**地区代码参考：**
- `US:en` - 美国英文
- `GB:en` - 英国英文
- `CN:zh` - 中国中文
- `HK:zh` - 香港中文
- `TW:zh` - 台湾中文

### 专业新闻聚合 API（开发者友好）

| 服务 | 免费额度 | 特点 | 适用场景 |
|------|---------|------|----------|
| **NewsAPI.org** | 100 requests/day | RESTful API，多源聚合 | 开发新闻应用 |
| **GNews.io** | 100 requests/day | 简单 REST API | 快速原型 |
| **Currents API** | 600 requests/month | 无需 API Key 测试 | 小型项目 |
| **Newscatcher** | 付费为主 | 高级筛选、语义搜索 | 企业级新闻监控 |
| **Cloudsway Web Search API** | 免费试用 | 实时新闻、AI 相关性排序 | 实时资讯聚合 |

---

## 3. Tier 1 权威新闻媒体（RSS/官方源）

### 国际顶级通讯社与财经媒体

**Bloomberg（彭博社）** [^20^][^24^][^27^]
- 特点：每日发送约 11,000 条新闻，以快速头条为主
- 覆盖：全球金融、市场数据、宏观经济
- 访问：终端付费，部分 RSS 免费
- **替代免费方案**: Bloomberg RSS Feeds (有限制)
  - `https://feeds.bloomberg.com/bloomberg/view`

**Reuters（路透社）** [^20^][^24^][^27^]
- 特点：每日约 7,500 条新闻，更注重背景分析和深度报道
- 覆盖：国际金融、政治、商业新闻
- 优势：与 Bloomberg 合计占全球金融信息支出 60% 份额
- **免费 RSS**:
  - 科技: `https://www.reuters.com/technology/rss.xml`
  - 商业: `https://www.reuters.com/business/rss.xml`

**华尔街日报 (WSJ)** [^20^]
- **免费 RSS**:
  - 科技: `https://feeds.a.dj.com/rss/RSSWSJD.xml`
  - 商业: `https://feeds.a.dj.com/rss/RSSMarketsMain.xml`

### 科技媒体 Tier 1

| 媒体 | RSS Feed URL | 内容定位 | 更新频率 |
|------|-------------|---------|---------|
| **TechCrunch** | `https://techcrunch.com/feed/` | 初创公司、科技新闻 | 实时 |
| **The Verge** | `https://www.theverge.com/rss/index.xml` | 消费科技、数字文化 | 实时 |
| **Ars Technica** | `https://arstechnica.com/rss.xml` | 深度技术分析 | 每日 |
| **Wired** | `https://www.wired.com/feed/rss` | 科技趋势、网络安全 | 每日 |
| **MIT Technology Review** | `https://www.technologyreview.com/feed/` | 前沿科技研究 | 每日 |
| **ZDNet** | `https://www.zdnet.com/news/rss.xml` | 企业 IT 技术 | 实时 |
| **VentureBeat** | `https://feeds.feedburner.com/venturebeat` | AI/ML、游戏产业 | 实时 |
| **InfoWorld** | `https://www.infoworld.com/rss.xml` | 企业级技术 | 每日 |
| **Hacker News** | `https://news.ycombinator.com/rss` | 开发者社区精选 | 实时 |
| **O'Reilly Radar** | `https://feeds.feedburner.com/oreilly/radar` | 技术趋势分析 | 每周 |

### 开发者社区与开源动态

| 平台 | 数据源类型 | 获取方式 | 用途 |
|------|-----------|---------|------|
| **GitHub Trending** | Repository 趋势 | 无官方 API，需解析 HTML 或使用第三方 | 技术热点追踪 |
| **Stack Overflow Survey** | 开发者年度统计 | 公开数据下载 [^41^][^44^][^47^] | 技术趋势分析 |
| **GitHub Blog** | 官方公告 | `https://github.blog/feed/` | 平台更新 |
| **OpenAI Blog** | AI 研究进展 | `https://openai.com/news/rss.xml` | AI 前沿 [^14^] |
| **Hugging Face Blog** | ML 工具/模型 | `https://huggingface.co/blog/feed.xml` | AI 开发生态 |
| **Google AI Blog** | Google AI 研究 | `https://blog.google/technology/ai/rss/` | AI 动态 |
| **arXiv cs.AI** | 学术研究 | `https://rss.arxiv.org/rss/cs.AI` | 研究论文 |

---

## 4. 官方金融数据源（Financial Data）

### 免费/低成本金融 API

| 数据源 | 覆盖范围 | 免费额度 | API 特点 | 适用场景 |
|--------|---------|---------|----------|----------|
| **Alpha Vantage** [^33^] | 股票、外汇、加密货币、技术指标 | 500 requests/day | 官方授权 NASDAQ/OPRA 数据，毫秒级延迟 | 量化分析、交易算法 |
| **Financial Modeling Prep (FMP)** [^33^][^35^] | 股价、基本面、财报、宏观经济 | 250 requests/day | 一体化覆盖，开发者友好 | 股票筛选器、财报分析 |
| **Finnhub** [^33^] | 股价、新闻、情绪信号、事件日历 |  generous free tier | WebSocket 支持，新闻情绪分析 | 实时应用开发 |
| **Tiingo** [^33^] | 美股历史 EOD 数据、基本面 | 付费起步价低 | 历史数据质量高 | 回测研究 |
| **EOD Historical Data** [^35^][^36^] | 全球 70+ 交易所，30 年历史 | 20 API calls/day | REST API，JSON 格式，Excel 插件 | 历史数据分析 |
| **Market Stack** [^35^][^36^] | 170,000+ 股票代码，全球 70+ 交易所 | 100 requests/month | 银行级安全，JSON 格式 | 全球市场监控 |
| **Yahoo Finance** (unofficial) | 股票、ETF、加密货币 | 无限制（通过 yfinance Python 库） | 非官方 API，有频率限制 | 个人研究、教育 |

### 专业级金融数据（付费/机构级）

| 数据源 | 类型 | 特点 | 获取途径 |
|--------|------|------|----------|
| **Bloomberg Terminal** [^32^] | 终端服务 | 实时数据、分析工具 | 机构订阅 |
| **Refinitiv (LSEG)** [^32^] | 数据平台 | 全球定价数据、I/B/E/S 估计、ESG 数据 | 机构订阅 |
| **Capital IQ Pro** [^32^] | 数据分析 | 深度公司基本面、并购数据 | 机构订阅 |
| **FactSet** [^32^] | 数据平台 | 全球市场、固定收益数据 | 机构订阅 |
| **WRDS (CRSP/TAQ)** [^32^] | 学术研究 | 美股历史价格、日内交易数据 | 学术机构 |

---

## 5. 宏观经济与官方统计数据源

### 国际组织官方数据 API

| 数据源 | 覆盖范围 | API 详情 | 特点 |
|--------|---------|----------|------|
| **World Bank Open Data** [^54^][^55^][^58^][^61^][^62^] | 全球 16,000+ 指标，50+ 年历史，214 个国家 | `https://api.worldbank.org/v2/indicator/{code}` | 免费，无需 API Key，支持 JSON/XML/JSON-stat |
| **IMF Data Portal** [^30^] | 世界经济展望、国际收支、财政监测 | 新 API 支持批量下载 | 权威宏观经济数据 |
| **UN Data** [^60^][^67^] | 联合国各机构统计（人口、教育、健康、贸易） | `https://data.un.org/Handlers/DownloadHandler.ashx` | 单一入口，多机构数据 |
| **OECD Statistics** | 发达经济体经济数据、公共政策 | `https://stats.oecd.org/SDMX-JSON/data` | 标准化数据格式 |
| **Eurostat** | 欧盟统计数据 | REST API | 欧洲经济分析 |
| **UN Comtrade** | 国际贸易数据（1962-至今） | API 访问 | 双边商品贸易 |

### 美国官方经济数据

| 数据源 | 机构 | 覆盖内容 | API 访问 |
|--------|------|----------|----------|
| **FRED (Federal Reserve Economic Data)** [^48^][^56^][^59^][^63^][^71^] | 圣路易斯联储 | 816,000+ 时间序列，GDP、就业、通胀、利率 | `https://api.stlouisfed.org/fred/series/observations?series_id={id}` |
| **ALFRED** [^63^][^72^] | 圣路易斯联储 | FRED 历史版本数据（实时期数据） | 与 FRED 共用 API |
| **U.S. Census Bureau** [^49^][^50^][^51^][^52^][^53^] | 美国人口普查局 | 制造业、国际贸易、人口统计 | `https://api.census.gov/data/` |
| **Bureau of Economic Analysis (BEA)** | 经济分析局 | GDP、国际收支、区域经济 | `https://apps.bea.gov/API/signup/` |
| **BLS (Bureau of Labor Statistics)** | 劳工统计局 | CPI、就业数据、工资统计 | API 访问 |

**FRED API 常用经济指标代码参考** [^71^][^72^]：
```python
# GDP (国内生产总值)
series_id = "GDP"

# 失业率
series_id = "UNRATE"

# CPI (消费者价格指数)
series_id = "CPIAUCSL"

# 联邦基金利率
series_id = "FEDFUNDS"

# 10 年期国债收益率
series_id = "DGS10"

# 标普 500 指数
series_id = "SP500"
```

---

## 6. 开发者/技术行业特定数据源

### 编程语言趋势数据

| 指数 | 数据来源 | 更新频率 | 用途 |
|------|---------|---------|------|
| **TIOBE Index** [^37^][^38^][^40^] | 搜索引擎查询分析 | 月度 | 编程语言流行度排名 |
| **PYPL Index** [^42^][^45^][^46^] | Google 教程搜索统计 | 月度 | 语言学习热度趋势 |
| **Stack Overflow Survey** [^41^][^44^][^47^] | 开发者年度调查 | 年度 | 技术采用率、薪资数据 |
| **GitHub Octoverse** | GitHub 官方年度报告 | 年度 | 开源项目语言分布 |

### 实时技术趋势监控

| 数据源 | 内容 | 获取方式 |
|--------|------|----------|
| **GitHub Trending** | 热门仓库、开发者 | 页面解析: `https://github.com/trending` |
| **Stack Overflow Questions** | 技术问题趋势 | Stack Exchange API |
| **npm Trends** | JavaScript 包下载趋势 | `https://npmtrends.com/` |
| **Pypi Stats** | Python 包下载统计 | `https://pypistats.org/` |
| **Crates.io** | Rust 包生态 | API: `https://crates.io/api/` |
| **PyPI** | Python 包索引 | RSS/JSON API |

---


---

## 6. AI 与新兴技术数据源（AI & Emerging Tech）

### 6.1 顶级 AI 研究机构官方博客（Tier 1）

#### 主要 AI 实验室官方 RSS

| 机构 | RSS Feed URL | 更新频率 | 内容类型 | 权重 |
|------|-------------|---------|---------|------|
| **OpenAI News** [^14^][^75^][^78^] | `https://openai.com/news/rss.xml` | 每周 | GPT 更新、研究发布、产品公告 | P0 |
| **Google DeepMind** [^75^][^77^][^78^] | `https://deepmind.google/blog/rss.xml` | 1-2次/周 | Gemini、AlphaFold、强化学习突破 | P0 |
| **Google AI Blog** [^76^][^77^][^78^] | `https://blog.google/technology/ai/rss/` | 实时 | 模型与平台公告、应用案例 | P0 |
| **Google Research** [^75^][^81^] | `https://research.google/blog/rss/` | 1-2次/周 | 基础研究、论文解读 | P0 |
| **BAIR (Berkeley AI Research)** [^75^][^76^] | `https://bair.berkeley.edu/blog/feed.xml` | 每月2次 | 机器人、NLP、计算机视觉、强化学习 | P1 |
| **Stanford AI Lab** [^76^] | `https://ai.stanford.edu/blog/feed.xml` | 每月 | 前沿研究、学术讨论 | P1 |
| **CMU Machine Learning Blog** [^76^] | `https://blog.ml.cmu.edu/feed` | 双周 | 机器学习研究、教学资源 | P1 |
| **MIT Technology Review - AI** [^79^][^14^] | `https://www.technologyreview.com/topic/artificial-intelligence/feed/` | 每日 | 编辑分析、行业背景、商业影响 | P0 |
| **MIT News - AI** [^79^] | `https://news.mit.edu/rss/topic/artificial-intelligence2` | 每周 | MIT 研究成果、技术突破 | P1 |
| **MIRI (Machine Intelligence Research)** [^79^] | `https://intelligence.org/feed` | 每月 | AI 安全、对齐研究、数学理论 | P2 |

#### 重要提示：无官方 RSS 的 AI 公司（需使用替代方案）

| 公司 | 替代方案 | 说明 |
|------|---------|------|
| **Anthropic** [^90^][^94^] | 社区生成 RSS: `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml` | 官方无 RSS，但有第三方维护 [^75^] |
| **Anthropic Engineering** [^90^][^94^] | `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml` | 工程团队博客 |
| **Anthropic Research** [^94^] | `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml` | 研究论文发布 |
| **xAI** [^94^] | `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_xainews.xml` | 马斯克 xAI 新闻 |
| **Ollama** [^94^] | `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_ollama.xml` | 本地 LLM 工具 |

### 6.2 AI 论文与学术预印本

| 数据源 | RSS Feed URL | 内容 | 更新频率 |
|--------|-------------|------|----------|
| **arXiv CS.AI** [^77^][^78^] | `https://rss.arxiv.org/rss/cs.AI` | 人工智能论文 | 每日 |
| **arXiv CS.LG** [^76^][^77^] | `https://rss.arxiv.org/rss/cs.LG` | 机器学习论文 | 每日 |
| **arXiv CS.CL** [^77^][^78^] | `https://rss.arxiv.org/rss/cs.CL` | 计算语言学/NLP | 每日 |
| **arXiv CS.CV** | `https://rss.arxiv.org/rss/cs.CV` | 计算机视觉 | 每日 |
| **arXiv CS.RO** | `https://rss.arxiv.org/rss/cs.RO` | 机器人学 | 每日 |
| **Distill.pub** [^76^] | `https://distill.pub/rss.xml` | 高质量可视化论文解释 | 不定期 |
| **Papers With Code** [^81^] | `https://paperswithcode.com/latest` | 带代码的最新论文 | 每日 |
| **Google Research** [^76^] | `https://feeds.feedburner.com/blogspot/gJZg` | Google 研究博客 | 每周 |

### 6.3 AI 行业新闻与开发者社区

#### 专业 AI 媒体（Tier 1）

| 媒体 | RSS Feed URL | 特点 | 权重 |
|------|-------------|------|------|
| **Hugging Face Blog** [^14^][^75^][^76^] | `https://huggingface.co/blog/feed.xml` | 开源模型、工具更新、教程 | P0 |
| **Towards Data Science** [^76^] | `https://towardsdatascience.com/feed` | Medium 最大数据科学社区 | P1 |
| **KDnuggets** [^76^] | `https://kdnuggets.com/feed` | 数据科学、AI 新闻、教程 | P1 |
| **VentureBeat - AI** [^83^][^84^][^85^] | `https://venturebeat.com/category/ai/feed` | AI 商业应用深度报道 | P1 |
| **TechCrunch - AI** [^83^][^84^] | `https://techcrunch.com/category/artificial-intelligence/feed` | 初创公司、投资新闻 | P1 |
| **MarkTechPost** [^14^][^76^] | `https://marktechpost.com/feed/` | AI 论文摘要、快速发布 | P2 |
| **O'Reilly AI & ML** [^79^][^76^] | `https://oreilly.com/radar/topics/ai-ml` | 行业洞察、技术趋势 | P1 |
| **Synced (机器之心)** [^78^] | `https://www.jiqizhixin.com/rss` | 中文顶尖 AI 媒体 | P1 |
| **AI News** [^83^][^84^] | `https://www.artificialintelligence-news.com/feed/rss/` | AI 新闻聚合 | P2 |
| **Data Machina** [^83^][^84^] | `https://datamachina.substack.com/feed` | 每周 AI/ML 研究进展 | P2 |

#### 开发者社区与讨论

| 平台 | 数据源 | 获取方式 | 内容类型 |
|------|--------|---------|----------|
| **Hacker News** [^77^][^78^] | AI 相关讨论 | `https://hnrss.org/newest?q=AI` | 技术社区热点 |
| **Hacker News** | LLM 相关 | `https://hnrss.org/newest?q=LLM` | 大模型讨论 |
| **Hacker News** | ChatGPT 相关 | `https://hnrss.org/newest?q=ChatGPT` | OpenAI 产品讨论 |
| **Reddit r/MachineLearning** | 社区聚合 | 需 RSSHub 或第三方 | 研究讨论、资源分享 |
| **Reddit r/LocalLLaMA** | 本地模型讨论 | 需 RSSHub 或第三方 | 开源模型、硬件讨论 |

#### 个人博客与意见领袖（Andrej Karpathy 推荐精选）

| 博主 | RSS Feed URL | 专长领域 | 更新频率 |
|------|-------------|---------|----------|
| **Simon Willison** [^76^][^88^] | `https://simonwillison.net/atom/everything/` | LLM 应用、代码实测、Django | 持续 |
| **Andrej Karpathy** | `https://karpathy.bearblog.dev/feed/` | AI 研究、教育、行业洞察 | 不定期 |
| **Julia Evans** [^76^] | `https://jvns.ca/atom.xml` | 底层技术、漫画解释 | 每周 |
| **Terence Tao (陶哲轩)** | `https://terrytao.wordpress.com/feed/` | 数学理论、AI 数学基础 | 不定期 |
| **Scott Aaronson** [^104^] | `https://scottaaronson.blog/?feed=rss2` | 量子计算、计算复杂性、AI 安全 | 不定期 |
| **Machine Learning Mastery** [^76^] | `https://feeds.feedburner.com/MachineLearningMastery` | 入门教程、实用指南 | 每周 |
| **Chip Huyen** | `https://huyenchip.com/feed.xml` | ML 工程、系统设计 | 每月 |

### 6.4 加密货币与区块链（Web3 & Blockchain）

#### Tier 1 权威加密媒体

| 媒体 | RSS Feed URL | 特点 | 权重 |
|------|-------------|------|------|
| **CoinDesk** [^91^][^93^] | `https://coindesk.com/feed` | 加密行业领导者、新闻+数据 | P0 |
| **Cointelegraph** [^91^][^93^] | `https://cointelegraph.com/rss` | 多语言、涵盖 DeFi/NFT/监管 | P0 |
| **The Block** [^91^] | `https://theblock.co/rss` | 机构级分析、研究深入 | P1 |
| **Decrypt** [^91^] | `https://decrypt.co/feed` | 用户友好、教育性强 | P1 |
| **Bitcoin Magazine** [^91^] | `https://bitcoinmagazine.com/feed` | 比特币生态权威 | P1 |
| **Messari** [^91^] | `https://messari.io/rss` | 研究驱动、数据丰富 | P1 |
| **CryptoSlate** [^93^] | `https://cryptoslate.com/feed` | 新闻+数据+分析 | P2 |

#### 区块链数据与分析

| 数据源 | 类型 | API/RSS 可用性 | 说明 |
|--------|------|---------------|------|
| **CoinMarketCap** | 市场数据 | API (付费) | 市值、交易量排名 |
| **CoinGecko** | 市场数据 | API (免费额度) | 替代 CoinMarketCap |
| **Glassnode** | 链上分析 | API (付费) | 比特币/以太坊链上指标 |
| **Dune Analytics** | 链上数据 | 需导出 | 社区创建的分析仪表板 |
| **Etherscan** | 交易数据 | API (免费+付费) | 以太坊区块链浏览器 |

### 6.5 量子计算（Quantum Computing）

#### 主要量子计算公司官方源

| 公司/机构 | RSS/新闻源 | 类型 | 说明 |
|-----------|-----------|------|------|
| **IBM Quantum** [^99^][^104^] | `https://research.ibm.com/quantum-computing/rss` (推测) | 硬件+软件 | 量子计算领导者 |
| **Google Quantum AI** [^99^] | 通过 Google Research Blog | 研究进展 | 量子霸权里程碑 |
| **Microsoft Quantum** [^99^] | 官方博客 | 云量子计算 | Azure Quantum |
| **IonQ** [^99^] | 官方新闻 | 离子阱量子计算 | 上市公司 |
| **Rigetti Computing** [^99^] | 官方新闻 | 超导量子计算 | 量子云服务 |
| **D-Wave Systems** [^99^] | 官方新闻 | 量子退火 | 专注优化问题 |
| **QuEra Computing** [^99^] | 官方新闻 | 中性原子 | 哈佛/麻省理工衍生 |
| **Xanadu** [^99^] | 官方新闻 | 光量子计算 | PennyLane 框架 |

#### 量子计算新闻聚合与学术

| 数据源 | URL/Feed | 内容类型 |
|--------|---------|----------|
| **QuantumNews.ai** [^99^] | `https://quantumnews.ai/` | 聚合 120+ 量子新闻源 |
| **Quantum Computing Report** [^101^] | `https://quantumcomputingreport.com/` | 行业分析、投资新闻 |
| **The Quantum Insider** [^104^] | `https://thequantuminsider.com/` | 市场情报、公司动态 |
| **arXiv Quantum Physics** [^99^] | `https://rss.arxiv.org/rss/quant-ph` | 量子物理论文 |
| **Qiskit Blog** [^104^] | `https://medium.com/feed/qiskit` | IBM 量子开发框架 |
| **QuTech Blog** [^104^] | `https://blog.qutech.nl/feed` | 代尔夫特理工/荷兰 |
| **Scott Aaronson Blog** [^104^] | `https://scottaaronson.blog/?feed=rss2` | 理论计算机科学、量子计算 |

### 6.6 增强现实与虚拟现实（AR/VR/XR）

| 媒体 | RSS Feed URL | 特点 | 权重 |
|------|-------------|------|------|
| **Road to VR** [^89^] | `https://roadtovr.com/feed` | 消费者 VR 行业领导者 | P0 |
| **Upload VR** [^89^] | `https://uploadvr.com/feed` | XR 行业新闻、评测 | P0 |
| **The Ghost Howls** [^89^] | `https://skarredghost.com/feed` | VR 创业、技术分析 | P1 |
| **Hypergrid Business** [^89^] | `https://hypergridbusiness.com/feed` | 企业 VR/AR 应用 | P1 |
| **Game Developer - XR** [^89^] | `https://gamedeveloper.com/rss.xml` | VR 游戏开发 | P2 |
| **Mixed Reality News** | 第三方聚合 | 微软 HoloLens/MR | P2 |

### 6.7 其他新兴技术

#### 生物技术（Biotech）

| 数据源 | RSS Feed URL | 说明 |
|--------|-------------|------|
| **MIT News - Bioengineering** | `https://news.mit.edu/rss/topic/bioengineering-and-biotechnology` | MIT 生物工程 |
| **Nature Biotechnology** | 需订阅 | 顶级学术期刊 |
| **STAT News** | `https://statnews.com/feed` | 生物医药新闻 |
| **Fierce Biotech** | `https://fiercebiotech.com/feed` | 生物科技行业 |

#### 太空技术（Space Tech）

| 数据源 | RSS Feed URL | 说明 |
|--------|-------------|------|
| **SpaceNews** | `https://spacenews.com/feed/` | 太空产业新闻 |
| **Space.com** | `https://space.com/feeds/all` | 综合太空新闻 |
| **NASA Blogs** | `https://blogs.nasa.gov/feed/` | 官方博客 |
| **SpaceX Updates** | 社区生成 RSS | 发射更新 |
| **Ars Technica - Space** | `https://arstechnica.com/tag/space/feed/` | 深度报道 |

#### 机器人技术（Robotics）

| 数据源 | RSS Feed URL | 说明 |
|--------|-------------|------|
| **IEEE Spectrum Robotics** | `https://spectrum.ieee.org/robotics/rss` | IEEE 机器人新闻 |
| **The Robot Report** | `https://therobotreport.com/feed` | 机器人产业 |
| **Boston Dynamics News** | 官方新闻稿 | 人形机器人 |
| **Tesla Bot News** | 通过 Tesla 官方 | Optimus 进展 |

### 6.8 AI 与科技聚合源（一站式监控）

#### 聚合 RSS 服务

| 服务 | URL | 聚合范围 | 说明 |
|------|-----|---------|------|
| **Planet AI** [^98^] | `https://planet-ai.net/rss.xml` | OpenAI, Anthropic, Google AI, Meta, Hugging Face 等 30+ 源 | 单一 Feed 监控所有 AI 新闻 |
| **GitHub Awesome RSSHub** [^78^] | `https://github.com/JackyST0/awesome-rsshub-routes` | 中文 RSSHub 路由精选 | 适合中文用户 |
| **RSSHub** | `https://rsshub.app/` | 万能 RSS 生成器 | 可为无 RSS 网站生成 Feed |
| **Feedless** [^75^] | 第三方服务 | AI 公司新闻 | 为无 RSS 网站提供桥接 |

#### 推荐 RSS 阅读器配置（针对 OpenClaw 项目）

```yaml
# AI & Emerging Tech RSS 监控配置
ai_tech_sources:
  tier_1_must_have:
    - openai_news: "https://openai.com/news/rss.xml"
    - deepmind: "https://deepmind.google/blog/rss.xml"
    - google_ai: "https://blog.google/technology/ai/rss/"
    - huggingface: "https://huggingface.co/blog/feed.xml"
    - arxiv_ai: "https://rss.arxiv.org/rss/cs.AI"
    - mit_tech_review_ai: "https://www.technologyreview.com/topic/artificial-intelligence/feed/"

  tier_2_important:
    - bair: "https://bair.berkeley.edu/blog/feed.xml"
    - stanford_ai: "https://ai.stanford.edu/blog/feed.xml"
    - towards_data_science: "https://towardsdatascience.com/feed"
    - venturebeat_ai: "https://venturebeat.com/category/ai/feed"
    - techcrunch_ai: "https://techcrunch.com/category/artificial-intelligence/feed"
    - coindesk: "https://coindesk.com/feed"
    - roadtovr: "https://roadtovr.com/feed"

  tier_3_supplementary:
    - ai_news: "https://www.artificialintelligence-news.com/feed/rss/"
    - marktechpost: "https://marktechpost.com/feed/"
    - decrypt: "https://decrypt.co/feed"
    - uploadvr: "https://uploadvr.com/feed"

  community_generated:
    - anthropic_news: "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml"
    - anthropic_engineering: "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml"
    - xai_news: "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_xainews.xml"
```

### 6.9 数据源使用建议

**优先级配置策略：**

1. **P0 级（立即告警）**：OpenAI、DeepMind、Google AI、Hugging Face 的博客更新
   - 涉及：重大模型发布（如 GPT-5、Gemini 2.0）、API 变更、安全公告

2. **P1 级（每日汇总）**：学术预印本（arXiv）、顶级媒体（MIT Tech Review）、主要社区
   - 涉及：研究突破、行业趋势、重要产品发布

3. **P2 级（每周摘要）**：二级市场媒体、垂直领域（量子、VR、生物）
   - 涉及：深度分析、小众技术进展

**内容过滤建议：**

```python
# AI 内容相关性评分关键词
priority_keywords = [
    "GPT", "Claude", "Gemini", "Llama", "open source model",
    "AGI", "alignment", "safety", "multimodal", "reasoning",
    "AI agents", "RAG", "fine-tuning", "prompt engineering",
    "Neuralink", "robotics", "quantum advantage", "fusion energy"
]

# 过滤低质量内容
exclude_keywords = [
    "crypto scam", "get rich quick", "unverified claim",
    "sponsored content", "affiliate marketing"
]
```

**可靠性验证机制：**

- **学术内容**：核实是否来自 arXiv 顶级类别（cs.AI、cs.LG、cs.CL）或顶级会议（NeurIPS、ICML、ACL）
- **行业新闻**：交叉验证至少 2 个独立源（如 OpenAI 官方 + TechCrunch + The Verge）
- **技术博客**：验证作者背景（是否来自知名实验室或公司）

## 7. 数据源质量评估与使用建议

### 数据质量分级体系

**Tier 1 - 权威必查源（强制引用）：**
- ✅ 官方政府机构（美联储、世界银行、IMF）
- ✅ 顶级通讯社（Reuters、Bloomberg）
- ✅ 官方博客（OpenAI、Google AI）
- ✅ 学术数据库（arXiv、Google Scholar）

**Tier 2 - 专业验证源（交叉验证）：**
- ⚡ 专业媒体（TechCrunch、The Verge）
- ⚡ 行业分析报告（Gartner、McKinsey）
- ⚡ 开发者社区（Hacker News、Stack Overflow）

**Tier 3 - 补充参考源（谨慎使用）：**
- ⚠️ 自媒体/个人博客（需验证作者背景）
- ⚠️ 社交媒体（Twitter/X、Reddit，需事实核查）

### API 使用最佳实践

**1. 频率限制管理**
- 实施指数退避重试策略
- 缓存响应数据（建议 Redis）
- 监控 API 配额使用情况

**2. 数据验证与清洗**
```python
# 示例：数据源健康检查逻辑
def validate_data_source(source, response):
    checks = {
        "timeliness": response.timestamp > (now() - 24.hours),
        "accuracy": cross_verify_with_tier1_source(response.data),
        "completeness": len(response.data.required_fields) == expected_count,
        "source_availability": source.uptime > 99.5%
    }
    return all(checks.values())
```

**3. 故障转移策略**
- 每个数据类型至少配置 2 个备用源
- 本地缓存最近 30 天关键数据
- 自动切换机制（主源失效时切换到备用源）

**4. 引用规范**
- 所有数据必须标注来源 URL 和访问日期
- 使用置信度评分标记数据可靠性
- 低置信度数据（<70%）添加"待核实"标记

---

## 8. 快速集成清单（Checklist）

### 立即可用的数据源（无需注册）
- [ ] Google News RSS
- [ ] World Bank Open Data API
- [ ] Hacker News RSS
- [ ] arXiv RSS (cs.AI, cs.CL)
- [ ] Andrej Karpathy 推荐的 92 个博客 OPML

### 需要免费注册获取 API Key
- [ ] Alpha Vantage (股票数据)
- [ ] Financial Modeling Prep (金融数据)
- [ ] FRED (经济数据)
- [ ] NewsAPI.org (新闻聚合)
- [ ] GitHub API (开发者数据)

### 建议配置的数据源 MCP 服务器
- [ ] World Bank MCP
- [ ] FRED MCP Server [^73^][^74^]
- [ ] Alpha Vantage MCP
- [ ] News API MCP
- [ ] arXiv MCP

---

## 9. 参考资源链接汇总

**Andrej Karpathy 相关：**
- 92 个博客 OPML: https://gist.github.com/emschwartz/e6d2bf860ccc367fe37ff953ba6de66b
- Karpathy 博客: https://karpathy.bearblog.dev/

**金融数据 API 文档：**
- Alpha Vantage: https://www.alphavantage.co/documentation/
- FMP: https://site.financialmodelingprep.com/developer/docs/
- FRED API: https://fred.stlouisfed.org/docs/api/fred/

**宏观经济数据：**
- World Bank API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- IMF Data: https://www.imf.org/en/data
- UN Data: https://data.un.org/

**新闻 RSS 工具：**
- RSS FeedSpot (Technology): https://rss.feedspot.com/technology_rss_feeds/
- AI News RSS: https://www.readless.app/blog/best-ai-news-rss-feeds-2026

---

*数据源清单版本: v1.0*  
*维护建议: 每季度审查数据源可用性和准确性，更新失效链接*
