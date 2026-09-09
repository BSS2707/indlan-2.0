class Node:
    pass


# ---------- Expressions ----------

class NumberLit(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class StringLit(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class FString(Node):
    def __init__(self, template, expressions, line):
        self.template = template  # string with {} placeholders
        self.expressions = expressions  # list of expression strings to parse
        self.line = line

class BoolLit(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class NullLit(Node):
    def __init__(self, line):
        self.line = line

class ListLit(Node):
    def __init__(self, elements, line):
        self.elements = elements
        self.line = line

class DictLit(Node):
    def __init__(self, pairs, line):
        self.pairs = pairs  # list of (key_node, value_node)
        self.line = line

class Identifier(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line

class BinOp(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

class UnaryOp(Node):
    def __init__(self, op, operand, line):
        self.op = op
        self.operand = operand
        self.line = line

class LogicalOp(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

class Assign(Node):
    def __init__(self, target, value, line, op="="):
        self.target = target
        self.value = value
        self.op = op
        self.line = line

class KeywordArg(Node):
    def __init__(self, name, value, line):
        self.name = name
        self.value = value
        self.line = line

class Call(Node):
    def __init__(self, callee, args, line):
        self.callee = callee
        self.args = args  # list of expr nodes or KeywordArg nodes
        self.line = line

class Index(Node):
    def __init__(self, obj, index, line):
        self.obj = obj
        self.index = index
        self.line = line

class GetAttr(Node):
    def __init__(self, obj, name, line):
        self.obj = obj
        self.name = name
        self.line = line

class MethodCall(Node):
    def __init__(self, obj, method_name, args, line):
        self.obj = obj
        self.method_name = method_name
        self.args = args  # list of expr nodes or KeywordArg nodes
        self.line = line

class FunctionExpr(Node):
    """Anonymous function (used internally for fun declarations too)."""
    def __init__(self, params, body, line, name=None):
        self.params = params
        self.body = body
        self.line = line
        self.name = name


# ---------- Statements ----------

class LetStmt(Node):
    def __init__(self, name_or_names, value, line):
        if isinstance(name_or_names, list):
            self.names = name_or_names
            self.name = name_or_names[0] if len(name_or_names) == 1 else None
        else:
            self.names = [name_or_names]
            self.name = name_or_names
        self.value = value
        self.line = line

class ImportStmt(Node):
    def __init__(self, module_path, alias, line):
        self.module_path = module_path
        self.alias = alias
        self.line = line

class FromImportStmt(Node):
    def __init__(self, module_path, items, line):
        self.module_path = module_path
        self.items = items  # list of (name, alias) tuples
        self.line = line

class ExprStmt(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

class Block(Node):
    def __init__(self, statements, line):
        self.statements = statements
        self.line = line

class IfStmt(Node):
    def __init__(self, branches, else_block, line):
        # branches: list of (condition, block)
        self.branches = branches
        self.else_block = else_block
        self.line = line

class WhileStmt(Node):
    def __init__(self, condition, body, line):
        self.condition = condition
        self.body = body
        self.line = line

class DoWhileStmt(Node):
    def __init__(self, body, condition, line):
        self.body = body
        self.condition = condition
        self.line = line

class SwitchStmt(Node):
    def __init__(self, subject, cases, default_block, line):
        # cases: list of (value_expr, block)
        self.subject = subject
        self.cases = cases
        self.default_block = default_block
        self.line = line

class ForStmt(Node):
    def __init__(self, var_name, iterable, body, line):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body
        self.line = line

class FunDecl(Node):
    def __init__(self, name, params, body, line):
        self.name = name
        self.params = params
        self.body = body
        self.line = line

class ReturnStmt(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

class BreakStmt(Node):
    def __init__(self, line):
        self.line = line

class ContinueStmt(Node):
    def __init__(self, line):
        self.line = line

class ClassDecl(Node):
    def __init__(self, name, methods, line):
        self.name = name
        self.methods = methods  # list of FunDecl
        self.line = line

class Program(Node):
    def __init__(self, statements):
        self.statements = statements