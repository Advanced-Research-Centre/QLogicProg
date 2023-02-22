from sly import Lexer

class QLexer(Lexer):

    tokens = {PROG, NOUN, ADJ, COUNTS, VERB, COUNTOF, ADJOF, QUERY}
    
    ignore = ' \t\n'

    PROG        = r'p_[a-zA-Z_][a-zA-Z0-9_]*' # TODO: Extract only things after underscore : DONE!
    NOUN        = r'n_[a-zA-Z_][a-zA-Z0-9_]*'
    ADJ         = r'a_[a-zA-Z_][a-zA-Z0-9_]*'
    VERB        = r'v_[a-zA-Z_][a-zA-Z0-9_]*'
    COUNTOF     = r'::'
    ADJOF       = r'<-'
    QUERY       = r'\?'
    COUNTS      = r'\d+'

# if __name__ == '__main__':
#     data = '3::a_red <- n_ball'
#     lexer = MyLexer()
#     for tok in lexer.tokenize(data):
#         if tok.type in ['PROG', 'NOUN', 'ADJ', 'VERB']:
#             tok.value = tok.value[tok.value.index('_')+1:]
#         print('type=%r, value=%r' % (tok.type, tok.value))