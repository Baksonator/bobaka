class AST(object):
    pass

class Program(AST):
    def __init__(self, declarations):
        self.children = declarations

class Library(AST):
    def __init__(self, library):
        self.library = library

class Function(AST):
    def __init__(self, name, parameters, bodynode):
        self.name = name
        self.parameters = parameters
        self.bodynode = bodynode

class FunctionBody(AST):
    def __init__(self, expressions, ret_statement):
        self.expressions = expressions
        self.ret_statement = ret_statement

class FunctionCall(AST):
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

class MainFunction(AST):
    def __init__(self, name, function_call):
        self.name = name
        self.function_call = function_call

class FunDecl(AST):
    def __init__(self, type_node, fun_name, args_node, stmts_node):
        self.type_node = type_node
        self.fun_name = fun_name
        self.args_node = args_node
        self.stmts_node = stmts_node

class RegExpression(AST):
    def __init__(self, negates, chain, operators):
        self.negates = negates
        self.chain = chain
        self.operators = operators

class BoolExpression(AST):
    def __init__(self, negates, chain, operators):
        self.negates = negates
        self.chain = chain
        self.operators = operators

class Conditional(AST):
    def __init__(self, condition, then_part, else_part):
        self.condition = condition
        self.then_part = then_part
        self.else_part = else_part

class Loop(AST):
    def __init__(self, condition, loop_body, last_part):
        self.condition = condition
        self.loop_body = loop_body
        self.last_part = last_part

class Var(AST):
    def __init__(self, var):
        self.var = var

class VarDecl(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAssignment(AST):
    def __init__(self, name, function_call):
        self.name = name
        self.function_call = function_call

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class String(AST):
    def __init__(self, value):
        self.value = value

class ListVar(AST):
    def __init__(self, list_name, index):
        self.list_name = list_name
        self.index = index

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_{}'.format(type(node).__name__)
        visitor = getattr(self, method_name, self.error)
        return visitor(node)

    def error(self, node):
        raise Exception('Not found {}'.format(type(node).__name__))
