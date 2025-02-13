import ast
import sqlparse
import pandas as pd

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.conditions = []
        self.variables = {}
    
    def visit_Assign(self, node):
        """记录变量赋值信息"""
        if isinstance(node.value, (ast.Constant, ast.Compare, ast.BinOp, ast.BoolOp)):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.variables[target.id] = node.value
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """处理函数调用"""
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            args = node.args
            
            # 处理SQL查询
            if method_name in ['query', 'execute'] and args:
                self._process_sql_call(node, args[0], method_name)
            
            # 处理pandas的query方法
            if method_name == 'query' and args:
                self._process_pandas_query(node, args[0])
        
        self.generic_visit(node)
    
    def visit_Subscript(self, node):
        """处理布尔索引条件"""
        slice_node = node.slice if not isinstance(node.slice, ast.Index) else node.slice.value
        
        if isinstance(slice_node, (ast.Compare, ast.BinOp, ast.BoolOp)):
            self._record_pandas_condition(slice_node, node.lineno)
        elif isinstance(slice_node, ast.Name) and slice_node.id in self.variables:
            self._record_pandas_condition(self.variables[slice_node.id], node.lineno)
        
        self.generic_visit(node)
    
    def _process_sql_call(self, node, arg_node, method_name):
        """处理SQL查询调用"""
        sql = self._extract_string_value(arg_node)
        if sql:
            source_type = 'BigQuery' if method_name == 'query' else 'Other SQL'
            for condition in self._parse_sql_conditions(sql):
                self.conditions.append({
                    'Type': source_type,
                    'Condition': condition,
                    'Location': f"Line {node.lineno}"
                })
    
    def _process_pandas_query(self, node, arg_node):
        """处理pandas query方法"""
        query_str = self._extract_string_value(arg_node)
        if query_str:
            self.conditions.append({
                'Type': 'Pandas',
                'Condition': query_str,
                'Location': f"Line {node.lineno}"
            })
    
    def _record_pandas_condition(self, condition_node, lineno):
        """记录pandas布尔条件"""
        try:
            condition = ast.unparse(condition_node)
            self.conditions.append({
                'Type': 'Pandas',
                'Condition': condition,
                'Location': f"Line {lineno}"
            })
        except:
            pass
    
    def _extract_string_value(self, node):
        """提取字符串值，支持直接字符串或变量引用"""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name) and node.id in self.variables:
            var_node = self.variables[node.id]
            if isinstance(var_node, ast.Constant) and isinstance(var_node.value, str):
                return var_node.value
        return None
    
    @staticmethod
    def _parse_sql_conditions(sql):
        """解析SQL中的条件"""
        conditions = []
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            for token in statement.tokens:
                if isinstance(token, sqlparse.sql.Where):
                    where_str = token.value.replace("WHERE", "", 1).strip()
                    conditions.extend([cond.strip() for cond in re.split(r'\b(?:AND|OR)\b', where_str)])
        return conditions

def analyze_code(code):
    """分析代码并返回结果"""
    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return pd.DataFrame(analyzer.conditions)

if __name__ == "__main__":
    code = input("请输入要分析的Python代码：\n")
    try:
        result_df = analyze_code(code)
        print("\n分析结果：")
        print(result_df.to_string(index=False))
    except Exception as e:
        print(f"分析时出错：{e}")
