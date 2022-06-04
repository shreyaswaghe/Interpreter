KEYWORDS  = {
    'let',
    'const',
    'glbl',
    'if',
    'else',
    'func',
    'while',
    'for',
    'do',
    'true',
    'false',
    '__EOF'
}

OPEN_BRACES = {
    '{'
    '['
    '('
}

CLOSE_BRACES = {
    '}', ']', ')'
}
ARITH_OP = {
    '+',
    '-',
    '/',
    '*',
    '%',
    '//',
    '^'
}

REL_OP = {
    '<','<=',
    '>', '>='
}

LOG_OP = {
    '||', '&&'
}

EQ_OP = {
    '==', '!='
}

ASSN_OP = {
    '='
}

OP = ARITH_OP\
    .union(REL_OP)\
    .union(LOG_OP)\
    .union(EQ_OP)\
    .union(ASSN_OP)