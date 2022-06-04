from tokenise import Token
from error import ParseError
from re import escape
from grammar import *

EMPTY = lambda: True
NOTEMPTY= lambda: False

def parseExp(exp: list[Token], prior:int = 0):
    ''' e :='(' e ')'
            var
            literal
            e binop e
            unop e
    '''
    if not exp:
        return {
            'empty' : lambda: False,
            }, prior
    
    start_brace, end_brace =\
            find(exp, lambda tok : tok.val == '\\(')[0],\
            findlast(exp, lambda tok : tok.val == '\\)')[0]
    
    if start_brace == 0 and end_brace == len(exp) - 1:
        return parseExp(exp[1:-1], prior + 1)

    idx, op = find(exp, lambda tok : tok.val in map(escape, OP))
    if idx == -1:

        if len(exp) == 1:
            match exp[0].kind:
                case 'VAR':
                    return {
                        'kind' : 'VAR',
                        'name' : exp[0].val,
                        'empty' : NOTEMPTY,
                    }, prior
            
            return {
                'kind' : exp[0].kind,
                'value' : exp[0].val,
                'empty' : NOTEMPTY,
            }, prior

    else:
        LHS = parseExp(exp[:idx], prior + 1)
        RHS = parseExp(exp[idx+1:], prior + 1)

        if op.val not in ('\\+', '\\-', '!') and LHS[0]['empty']():
            raise ParseError(f'Expected expression before operator {op.val}, line {op.line}')
        if RHS[0]['empty']():
            raise ParseError(f'Expected expression after operator {op.val}, line {op.line}')

        return {
            'kind' : 'OPR',
            'op' : op.val,
            'LHS' : LHS,
            'RHS' : RHS,
            'empty': NOTEMPTY,
        }, prior



def find(l, func):
    for i, v in enumerate(l):
        if func(v):
            return (i,v)

    return -1, None


def findlast(l, func):
    for i in range(1, len(l)+1):
        if func(l[len(l) - i]):
            return len(l)-i, l[i]
    
    return -1, None


if __name__ == '__main__':
    exp = [
        Token('NUMBER', 1, 0),
        Token('OPR', '\\+', 0),
        Token('BRACE', '\\(', 0),
        Token('BOOLEAN', True, 0),
        Token('OPR', '\&\&', 0),
        Token('BRACE', '\\(', 0),
        Token('BOOLEAN', True, 0),
        Token('BRACE', '\\)', 0),
        Token('BRACE', '\\)', 0)
    ]

    print(parseExp(exp))
