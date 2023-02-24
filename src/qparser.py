from sly import Parser
from qlexer import QLexer

class QParser(Parser):
    # Get the token list from the lexer
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
        print(f'Count of {p[2]} :', self.d[p[4]][p[2]])
    
    @_('QUERY COUNTOF FORALL ADJOF NOUN')
    def expr(self, p):
        tot_count = 0
        for k in self.d[p[4]].keys():
            print(k, self.d[p[4]][k])
            tot_count += int(self.d[p[4]][k])
        print(tot_count)

    @_('QUERY COUNTOF FORALL ADJOF FORALL')
    def expr(self, p):
        tot_count = 0
        for k1 in self.d.keys():
            semi_tot_count = 0
            for k2 in self.d[k1].keys():
                semi_tot_count += int(self.d[k1][k2])
            tot_count += semi_tot_count
        tot_count = str(tot_count)
        print(f'total Count for all Adj and Noun', tot_count)

    @_('FORALL COUNTOF QUERY ADJOF NOUN')
    def expr(self, p):
        list_adj = []
        for k in self.d[p[4]].keys():
            list_adj.append(k)
        print(list_adj)
    
    @_('ADD COUNTS COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        self.d[p[5]][p[3]] = str(int(self.d[p[5]][p[3]])+int(p[1]))
        print(self.d)


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