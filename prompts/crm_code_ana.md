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

**Prompt for Analyzing Customer Filtering Scripts (Python/SQL)**  
---

**Objective**  
Analyze Python/SQL scripts designed to filter customer data based on criteria and generate a customer list. Extract and catalog all filtering conditions with contextual metadata.

---

### **Analysis Instructions**  
1. **Code Structure Identification**  
   - Separate Python and SQL code blocks.  
   - Identify data source connections (e.g., `pandas.read_sql`, SQLAlchemy, direct database connectors).  
   - Flag all filtering operations (e.g., SQL `WHERE`, Python `df.query()`, list comprehensions).  

2. **Condition Extraction Rules**  
   **For SQL Scripts**:  
   - Parse `WHERE`/`HAVING`/`ON` (JOIN) clauses.  
   - Extract conditions from dynamic queries (e.g., `@variable`, `?` placeholders).  
   - Decode nested `CASE WHEN` logic and subqueries.  

   **For Python Scripts**:  
   - Analyze `pandas` operations: `df[df['column'] > value]`, `df.query()`, `df.filter()`.  
   - Trace variables/parameters used in conditional logic (e.g., `start_date`, `min_revenue`).  
   - Inspect custom functions and loops for implicit filtering.  

3. **Structured Output Format**  
   For each condition, generate:  
   ```json  
   {  
     "id": "Condition_01",  
     "type": "Geographic | Temporal | Behavioral | ...",  
     "expression": "country = 'US' AND registration_date BETWEEN ? AND ?",  
     "parameters": ["start_date", "end_date"],  
     "source": {  
       "file": "filter_customers.py",  
       "line": 28,  
       "code_snippet": "df = df[df['status'] == 'active']"  
     },  
     "hardcoded_values": ["active"],  
     "dependencies": ["external_config.csv"],  
     "logic_operator": "AND/OR/NOT"  
   }  
   ```  

4. **Reporting Requirements**  
   Generate a Markdown report containing:  
   - **Summary Table**: Condition types, frequency, parameter dependencies.  
   - **Logic Map**: Visualize relationships between conditions (e.g., Mermaid flowchart).  
   - **Parameter Tracking**: List all dynamic variables and their sources.  
   - **Conflict Detection**: Highlight overlapping/redundant conditions (e.g., `age > 18` vs `age >= 21`).  

---

### **Special Guidelines**  
- Preserve nested logic hierarchies (e.g., parent-child conditions).  
- Differentiate between hardcoded values and parameterized inputs.  
- Flag conditions prone to null/empty results (e.g., `WHERE revenue IS NULL`).  
- Identify security risks (e.g., SQL injection patterns in raw queries).  

--- 

**Example Trigger**  
```  
Analyze the attached Python/SQL scripts:  
- Script 1: `customer_segment.py` (uses Pandas + SQLAlchemy)  
- Script 2: `active_users.sql` (includes JOINs and CASE statements)  
```  