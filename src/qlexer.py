from sly import Lexer

class QLexer(Lexer):

    tokens = {FRAME, NOUN, ADJ, VERB, 
              COUNTS, COUNTOF, ADJOF, VERBDEF, DEFV, DEFP, NOUNTGT, 
              VERBON, QUERY, FORALL, PREPDEF, PURIFY}
    
    ignore = ' \t\n'
    ignore_comment = r'\#.*'

    FRAME		= r'f_([a-zA-Z][a-zA-Z0-9_]*)' # TODO: Extract only things after underscore : DONE!
    NOUN        = r'n_([a-zA-Z][a-zA-Z0-9_]*)'
    ADJ         = r'a_([a-zA-Z][a-zA-Z0-9_]*)'
    VERB        = r'v_([a-zA-Z][a-zA-Z0-9_]*)'
    COUNTOF     = r'::'
    ADJOF       = r'<-'
    QUERY       = r'\?'
    COUNTS      = r'\d+'
    FORALL      = r'\*'
    NOUNTGT     = r'\([1-9][0-9]*\)'
    DEFV       = r':='
    VERBON      = r'-> \{[a-zA-Z][a-zA-Z0-9_,]*\}'
    VERBDEF     = r'\[[a-zA-Z][a-zA-Z0-9_:+-,|]*\]'

    DEFP       = r'=='
    PREPDEF     = r'/[a-zA-Z][a-zA-Z0-9_<:,|]*/'

    PURIFY      = r'purify'

# if __name__ == '__main__':
#     data = '?::* <- n_ball'
#     lexer = QLexer()
#     for tok in lexer.tokenize(data):
#         if tok.type in ['PROG', 'NOUN', 'ADJ', 'VERB']:
#             tok.value = tok.value[tok.value.index('_')+1:]
#         print('type=%r, value=%r' % (tok.type, tok.value))
