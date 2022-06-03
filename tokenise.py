from typing import Any, NamedTuple
from error import ParseError
from regex import RX_DEF
import re

class Token(NamedTuple):
    kind : str
    val : Any
    line : int

    def __str__(self):
        return f"({self.kind},{self.val})"

    def __repr__(self):
        return self.__str__()

def tokeniser(line_gen):
    line_num = 1
    token_rx = re.compile('|'.join(['(?P<%s>%s)' %pair for pair in RX_DEF.items()]))
    while True:
        try:
            line:str = next(line_gen)
            line = line.strip(' \t')
        except StopIteration:
            break

        if not len(line):
            line = '\n'

        for match in token_rx.finditer(line):
            kind = match.lastgroup.upper()
            value = match.group()
            
            match kind:
                case 'NUMBER':
                    value = float(value) if '.' in value else int(value)
                case 'WSP':
                    continue
                case 'ENDL':
                    if value == '\\n':
                        line_num += 1
                case 'BOOLEAN':
                    value = True if value == 'true' else False
                case 'UNKNOWN':
                    raise ParseError(f"Unknown token encountered {value}, line {line_num}")  

            yield Token(kind, value, line_num)


if __name__ == '__main__':
    pass
