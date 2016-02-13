import nltk
import pprint
import parse_sms

f= open("tests.txt")
for x in f.readlines():
    for y in parse_sms.process(x):
        print y
