import argparse
import textwrap
import sys

from interpreter.lexical_analysis.lexer import Lexer
from interpreter.lexical_analysis.tokenType import *
from interpreter.syntax_analysis.interpreter import NodeVisitor
from interpreter.syntax_analysis.parser import Parser

class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.nodecount = 1
        # self.dot_heder = [textwrap.dedent("""
        #     digraph astgraph {
        #         node [shape=box, fontsize=12, fontname="Courier", height=.1];
        #         ranksep=.3;
        #         edge [arrowsize=.5]
        # """)]
        self.dot_heder = ['']
        self.dot_body = []
        self.dot_footer = ['']
        self.tabcounter = 0

    def visit_Program(self, node):
        # s = 'node{} [label="Program"]\n'.format(self.nodecount)
        # node.num = self.nodecount
        # self.nodecount += 1
        # self.dot_body.append(s)

        for child in node.children:
            self.visit(child)
            # s = 'node{} -> node{}\n'.format(node.num, child.num)
            # self.dot_body.append(s)

    def visit_Library(self, node):
        # s = 'node{} [label="Library: {}"]\n'.format(self.nodecount, node.library)
        s = 'import ' + node.library + '\n'
        # node.num = self.nodecount
        # self.nodecount += 1
        self.dot_body.append(s)

    def visit_VarDecl(self, node):
        # s = 'node{} [label="VarDecl"]\n'.format(self.nodecount)
        # s = str(node.name) + ' = ' + str(node.value) + '\n'
        # node.num = self.nodecount
        # self.nodecount += 1
        # self.dot_body.append(s)

        self.dot_body.append(str(node.name) + ' = ')
        self.visit(node.value)
        self.dot_body.append('\n')
        # s = 'node{} -> node{}\n'.format(node.num, node.type_node.num)
        # self.dot_body.append(s)
        #
        # self.visit(node.var_node)
        # s = 'node{} -> node{}\n'.format(node.num, node.var_node.num)
        # self.dot_body.append(s)

    def visit_VarAssignment(self, node):
        for i in range(self.tabcounter):
            self.dot_body.append('\t')
        self.dot_body.append(node.name + ' = ')
        self.visit(node.function_call)

    def visit_Assign(self, node):
        s = 'node{} [label="Assign"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.var_node)
        s = 'node{} -> node{}\n'.format(node.num, node.var_node.num)
        self.dot_body.append(s)

        self.visit(node.expr)
        s = 'node{} -> node{}\n'.format(node.num, node.expr.num)
        self.dot_body.append(s)

    def visit_Function(self, node):
        s = 'def ' + node.name + '('
        for i in range(len(node.parameters) - 1):
            s += node.parameters[i] + ','
        if len(node.parameters) > 0:
            s += node.parameters[len(node.parameters) - 1] + '):\n'
        else:
            s += '):\n'

        self.dot_body.append(s)
        self.visit(node.bodynode)
        self.dot_body.append('\n')
        # self.dot_body.append(s)

    def visit_FunctionBody(self, node):
        self.tabcounter += 1
        for child in node.expressions:
            self.visit(child)
            self.dot_body.append('\n')

        self.tabcounter -= 1

        if node.ret_statement is not None:
            self.dot_body.append('\treturn ')
            self.visit(node.ret_statement)
            self.dot_body.append('\n')

    def visit_RegExpression(self, node):
        c = 0
        for i in range(self.tabcounter):
            self.dot_body.append('\t')
        for bool in node.chain:
            if node.negates[c]:
                self.dot_body.append('not ')
            self.visit(bool)

            if c < len(node.chain) - 1:
                self.dot_body.append(' ' + str(node.operators[c]) + ' ')

            c += 1

    def visit_BoolExpression(self, node):
        c = 0
        for bool in node.chain:
            if node.negates[c]:
                self.dot_body.append('not ')
            self.visit(bool)

            if c < len(node.chain) - 1:
                self.dot_body.append(' ' + str(node.operators[c]) + ' ')

            c += 1

    def visit_Conditional(self, node):
        for i in range(self.tabcounter):
            self.dot_body.append('\t')
        self.dot_body.append('if ')
        self.visit(node.condition)
        self.dot_body.append(':\n')

        self.tabcounter += 1
        self.visit(node.then_part)

        self.dot_body.append('\n')
        for i in range(self.tabcounter - 1):
            self.dot_body.append('\t')
        self.dot_body.append('else:\n')
        self.visit(node.else_part)

        self.tabcounter -= 1

    def visit_Loop(self, node):
        for i in range(self.tabcounter):
            self.dot_body.append('\t')
        self.dot_body.append('while ')
        self.visit(node.condition)
        self.dot_body.append(':\n')

        self.tabcounter += 1
        self.visit(node.loop_body)
        self.dot_body.append('\n')
        if node.last_part is not None:
            self.visit(node.last_part)
            self.dot_body.append('\n')

        self.tabcounter -= 1

    def visit_FunDecl(self, node):
        s = 'node{} [label="FunDecl: {}"]\n'.format(self.nodecount, node.fun_name)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = 'node{} -> node{}\n'.format(node.num, node.type_node.num)
        self.dot_body.append(s)

        self.visit(node.args_node)
        s = 'node{} -> node{}\n'.format(node.num, node.args_node.num)
        self.dot_body.append(s)

        self.visit(node.stmts_node)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts_node.num)
        self.dot_body.append(s)

    def visit_Args(self, node):
        s = 'node{} [label="Args"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.args:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_Stmts(self, node):
        s = 'node{} [label="Stmts"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.stmts:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

    def visit_Type(self, node):
        s = 'node{} [label="Type: {}"]\n'.format(self.nodecount, node.type)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_FunctionCall(self, node):
        self.dot_body.append(node.function_name + '(')
        c = 0
        for arg in node.arguments:
            self.visit(arg)
            if c < len(node.arguments) - 1:
                self.dot_body.append(',')
            c += 1
        self.dot_body.append(')')

    def visit_Var(self, node):
        # s = 'node{} [label="Var: {}"]\n'.format(self.nodecount, node.var)
        # node.num = self.nodecount
        # self.nodecount += 1
        self.dot_body.append(node.var)


    def visit_BinOp(self, node):
        # s = 'node{} [label="{}"]\n'.format(self.nodecount, node.op)
        # node.num = self.nodecount
        # self.nodecount += 1
        # self.dot_body.append(s)

        self.visit(node.left)
        # s = 'node{} -> node{}\n'.format(node.num, node.left.num)
        # self.dot_body.append(s)
        self.dot_body.append(' ' + str(node.op) + ' ')

        self.visit(node.right)
        # s = 'node{} -> node{}\n'.format(node.num, node.right.num)
        # self.dot_body.append(s)

    def visit_Num(self, node):
        # s = 'node{} [label="{}"]\n'.format(self.nodecount, node.value)
        # node.num = self.nodecount
        # self.nodecount += 1
        s = str(node.value)
        self.dot_body.append(s)

    def visit_String(self, node):
        self.dot_body.append("'" + node.value + "'")

    def visit_If(self, node):
        s = 'node{} [label="If"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.cond_node)
        s = 'node{} -> node{}\n'.format(node.num, node.cond_node.num)
        self.dot_body.append(s)

        self.visit(node.body_node)
        s = 'node{} -> node{}\n'.format(node.num, node.body_node.num)
        self.dot_body.append(s)

        if node.else_node is not None:
            self.visit(node.else_node)
            s = 'node{} -> node{}\n'.format(node.num, node.else_node.num)
            self.dot_body.append(s)

    def visit_Cond(self, node):
        s = 'node{} [label="Cond"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        self.visit(node.cond)
        s = 'node{} -> node{}\n'.format(node.num, node.cond.num)
        self.dot_body.append(s)

    def visit_Body(self, node):
        s = 'node{} [label="Body"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_Else(self, node):
        s = 'node{} [label="Else"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

    def visit_For(self, node):
        s = 'node{} [label="For"]\n'.format(self.nodecount)
        node.num = self.nodecount
        self.nodecount += 1
        self.dot_body.append(s)

        for child in node.var_decl:
            self.visit(child)
            s = 'node{} -> node{}\n'.format(node.num, child.num)
            self.dot_body.append(s)

        # self.visit(node.var_decl)
        # s = 'node{} -> node{}\n'.format(node.num, node.var_decl.num)
        # self.dot_body.append(s)

        self.visit(node.cond)
        s = 'node{} -> node{}\n'.format(node.num, node.cond.num)
        self.dot_body.append(s)

        self.visit(node.stmts)
        s = 'node{} -> node{}\n'.format(node.num, node.stmts.num)
        self.dot_body.append(s)

        self.visit(node.body_stmts)
        s = 'node{} -> node{}\n'.format(node.num, node.body_stmts.num)
        self.dot_body.append(s)

    def genDot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_heder + self.dot_body + self.dot_footer)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('fname')

    args = argparser.parse_args()
    fname = args.fname

    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.genDot()

    print(content)



if __name__ == '__main__':
    main()
