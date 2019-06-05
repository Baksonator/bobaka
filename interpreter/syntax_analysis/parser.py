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
        # self.eat(MINUS)
        self.eat(LARROW)

        while self.current_token.type == ID:
            if self.current_token.value == 'main':
                pass
            else:
                declarations.append(self.function())

        return Program(declarations)

    @restorable
    def check_function(self):
        self.eat(TYPE)
        self.eat(ID)
        return self.current_token.type == LPAREN

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
            if self.current_token.type == ID:
                arguments.append(self.expr())
            elif self.current_token.type == GRACCENT:
                arguments.append(self.function_call())
            elif self.current_token.type == APOSTROPHE:
                self.eat(APOSTROPHE)
                if self.current_token.value == "'":
                    arguments.append(String(' '))
                else:
                    arguments.append(String(self.current_token.value))
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
            else:
                arguments.append(Num(self.current_token))
                print(self.current_token.value, sys.stdout)
                self.eat(INTEGER)
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

    def function_declarations(self):
        type_node = Type(self.current_token.value)
        self.eat(TYPE)

        fun_name = self.current_token.value
        self.eat(ID)

        self.eat(LPAREN)
        args_node = Args(self.argument_list())
        self.eat(RPAREN)

        self.eat(LBRACKET)
        stmts_node = Stmts(self.statement_list())
        self.eat(RBRACKET)

        return FunDecl(type_node=type_node, fun_name=fun_name, args_node=args_node, stmts_node=stmts_node)

    def argument_list(self):
        params = []

        while self.current_token.type != RPAREN:
            type_node = Type(self.current_token.value)
            self.eat(TYPE)

            var_node = Var(self.current_token.value)
            self.eat(ID)

            params.append(VarDecl(type_node, var_node))

            if self.current_token.type == COMMA:
                self.eat(COMMA)


        return params

    def statement_list(self):
        statements = []

        while self.current_token.type != RBRACKET:
            if self.current_token.type == IF:
                self.eat(IF)
                self.eat(LPAREN)
                cond = Cond(self.expr())
                self.eat(RPAREN)

                self.eat(LBRACKET)
                stamts_node = Stmts(self.statement_list())
                self.eat(RBRACKET)

                if self.current_token.type == ELSE:
                    self.eat(ELSE)

                    self.eat(LBRACKET)
                    else_stmts_node = Stmts(self.statement_list())
                    self.eat(RBRACKET)

                    if_node = If(cond, stamts_node, else_stmts_node)
                    statements.append(if_node)
                else:
                    if_node = If(cond, stamts_node)
                    statements.append(if_node)
            elif self.current_token.type == TYPE:
                statements.extend(self.var_declaration_list())
            elif self.current_token.type == FOR:
                self.eat(FOR)
                self.eat(LPAREN)
                for_decl = self.var_declaration_list()
                # self.eat(SEMICOLON)
                cond = Cond(self.expr())
                self.eat(SEMICOLON)
                stmts_node = Cond(self.expr())
                self.eat(RPAREN)

                self.eat(LBRACKET)
                body_stmts = Stmts(self.statement_list())
                self.eat(RBRACKET)

                for_node = For(for_decl, cond, stmts_node, body_stmts)
                statements.append(for_node)

        return statements



    def var_declaration_list(self):

        declarations = []

        type_node = Type(self.current_token.value)
        self.eat(TYPE)
        var_node = Var(self.current_token.value)
        self.eat(ID)

        declarations.extend(self.var_declaration(type_node, var_node))

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_node = Var(self.current_token.value)
            self.eat(ID)

            declarations.extend(self.var_declaration(type_node, var_node))

        self.eat(SEMICOLON)

        return declarations

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
        # result = True
        node = self.expr()

        while self.current_token.type in (LESS, GREATHER, EQUAL, NOT_EQUAL, LESS_EQ, GREATHER_EQ):
            token = self.current_token
            if token.type == LESS:
                self.eat(LESS)
                # right = self.expr()
                # if not (left < right):
                #     result = False
                # left = right
            elif token.type == GREATHER:
                self.eat(GREATHER)
                # right = self.expr()
                # if not (left > right):
                #     result = False
                # left = right
            elif token.type == EQUAL:
                self.eat(EQUAL)
                # right = self.expr()
                # if not (left == right):
                #     result = False
                # left = right
            elif token.type == NOT_EQUAL:
                self.eat(NOT_EQUAL)
                # right = self.expr()
                # if not (left != right):
                #     result = False
                # left = right
            elif token.type == LESS_EQ:
                self.eat(LESS_EQ)
                # right = self.expr()
                # if not (left <= right):
                #     result = False
                # left = right
            elif token.type == GREATHER_EQ:
                self.eat(GREATHER_EQ)
                # right = self.expr()
                # if not (left >= right):
                #     result = False
                # left = right
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.expr())

        return node

    def parse(self):
       return self.program()