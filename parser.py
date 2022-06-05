from tokenise import Token
from assets.error import ParseError
from re import escape
from assets.grammar import *

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
            raise ParseError('I have no idea what you\'re even trying to do')

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

'''
def buildStmtTree(tokeniser):
    token: Token
    stmt = []
    while True:
        try:
            token = next(tokeniser)
        except StopIteration:
            break

        match token.kind:

            case 'KEYW':
                keyw(token, tokeniser)


def condnBuild(token: Token, tokeniser):
    assert token.val == 'if'
    Cond = Else = Then = []
    cond = other = then = 0
    currentstate = [cond, then, other]
    # require { } at this point

    cmpd_hier = brace_hier = 0
    while True:
        try:
            token = next(tokeniser)
        except StopIteration:
            raise ParseError("Possible incomplete conditional, line {token.line}")

        if token.val == '\\n': continue

        if token.val == '\\(': 
            if not cond and brace_hier == 0: cond = 1

            brace_hier += 1

        if token.val == '\\)':
            brace_hier -= 1

            if cond and brace_hier == 0:
                cond = 2

        if token.val == '\\{':
            if currentstate == [2,0,0] and cmpd_hier == 2:
                then = 1

            cmpd_hier += 1

        match currentstate:
            case [1,0,0]:
                Cond.append(token)
            case [2,1,0]:
                Then.append(buildStmtTree(tokeniser))


        if currentstate == [1,0,0]:
            Cond.append(token)
        elif currentstate =
'''       

def buildstmt(tokeniser):
    token: Token|None = None
    stmt = []
    exp_hier = cmpd_hier = 0
    while True:
        try:
            token = next(tokeniser)
        except StopIteration:
            break

        match token.val:
            case '\\n':
                if exp_hier == 0:
                    yield stmt
                    stmt = []
                continue

            case ';':
                yield stmt
                stmt = []
                continue

            case '\\(':
                exp_hier += 1

            case '\\)':
                exp_hier -= 1
                if exp_hier == 0:
                    yield stmt
                    stmt = []
                    continue

            case '\\{':
                cmpd_hier += 1
                yield f'DEPTH {cmpd_hier}'
                continue
            
            case '\\}':
                cmpd_hier -= 1
                yield f'DEPTH {cmpd_hier}'
                continue

        stmt.append(token)
                
        
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
    def getgenerator(list):
        for _ in list:
            yield _

    exp = [
        Token('NUMBER', 1, 0),
        Token('OPR', '\\+', 0),
        Token('BRACE', '\\(', 0),
        Token('BOOLEAN', True, 0),
        Token('OPR', '\&\&', 0),
        Token('BRACE', '\\(', 0),
        Token('BOOLEAN', True, 0),
        Token('BRACE', '\\)', 0),
        Token('ENDL', '\\n', 0),
        Token('KEYW', 'let', 0),
        Token('VAR', 'a', 0),
        Token('OPR', '=', 0),
        Token('NUMBER', 34, 0),
        Token('ENDL', '\\n', 0),
        Token('BRACE', '\\)', 0)
    ]

    for _ in buildstmt(getgenerator(exp)):
        print(_)
