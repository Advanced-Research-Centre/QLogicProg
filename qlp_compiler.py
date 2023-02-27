from src.qlexer import QLexer
from src.qparser import QParser
import sys

if __name__ == '__main__':
    lexer = QLexer()
    parser = QParser()
    
    f = open(sys.argv[1],"r")
    text = f.read()       
    #for tok in lexer.tokenize(text):
    #    print('type=%r, value=%r' % (tok.type, tok.value))
    result = parser.parse(lexer.tokenize(text))