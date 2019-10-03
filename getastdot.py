import argparse
import textwrap
import sys

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import NodeVisitor
from interpreter.syntax_analysis.parser import Parser

built_in_functions = ['inputint', 'split', 'random', 'sqrt', 'append', 'isChar', 'isDigit', 'putStr', 'toCaps', 'subStr',
                      'readFile', 'toLower']
variables = []

class PythonTranslator(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.nodecount = 1
        self.header = ['']
        self.body = []
        self.footer = ['\nmain()']
        self.tabcounter = 0

    def visit_Program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Library(self, node):
        s = 'import ' + node.library + '\n'
        self.body.append(s)

    def visit_VarDecl(self, node):
        variables.append(node.name)
        self.body.append(str(node.name) + ' = ')
        self.visit(node.value)
        self.body.append('\n')

    def visit_VarAssignment(self, node):
        for i in range(self.tabcounter):
            self.body.append('\t')
        self.body.append(node.name + ' = ')
        self.visit(node.function_call)

    def visit_Function(self, node):
        s = 'def ' + node.name + '('
        for i in range(len(node.parameters) - 1):
            s += node.parameters[i] + ','
        if len(node.parameters) > 0:
            s += node.parameters[len(node.parameters) - 1] + '):\n'
        else:
            s += '):\n'

        self.body.append(s)
        self.visit(node.bodynode)
        self.body.append('\n')

    def visit_FunctionBody(self, node):
        self.tabcounter += 1
        for variable in variables:
            for i in range(self.tabcounter):
                self.body.append('\t')
            self.body.append('global ' + variable + '\n')
        for child in node.expressions:
            self.visit(child)
            self.body.append('\n')

        self.tabcounter -= 1

        if node.ret_statement is not None:
            self.body.append('\treturn ')
            self.visit(node.ret_statement)
            self.body.append('\n')

    def visit_RegExpression(self, node):
        c = 0
        for i in range(self.tabcounter):
            self.body.append('\t')
        for bool in node.chain:
            if node.negates[c]:
                self.body.append('not ')
            self.visit(bool)

            if c < len(node.chain) - 1:
                self.body.append(' ' + str(node.operators[c]) + ' ')

            c += 1

    def visit_BoolExpression(self, node):
        c = 0
        for bool in node.chain:
            if node.negates[c]:
                self.body.append('not ')
            self.visit(bool)

            if c < len(node.chain) - 1:
                self.body.append(' ' + str(node.operators[c]) + ' ')

            c += 1

    def visit_Conditional(self, node):
        for i in range(self.tabcounter):
            self.body.append('\t')
        self.body.append('if ')
        self.visit(node.condition)
        self.body.append(':\n')

        self.tabcounter += 1
        self.visit(node.then_part)

        self.body.append('\n')
        for i in range(self.tabcounter - 1):
            self.body.append('\t')
        self.body.append('else:\n')
        self.visit(node.else_part)

        self.tabcounter -= 1

    def visit_Loop(self, node):
        for i in range(self.tabcounter):
            self.body.append('\t')
        self.body.append('while ')
        self.visit(node.condition)
        self.body.append(':\n')

        self.tabcounter += 1
        self.visit(node.loop_body)
        self.body.append('\n')
        if node.last_part is not None:
            self.visit(node.last_part)
            self.body.append('\n')

        self.tabcounter -= 1

    def visit_MainFunction(self, node):
        s = 'def ' + node.name + '():\n\t'
        self.body.append(s)
        self.visit(node.function_call)
        self.body.append('\n')

    def visit_FunctionCall(self, node):
        if node.function_name in built_in_functions:
            if node.function_name == 'inputint':
                self.body.append('int(')
                self.body.append('input' + '(')
                c = 0
                for arg in node.arguments:
                    self.visit(arg)
                    if c < len(node.arguments) - 1:
                        self.body.append(',')
                    c += 1
                self.body.append('))')
            elif node.function_name == 'split':
                self.visit(node.arguments[0])
                self.body.append('.split()')
            elif node.function_name == 'random':
                self.body.append('random.randrange(')
                c = 0
                for arg in node.arguments:
                    self.visit(arg)
                    if c < len(node.arguments) - 1:
                        self.body.append(',')
                    c += 1
                self.body.append(')')
            elif node.function_name == 'sqrt':
                self.body.append('math.sqrt(')
                c = 0
                for arg in node.arguments:
                    self.visit(arg)
                    if c < len(node.arguments) - 1:
                        self.body.append(',')
                    c += 1
                self.body.append(')')
            elif node.function_name == 'append':
                self.visit(node.arguments[0])
                self.body.append('.append(')
                self.visit(node.arguments[1])
                self.body.append(')')
            elif node.function_name == 'isChar':
                self.visit(node.arguments[0])
                self.body.append('.isalpha()')
            elif node.function_name == 'isDigit':
                self.visit(node.arguments[0])
                self.body.append('.isdigit()')
            elif node.function_name == 'putStr':
                self.body.append('print(')
                c = 0
                for arg in node.arguments:
                    self.visit(arg)
                    if c < len(node.arguments) - 1:
                        self.body.append(',')
                    c += 1
                self.body.append(", end='')")
            elif node.function_name == 'toCaps':
                self.visit(node.arguments[0])
                self.body.append('.upper()')
            elif node.function_name == 'subStr':
                self.visit(node.arguments[2])
                self.body.append('[')
                self.visit(node.arguments[0])
                self.body.append(':')
                self.visit(node.arguments[1])
                self.body.append(']')
            elif node.function_name == 'readFile':
                self.body.append('open(')
                self.visit(node.arguments[0])
                self.body.append(', "r").read()')
            elif node.function_name == 'toLower':
                self.visit(node.arguments[0])
                self.body.append('.lower()')
        else:
            self.body.append(node.function_name + '(')
            c = 0
            for arg in node.arguments:
                self.visit(arg)
                if c < len(node.arguments) - 1:
                    self.body.append(',')
                c += 1
            self.body.append(')')

    def visit_Var(self, node):
        self.body.append(node.var)

    def visit_ListVar(self, node):
        self.body.append(node.list_name + '[')
        self.visit(node.index)
        self.body.append(']')

    def visit_BinOp(self, node):
        self.body.append('(')
        self.visit(node.left)
        self.body.append(' ' + str(node.op) + ' ')

        self.visit(node.right)
        self.body.append(')')

    def visit_Num(self, node):
        s = str(node.value)
        self.body.append(s)

    def visit_String(self, node):
        self.body.append("'" + node.value + "'")

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.header + self.body + self.footer)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fname')

    args = argparser.parse_args()
    fname = args.fname

    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    py_translator = PythonTranslator(parser)
    content = py_translator.genDot()

    print(content)



if __name__ == '__main__':
    main()
