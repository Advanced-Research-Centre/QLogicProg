from sly import Parser
from qlexer import QLexer

class QParser(Parser):
    # Get the token list from the lexer (required)
    tokens = QLexer.tokens

    d = dict()

    # Grammar rules and actions
    @_('COUNTS COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        if p[4] not in self.d:
            self.d[p[4]] = {}
        self.d[p[4]][p[2]] = p[0]   
    
    @_('PROG')
    def expr(self, p):
        print(f'Executing program {p[0]}')

    @_("expr expr")
    def expr(self, p):
        return [p[0], p[1]]

    @_('QUERY COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        print(self.d[p[4]][p[2]]) 

if __name__ == '__main__':
    lexer = QLexer()
    parser = QParser()
    
    f = open("qprog.qlp","r")
    text = f.read()
    # print(text)
    # for tok in lexer.tokenize(text):
    #     print('type=%r, value=%r' % (tok.type, tok.value))
    # exit()

    # while True:
    # try:

        
    print(text)
    result = parser.parse(lexer.tokenize(text))
        # print(result)
    # except EOFError:
        # break