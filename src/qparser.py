from sly import Parser
from src.qlexer import QLexer

class QParser(Parser):
    
    states = dict()
    processes = dict()

    # Get the token list from the lexer
    tokens = QLexer.tokens

    # Grammar rules and actions

    @_("expr expr")
    def expr(self, p):
        return [p[0], p[1]]

    @_('FRAME')
    def expr(self, p):
        print('\nExecuting frame :', p[0][2:])
      
    @_('COUNTS COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        if p[4][2:] not in self.states:
            self.states[p[4][2:]] = {}
        self.states[p[4][2:]][p[2][2:]] = int(p[0])
    
    @_('QUERY COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        print('Total Counts of',p[4][2:],'for',p[2][2:],':', self.states[p[4][2:]][p[2][2:]])
    
    @_('QUERY COUNTOF FORALL ADJOF NOUN')
    def expr(self, p):
        tot_count = 0
        for k in self.states[p[4][2:]].keys():
            tot_count += self.states[p[4][2:]][k]
        print('Total Counts of all Adjs for',p[4][2:],':',tot_count)

    @_('QUERY COUNTOF FORALL ADJOF FORALL')
    def expr(self, p):
        tot_count = 0
        for k1 in self.states.keys():
            semi_tot_count = 0
            for k2 in self.states[k1].keys():
                semi_tot_count += int(self.states[k1][k2])
            tot_count += semi_tot_count
        tot_count = str(tot_count)
        print('Total Counts of all Adjs for all Nouns :', tot_count)

    @_('FORALL COUNTOF QUERY ADJOF NOUN')
    def expr(self, p):
        list_adj = []
        for k in self.states[p[4][2:]].keys():
            list_adj.append(k)
        print('All (non-zero Count) Adjs for',p[4][2:],':',list_adj)
        
    @_('VERB NOUNTGT DEFVERB VERBDEF') 
    def expr(self, p):
        if p[0][2:] not in self.processes:
            self.processes[p[0][2:]] = [p[1][1:-1],p[3][1:-1]]
        print('Processes Dictionary :',self.processes)
    
    '''
    @_('ADD COUNTS COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        self.states[p[5][2:]][p[3][2:]] = self.states[p[5][2:]][p[3][2:]]+int(p[1])
    '''