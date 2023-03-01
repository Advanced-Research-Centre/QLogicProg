from sly import Parser
from src.qlexer import QLexer
import re
import copy
import json

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
        if p[2][2:] in self.states[p[4][2:]].keys():
            print('Total Counts of',p[4][2:],'for',p[2][2:],':', self.states[p[4][2:]][p[2][2:]])
        else:
            print('Total Counts of',p[4][2:],'for',p[2][2:],': Null')
    
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
            self.processes[p[0][2:]] = [int(p[1][1:-1]), {}]
            v_def = p[3][1:-1]
            v_ops = v_def.split(",")
            for op in v_ops:
                split_left_right = re.compile(r'([\S]*):([\S]*)')
                op_assign = split_left_right.search(op).groups()
                self.processes[p[0][2:]][1][op_assign[0]] = op_assign[1]
    
    # One noun multiple adj
    @_('VERB VERBON NOUN')
    def expr(self, p):
        print('Applying',p[0][2:],'on',p[2][2:])
        #print('[DEBUG] Processes Dictionary :\n',json.dumps(self.processes, indent=2, default=str))
        src_verb = copy.deepcopy(self.processes[p[0][2:]][1])
        copy_noun = copy.deepcopy(self.states[p[2][2:]])
        baler_dict = self.states[p[2][2:]]
        for k in src_verb.keys():
            for adj in copy_noun.keys():
                src_verb[k] = src_verb[k].replace('a_'+adj+'|1|', str(copy_noun[adj])) 
        for k in src_verb.keys():
            src_verb[k] = eval(src_verb[k])
        for k in src_verb.keys():
            self.states[p[2][2:]][k[2:-3]] = src_verb[k]                

    # One noun one adj
    """
    @_('VERB VERBON NOUN')
    def expr(self, p):
        print('Applying',p[0][2:],'on',p[2][2:])
        print('[DEBUG] Processes Dictionary :')#,self.processes)
        print (json.dumps(self.processes, indent=2, default=str))
        src_verb = self.processes[p[0][2:]][1]
        baler_dict = self.states[p[2][2:]]
        # print(src_verb)
        for k in src_verb.keys():
            if k in baler_dict.keys():
                baler_string = src_verb[k][1]
                tgt = re.compile(r'[0-9+-]*a_([a-zA-Z][a-zA-Z0-9_]*)\|([0-9]*)\|[0-9+-]*')
                parts = tgt.search(baler_string).groups()
                baler_string = baler_string.replace('a_'+parts[0]+'|'+parts[1]+'|', str(baler_dict[k]))
                baler_dict[k] = eval(baler_string)
    """