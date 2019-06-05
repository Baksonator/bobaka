from interpreter.lexical_analysis.token import Token
from interpreter.lexical_analysis.tokenType import *


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Neocekivani karakter {} '.format(self.current_char))

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        number = ""
        while (self.current_char is not None and self.current_char.isdigit()):
            number += self.current_char
            self.advance()
        return int(number)

    def _id(self):
        result = ""
        while (self.current_char is not None and self.current_char.isalnum()):
            result += self.current_char
            self.advance()

        if result == 'Num' or result == 'Char' or result == 'Bool' or result == 'String' or result == 'IO':
            return Token(TYPE, result)
        elif result == 'return':
            return Token(RETURN, result)
        elif result == 'if':
            return Token(IF, result)
        elif result == 'fi':
            return Token(FI, result)
        elif result == 'loop':
            return Token(LOOP, result)
        elif result == 'pool':
            return Token(POOL, result)
        elif result == 'do':
            return Token(DO, result)
        elif result == 'else':
            return Token(ELSE, result)
        elif result == 'for':
            return Token(FOR, result)
        elif result == 'and':
            return Token(AND, result)
        elif result == 'or':
            return Token(OR, result)
        elif result == 'check':
            return Token(CHECK, result)
        else:
            return Token(ID, result)


    def skip_whitespace(self):
        while (self.current_char is not None and self.current_char.isspace()):
            self.advance()


    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            # print('------')
            # print(self.current_char)
            # print('******')

            if self.current_char is None:
                return Token(EOF, None)

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '`':
                self.advance()
                return Token(GRACCENT, '`')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == "'":
                self.advance()
                return Token(APOSTROPHE, "'")

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACKET, '}')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')

            if self.current_char == '$':
                self.advance()
                return Token(DOLLAR, '$')

            if self.current_char == '?':
                self.advance()
                return Token(QMARK, '?')

            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    return Token(LARROW, '->')
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    return Token(REALDIV, '//')
                return Token(DIV, '/')

            if self.current_char == '[':
                self.advance()
                if self.current_char is not None and self.current_char.isalnum():
                    result = ""
                    while (self.current_char is not None and self.current_char.isalnum()):
                        result += self.current_char
                        self.advance()
                    self.advance()
                    return Token(TYPE, result)
                else:
                    return Token(LANGLEBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return Token(RANGLEBRACKET, ']')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESS_EQ, '<=')
                if self.current_char == '<':
                    self.advance()
                    self.advance()
                    return Token(INITIALIZE, '<<=')
                return Token(LESS, '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREATHER_EQ, '>=')
                return Token(GREATHER, '>')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUAL, '==')
                return Token(ASSIGN, '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NOT_EQUAL, '!=')
                return Token(EMARK, '!')

            self.error()

        return Token(EOF, None)