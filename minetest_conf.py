
class MinetestConfParseSyntaxException(Exception):
    def __init__(self, message=None, line_num=None, col_num=None, cause=None):
        super().__init__(message, line_num, col_num, cause)
def parse_conf(conf_file):
    with open(conf_file, "r") as f:
        everything = f.read()
        i = 0
        brackets_stack = []
        line_num = 1
        col_num = 1
        while i < len(everything):
            c = everything[i]
            if c == "{":
                brackets_stack.append("{")
            elif c == "(":
                brackets_stack.append("(")
            elif c == ")":
                if not brackets_stack:
                    raise MinetestConfParseSyntaxException(line_num=line_num, col_num=col_num, message=f"Unexpected closing bracket {c}")
                if brackets_stack[-1] == "(":
                    brackets_stack.pop()
                else:
                    raise MinetestConfParseSyntaxException(line_num=line_num, col_num=col_num, message=f"Mismatched brackets (expected ')', got {c})")
            elif c == "}":
                if not brackets_stack:
                    raise MinetestConfParseSyntaxException(line_num=line_num, col_num=col_num, message=f"Unexpected closing bracket {c}")
                if brackets_stack[-1] == "{":
                    brackets_stack.pop()
                else:
                    raise MinetestConfParseSyntaxException(line_num=line_num, col_num=col_num, message=f"Mismatched brackets (expected '}}', got {c})")
            elif c == "\n":
                line_num += 1
                col_num = 1
            col_num += 1
            i += 1