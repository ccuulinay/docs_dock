---
**分析任务指令**
请按以下步骤分析提供的代码脚本：

1. 代码结构识别
- 区分Python和SQL代码段
- 定位数据源连接模块
- 标记所有数据筛选操作节点

2. 条件提取规范
▶ SQL脚本分析
- 解析WHERE/HAVING子句
- 提取JOIN条件中的过滤逻辑
- 识别动态参数化查询的占位符
- 标注CASE WHEN语句中的判断条件

▶ Python脚本分析
- 解析pandas.query()/filter()
- 分析条件推导式（List/Dict Comprehensions）
- 跟踪变量传递的条件参数
- 识别自定义函数中的条件判断

3. 条件标准化输出
对每个筛选条件生成结构化描述：
```
{
  "condition_type": "地域筛选 | 时间范围 | 消费行为...",
  "expression": "country_code = 'US'",
  "parameters": ["start_date", "end_date"],
  "source": {
    "file": "customer_segment.py",
    "line": 45,
    "code_snippet": "df = df[df['last_purchase'] > start_date]"
  },
  "logic_relation": "AND/OR/NOT"
}
```

4. 可视化输出要求
生成Markdown格式报告，包含：
- 条件分类统计表
- 参数依赖关系图
- 条件逻辑组合示意图
- 重点条件代码溯源

**特别说明**
- 处理嵌套条件时保持逻辑完整性
- 区分硬编码值与动态参数
- 标注可能产生空值的筛选条件
- 识别冗余/冲突条件组合
---

这个提示词的特点：
1. 多维度分析：同时覆盖Python和SQL的语法特性
2. 上下文感知：跟踪变量传递和参数化查询
3. 结构化解构：将条件拆解为可解释的标准化元素
4. 可视化输出：便于快速定位和理解复杂条件逻辑
5. 异常检测：自动识别可能的问题条件