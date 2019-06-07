from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import *
from interpreter.syntax_analysis.util import restorable
import sys

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Greska u parsiranju')

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        declarations = []

        while self.current_token.type == DOLLAR:
            declarations.append(self.include_library())

        while self.current_token.type == ID:
            declarations.append(self.var_declaration())

        self.eat(LESS)
        self.eat(MINUS)
        self.eat(LARROW)

        while self.current_token.type == ID:
            if self.current_token.value == 'main':
                declarations.append(self.main_function())
            else:
                declarations.append(self.function())

        return Program(declarations)

    def main_function(self):
        name = self.current_token.value
        self.function_declaration()
        function_call = self.main_func()

        return MainFunction(name, function_call)

    def main_func(self):
        self.eat(ID)
        self.eat(ASSIGN)
        self.eat(QMARK)

        function_call = self.function_call()

        self.eat(QMARK)

        return function_call

    def include_library(self):
        self.eat(DOLLAR)
        self.eat(ID)
        self.eat(DOLLAR)
        library = self.current_token
        self.eat(ID)
        self.eat(SEMICOLON)

        return Library(library.value)

    def function(self):
        name = self.current_token.value
        self.function_declaration()
        func = self.func()
        return Function(name, func[0], func[1])

    def function_declaration(self):
        self.eat(ID)
        self.eat(COLON)
        self.eat(COLON)
        self.eat(TYPE)

        while self.current_token.type == LARROW:
            self.eat(LARROW)
            self.eat(TYPE)

    def func(self):
        self.eat(ID)
        parameters = []

        while self.current_token.type == ID:
            parameters.append(self.current_token.value)
            self.eat(ID)

        self.eat(ASSIGN)
        self.eat(QMARK)

        bodynode = self.function_body()
        self.eat(QMARK)

        return (parameters, bodynode)

    def regExpression(self):
        negate = []
        if self.current_token.type == EMARK:
            negate.append(True)
            self.eat(EMARK)
        else:
            negate.append(False)

        chain = []
        chain.append(self.bool())

        operators = []

        while self.current_token.type != SEMICOLON:
            if self.current_token.type == AND:
                operators.append(self.current_token.value)
                self.eat(AND)
            elif self.current_token.type == OR:
                operators.append(self.current_token.value)
                self.eat(OR)

            if self.current_token.type == EMARK:
                negate.append(True)
                self.eat(EMARK)
            else:
                negate.append(False)
            chain.append(self.bool())

        self.eat(SEMICOLON)

        return RegExpression(negate, chain, operators)

    def boolExpression(self):
        negate = []
        if self.current_token.type == EMARK:
            negate.append(True)
            self.eat(EMARK)
        else:
            negate.append(False)

        chain = []
        chain.append(self.bool())

        operators = []

        while self.current_token.type != FI and self.current_token.type != LOOP:
            if self.current_token.type == AND:
                operators.append(self.current_token.value)
                self.eat(AND)
            elif self.current_token.type == OR:
                operators.append(self.current_token.value)
                self.eat(OR)

            if self.current_token.type == EMARK:
                negate.append(True)
                self.eat(EMARK)
            else:
                negate.append(False)
            chain.append(self.bool())

        return BoolExpression(negate, chain, operators)

    @restorable
    def check_assginment(self):
        if self.current_token.type != ID:
            return False
        self.eat(ID)
        return self.current_token.type == ASSIGN

    def function_body(self):
        expressions = []

        while self.current_token.type != RETURN and self.current_token.type != QMARK:
            if self.current_token.type == IF:
                expressions.append(self.conditional())
            elif self.current_token.type == CHECK:
                expressions.append(self.loop())
            elif self.check_assginment():
                expressions.append(self.var_assignment())
            else:
                expressions.append(self.regExpression())

        if self.current_token.type == RETURN:
            self.eat(RETURN)
            return_expr = self.regExpression()
        else:
            return_expr = None

        return FunctionBody(expressions, return_expr)

    def function_call(self):
        self.eat(GRACCENT)
        function_name = self.current_token.value
        self.eat(ID)
        self.eat(GRACCENT)

        arguments = []
        self.eat(LBRACKET)
        while self.current_token.type != RBRACKET:
            arguments.append(self.expr())
            # if self.current_token.type == ID:
            #     arguments.append(self.expr())
            # elif self.current_token.type == GRACCENT:
            #     arguments.append(self.expr())
            # elif self.current_token.type == APOSTROPHE:
            #     arguments.append(self.expr())
                # self.eat(APOSTROPHE)
                # if self.current_token.value == "'":
                #     arguments.append(String(' '))
                # else:
                #     arguments.append(String(self.current_token.value))
                # if self.current_token.type == ID:
                #     self.eat(ID)
                # elif self.current_token.type == COMMA:
                #     self.eat(COMMA)
                # elif self.current_token.type == HASH:
                #     self.eat(HASH)
                # elif self.current_token.type == MUL:
                #     self.eat(MUL)
                # elif self.current_token.type == EMARK:
                #     self.eat(EMARK)
                # elif self.current_token.type == QMARK:
                #     self.eat(QMARK)
                # elif self.current_token.type == DOT:
                #     self.eat(DOT)
                # self.eat(APOSTROPHE)
            # else:
            #     arguments.append(Num(self.current_token))
            #     self.eat(INTEGER)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RBRACKET)

        return FunctionCall(function_name, arguments)

    def conditional(self):
        self.eat(IF)
        condition = self.boolExpression()
        self.eat(FI)

        self.eat(ID)
        then_part = None
        if self.current_token.type == IF:
            then_part = self.conditional()
        elif self.current_token.type == CHECK:
            then_part = self.loop()
        elif self.check_assginment():
            then_part = self.var_assignment()
        else:
            then_part = self.regExpression()

        self.eat(ID)
        self.eat(ELSE)

        else_part = None
        if self.current_token.type == IF:
            else_part = self.conditional()
        elif self.current_token.type == CHECK:
            else_part = self.loop()
        elif self.check_assginment():
            else_part = self.var_assignment()
        else:
            else_part = self.regExpression()

        self.eat(ID)

        return Conditional(condition, then_part, else_part)

    def loop(self):
        self.eat(CHECK)
        condition = self.boolExpression()

        self.eat(LOOP)
        loop_body = None
        if self.current_token.type == IF:
            loop_body = self.conditional()
        elif self.current_token.type == CHECK:
            loop_body = self.loop()
        elif self.check_assginment():
            loop_body = self.var_assignment()
        else:
            loop_body = self.regExpression()

        self.eat(POOL)
        last_part = None

        if self.current_token.type == DO:
            self.eat(DO)
            last_part = self.var_assignment()

        return Loop(condition, loop_body, last_part)

    def var_assignment(self):
        name = self.current_token.value
        self.eat(ID)
        self.eat(ASSIGN)

        function_call = self.function_call()

        self.eat(SEMICOLON)

        return VarAssignment(name, function_call)

    def var_declaration(self):
        name = self.current_token.value
        self.eat(ID)
        self.eat(INITIALIZE)
        value = self.bool()
        self.eat(SEMICOLON)

        return VarDecl(name, value)

    def factor(self):
        token = self.current_token

        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            self.eat(ID)
            if self.current_token.type == LANGLEBRACKET:
                self.eat(LANGLEBRACKET)
                index = self.expr()
                # self.eat(ID)
                self.eat(RANGLEBRACKET)
                return ListVar(token.value, index)
            return Var(token.value)
        elif token.type == GRACCENT:
            node = self.function_call()
            return node
        elif token.type == APOSTROPHE:
            self.eat(APOSTROPHE)
            value = self.current_token.value
            if value == "'":
                self.eat(APOSTROPHE)
                return String(' ')
            if self.current_token.type == ID:
                self.eat(ID)
            elif self.current_token.type == COMMA:
                self.eat(COMMA)
            elif self.current_token.type == HASH:
                self.eat(HASH)
            elif self.current_token.type == MUL:
                self.eat(MUL)
            elif self.current_token.type == EMARK:
                self.eat(EMARK)
            elif self.current_token.type == QMARK:
                self.eat(QMARK)
            elif self.current_token.type == DOT:
                self.eat(DOT)
            self.eat(APOSTROPHE)
            return String(value)
        elif token.type == LANGLEBRACKET:
            self.eat(LANGLEBRACKET)
            self.eat(RANGLEBRACKET)
            return Var('[]')

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV, REALDIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == REALDIV:
                self.eat(REALDIV)
            elif token.type == MOD:
                self.eat(MOD)
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):

        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def bool(self):
        node = self.expr()

        while self.current_token.type in (LESS, GREATHER, EQUAL, NOT_EQUAL, LESS_EQ, GREATHER_EQ):
            token = self.current_token
            if token.type == LESS:
                self.eat(LESS)
            elif token.type == GREATHER:
                self.eat(GREATHER)
            elif token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == NOT_EQUAL:
                self.eat(NOT_EQUAL)
            elif token.type == LESS_EQ:
                self.eat(LESS_EQ)
            elif token.type == GREATHER_EQ:
                self.eat(GREATHER_EQ)
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.expr())

        return node

    def parse(self):
       return self.program()