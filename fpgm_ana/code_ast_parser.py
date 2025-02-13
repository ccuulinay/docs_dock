import ast
import sqlparse
from sqlparse.sql import Where, Comparison
import pandas as pd

class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.results = []
        self.current_class = None

    def visit_Call(self, node):
        # 检测pandas的query()方法
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'query':
                for arg in node.args:
                    if isinstance(arg, ast.Str):
                        self._record_condition(arg.s, 'pandas', node.lineno)
            elif node.func.attr == 'loc':
                self._analyze_loc_condition(node)

        # 检测SQL执行语句
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
            for arg in node.args:
                if isinstance(arg, ast.Str):
                    self._parse_sql(arg.s, node.lineno)

        self.generic_visit(node)

    def visit_Subscript(self, node):
        # 检测布尔索引条件
        if isinstance(node.slice, ast.Index):
            slice_value = node.slice.value
            if isinstance(slice_value, ast.BoolOp):
                self._parse_boolop(slice_value, node.lineno)
        self.generic_visit(node)

    def _parse_boolop(self, boolop, lineno):
        for value in boolop.values:
            if isinstance(value, ast.Compare):
                condition = ast.unparse(value).strip()
                self._record_condition(condition, 'pandas', lineno)

    def _analyze_loc_condition(self, node):
        for keyword in node.keywords:
            if keyword.arg == 'mask':
                condition = ast.unparse(keyword.value).strip()
                self._record_condition(condition, 'pandas', node.lineno)

    def _parse_sql(self, sql, lineno):
        parsed = sqlparse.parse(sql)
        for stmt in parsed:
            for token in stmt.tokens:
                if isinstance(token, Where):
                    where_clause = str(token).replace("WHERE", "", 1).strip()
                    for sub_token in token.tokens:
                        if isinstance(sub_token, Comparison):
                            self._record_condition(str(sub_token).strip(), 'SQL', lineno)

    def _record_condition(self, condition, type_, lineno):
        self.results.append({
            "Type": type_,
            "Condition": condition,
            "Line": lineno,
            "Context": self.current_class
        })

def analyze_code(code):
    tree = ast.parse(code)
    extractor = ConditionExtractor()
    extractor.visit(tree)
    return pd.DataFrame(extractor.results)

if __name__ == "__main__":
    sample_code = """
import pandas as pd
from sqlalchemy import create_engine

df = pd.DataFrame({'a': [1,2,3], 'b': [4,5,6]})
filtered = df[df['a'] > 1]
query_result = df.query('a < 3 and b > 4')
engine = create_engine('sqlite:///:memory:')
with engine.connect() as conn:
    conn.execute("SELECT * FROM table WHERE col1 > 100 AND col2 = 'test'")
    conn.execute('UPDATE users SET status=1 WHERE last_login < "2023-01-01"')
"""

    df = analyze_code(sample_code)
    print("\n提取的条件汇总表：")
    print(df.to_markdown(index=False))