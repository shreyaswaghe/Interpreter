from grammar import *
from re import escape
KEYWORD_PATTERN = '|'.join(KEYWORDS)

OP_PATTERN = '|'.join(map(
    escape,
    OP
))

print(OP_PATTERN)

BRACE_PATTERN = '|'.join(map(
    escape,
    BRACES
))

RX_DEF = {
    'NUMBER' : r'\d+(\.\d*)?|\d*\.\d+',
    'BOOLEAN' : 'true|false',
    'OPR' : OP_PATTERN,
    'ENDL' : r';|\n|__EOF',
    'KEYW' : KEYWORD_PATTERN,
    'VAR' : r'[a-zA-Z_0-9]+',
    'OPEN_BRACES' : '[\{\(\[]',
    'CLOSE_BRACES' : '[\}\)\]]',
    'STR' : r'[\"]\w*[\"]|[\']\w*[\']',
    'WSP' : r' |\t',
    'CONTINUE' : r'\\',
    'UNKNOWN' : r'.'
}
'''
TOKEN_RX = {
    'number': r'\d+(\.\d*)?|\d*\.\d+',
    'boolean': 'true|false',
    'string' : '[\"]\w*[\"]|[\']\w*[\']',
    'operator' : OPERATOR_PATTERN,
    'brace': '[\{\}\(\)\[\]]',
    'endl': r';|\n|EOF',
    'decl' : '|'.join(DECL),
    'keyw' : KEYWORD_PATTERN,
    'var': r'[a-zA-Z0-9_$]+',
    'text': r'[\w]+',
    'whitesp':' |\t',
    'unknown': r'.', 
}
'''