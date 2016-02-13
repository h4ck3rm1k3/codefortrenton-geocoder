import nltk
import pprint

def process(x):
    tokens = nltk.word_tokenize(x)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    found = []
    state = 1
    for y in entities:
        if state ==1 :
            if y[1] == 'CD':
                state =2
                found=[]
            found.append(y[0])                
        else:
            found.append(y[0])                
            if y[1] == 'CD':
                state =1
                yield " ".join(found)
                found = []


