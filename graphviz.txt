digraph astgraph {
  node [shape=box, fontsize=12, fontname="Courier", height=.1];
  ranksep=.3;
  edge [arrowsize=.5]
  
  
python getastdot.py {} > {} && dot -Tpng -o {} {}


RESERVED_KEYWORDS = {
    'int': Token(TYPE, 'int'),
    'if': Token(IF, 'if'),
    'else': Token(ELSE, 'else'),
    'return': Token(RETURN, 'return'),
}

from functools import wraps
import pickle

def restorable(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        state = pickle.dumps(self.__dict__)
        result = fn(self, *args, **kwargs)
        self.__dict__ = pickle.loads(state)
        return result
    return wrapper


program                     : declarations

declarations                : (include_library | function_declaration | var_declaration_list)*

include_library             : HASH ID<'include'> LESS_THAN ID DOT ID<'h'> GREATER_THAN

function_declaration        : type_spec ID LPAREN parameters RPAREN function_body

function_body               : LBRACKET statement_list RBRACKET

var_declaration_list        : type_spec var var_initialization (COMMA var var_initialization)* SEMICOLON

var_initialization          : (ASSIGN expr)?

parameters                  : empty
							| param (COMMA param)*

param                       : type_spec variable

block                       : LBRACKET statement_list RBRACKET

statement_list              : var_declaration_list
							| statement
							| statement statement_list

statement                   : assignment_statement
							| function_call SEMICOLON
							| if_statement
							| return_statement
							| empty

assignment_statement        : variable ASSIGN expr SEMICOLON

return_statement            : RETURN expr SEMICOLON

if_statement                : IF LPAREN expr RPAREN stmt_body (ELSE stmt_body)?

term                        : factor ((MUL | DIV) factor)*

type_spec                   : TYPE

variable                    : ID

expr                        : term ((PLUS | MINUS) term)*

term                        : factor ((MUL | DIV) factor)*

factor                      : PLUS factor
							| MINUS factor
							| AMPERSAND variable
							| INT_NUMBER
							| LPAREN expr RPAREN
							| variable
							| function_call

function_call               : ID LPAREN (expr | STRING)* RPAREN