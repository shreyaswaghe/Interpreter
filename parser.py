from tokenise import Token
from error import ParseError
from re import escape
from grammar import *

def parseExp(exp: list[Token], prior:int = 0):
    ''' e :='(' e ')'
            var
            literal
            e binop e
            unop e
    '''
    if not exp:
        return {}
    
    start_brace, end_brace =\
            find(exp, lambda tok : tok.val == '\\(')[0],\
            find(exp, lambda tok : tok.val == '\\)')[0]
    
    if start_brace == 0 and end_brace == len(exp) - 1:
        return parseExp(exp[1:-1], prior + 1)

    idx, op = find(exp, lambda tok : tok.val in map(escape, OP))
    if idx == -1:

        if len(exp) == 1:
            match exp[0].kind:
                case 'VAR':
                    return {
                        'kind' : 'VAR',
                        'name' : exp[0].val
                    }, prior
            
            return {
                'kind' : exp[0].kind,
                'value' : exp[0].val
            }, prior

    else : 
        return {
            'kind' : 'OPR',
            'op' : op.val,
            'LHS' : parseExp(exp[:idx]),
            'RHS' : parseExp(exp[idx+1:])
        }



def find(l, func) -> tuple[int, Token]:
    for i, v in enumerate(l):
        if func(v):
            return i, v
        
    return -1, None


if __name__ == '__main__':
    exp = [
        Token('NUMBER', 1, 0),
        Token('OPR', '\\+', 0),
        Token('BRACE', '\\(', 0),
        Token('BOOLEAN', True, 0),
        Token('BRACE', '\\)', 0)
    ]

    print(parseExp(exp))
