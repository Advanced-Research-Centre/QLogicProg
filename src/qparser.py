from sly import Parser
from src.qlexer import QLexer
import re
import copy
import json

class QParser(Parser):
    
    states = dict()
    processes = dict()
    macrostates = dict()

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
        
    @_('VERB NOUNTGT DEFV VERBDEF')
    def expr(self, p):
        if p[0][2:] not in self.processes:
            self.processes[p[0][2:]] = [int(p[1][1:-1]), {}]
            v_ops = p[3][1:-1].split(",")
            for op in v_ops:
                split_left_right = re.compile(r'([\S]*):([\S]*)')
                op_assign = split_left_right.search(op).groups()
                self.processes[p[0][2:]][1][op_assign[0]] = op_assign[1]

    @_('VERB VERBON')
    def expr(self, p):
        str_tgt_nouns = re.compile(r'-> \{([\S]*)\}')
        tgt_nouns = str_tgt_nouns.search(p[1]).group(1).split(",")
        print('Applying',p[0][2:],'on :',*[i[2:] for i in tgt_nouns])
        tgt_noun = tgt_nouns[0]
        #print('[DEBUG] Processes Dictionary :\n',json.dumps(self.processes, indent=2, default=str))
        src_verb = copy.deepcopy(self.processes[p[0][2:]])
        copy_nouns = {}
        for n in tgt_nouns:
            copy_nouns[n[2:]] = self.states[n[2:]]
        for k in src_verb[1].keys():
            for n_no in range(1,src_verb[0]+1):
                rep_dict = copy_nouns[tgt_nouns[n_no-1][2:]]
                for rep_adj in rep_dict.keys():
                    src_verb[1][k] = src_verb[1][k].replace('a_'+rep_adj+'|'+str(n_no)+'|', str(rep_dict[rep_adj]))
        for k in src_verb[1].keys():
            src_verb[1][k] = eval(src_verb[1][k])
        find_tgt_adj_noun = re.compile(r'a_([a-zA-Z][a-zA-Z0-9_]*)\|([0-9]*)\|')
        for k in src_verb[1].keys():
            tgt_adj_noun = find_tgt_adj_noun.search(k).groups()
            tgt_noun = tgt_nouns[int(tgt_adj_noun[1])-1][2:]
            self.states[tgt_noun][tgt_adj_noun[0]] = src_verb[1][k] 

    @_('ADJ ADJOF NOUN DEFP PREPDEF')
    def expr(self, p):      
        an_list = p[4][1:-1].split(",")
        if p[2][2:] not in self.macrostates:
            self.macrostates[p[2][2:]] = {}
        self.macrostates[p[2][2:]][p[0][2:]] = an_list
        print(self.macrostates)

    @_('PURIFY NOUN')
    def expr(self, p):
        ops = self.macrostates[p[1][2:]]
        print(ops)
        for a in ops:
            print(self.states[p[1][2:]][a])  
            # Distribute this value to the microstates    