from sly import Parser
from src.qlexer import QLexer
import re

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
            self.processes[p[0][2:]] = [int(p[1][1:-1]), {}]#{}
            # print(self.processes)
            v_def = p[3][1:-1]

            lr = re.compile(r'([\S]*):([\S]*)')
            parts = lr.search(v_def).groups()
            # print(parts)
            tgt = re.compile(r'[0-9+-]*a_([a-zA-Z][a-zA-Z0-9_]*)\|([0-9]*)\|[0-9+-]*')
            parts2 = tgt.search(parts[0]).groups()
            # print(parts2,parts[1])
            # print(self.processes[p[0][2:]][1])
            self.processes[p[0][2:]][1][parts2[0]] = [int(parts2[1]),parts[1]]
            print(parts)
            # exit()
            # indx = v_def.index(':')
            # v_def_left, v_def_right = v_def[ : indx], v_def[ indx+1:]
            # print(v_def_left, v_def_right)
            # for case_no, left_right_case in enumerate([v_def_left, v_def_right]):
            #     indices_pipe = [i for i, x in enumerate(left_right_case) if x == '|']
            #     targ_noun = int(v_def_left[ int(indices_pipe[0])+1: int(indices_pipe[1]) ])
            #     process_dict[p[0][2:]][int(p[1][1:-1])][targ_noun] = 0
            #     if case_no != 0:
            #         operation = left_right_case[indices_pipe[-1]+1:indices_pipe[-1]+2]
            #         indx_operation = left_right_case.index(operation)
            #         out_after_v = left_right_case[indx_operation+1:]   
            # print(process_dict)    
            # exit()
            
            # self.processes[p[0][2:]] = [int(p[1][1:-1]),p[3][1:-1]]

        # print('Processes Dictionary :',self.processes)

    @_('VERB VERBON NOUN')
    def expr(self, p):
        dig = self.processes[ p[0][2:] ][1]
        baler_dict = self.states[p[2][2:]]
        arekta_baler_dict = self.processes[ p[0][2:] ]
        for k in dig.keys():
            if k in baler_dict.keys():
                baler_string = arekta_baler_dict[1][k][1]
                tgt = re.compile(r'[0-9+-]*a_([a-zA-Z][a-zA-Z0-9_]*)\|([0-9]*)\|[0-9+-]*')
                parts = tgt.search(baler_string).groups()
                baler_string = baler_string.replace('a_'+parts[0]+'|'+parts[1]+'|', str(baler_dict[k]))
                baler_dict[k] = eval(baler_string)
    
    '''
    @_('ADD COUNTS COUNTOF ADJ ADJOF NOUN')
    def expr(self, p):
        self.states[p[5][2:]][p[3][2:]] = self.states[p[5][2:]][p[3][2:]]+int(p[1])
    '''