#!/usr/bin/python3
"""
    knownWords.py: compute frequency of known words in text
    usage knownWords.py file1.txt [file2.txt ...]
    20181127 erikt(at)xs4all.nl
"""

import nltk
import re
import sys

COMMAND = sys.argv.pop(0)
LEXICONFILE = "/home/erikt/projects/teamproject2018-11/lexicons/Dutch/OCRLexicon/DBNL.mostFrequent.tf"
NELEXICONFILE = "/home/erikt/projects/teamproject2018-11/lexicons/NE_Lexicon_NL/ocrlexicon_dutch.lex"
USEWORDSFROMOTHERTEXTS = False

def isWord(string):
    return(re.search(r"[a-zA-Z]",string))

def readLexicon(fileName,lexicon,lexiconLowerCase):
    try: inFile = open(fileName,"r",encoding="ISO-8859-1")
    except Exception as e: 
        sys.exit(COMMAND+": cannot read lexicon file: "+fileName)
    try:
        for line in inFile:
            if isWord(line):
                line = line.strip()
                line = re.sub(r"\t.*$","",line)
                tokens = line.split()
                for token in tokens:
                    lexicon[token] = True
                    lexiconLowerCase[token.lower()] = True
    except Exception as e: print(COMMAND+": error: "+str(e),file=sys.stderr)
    inFile.close()
    return(lexicon,lexiconLowerCase)

def tokenize(text):
    tokenizedSentenceList = nltk.word_tokenize(text)
    tokenizedText = " ".join(tokenizedSentenceList)
    return(tokenizedText)

def readSingleText(fileName):
    text = ""
    try: inFile = open(fileName,"r")
    except Exception as e: sys.exit(COMMAND+": error: "+str(e))
    for line in inFile: text += line
    inFile.close()
    return(text)

def readTexts(argv):
    texts = {}
    for fileName in argv: texts[fileName] = readSingleText(fileName)
    return(texts)

def checkText(text,lexicon,lexiconLowerCase):
    tokenized = tokenize(text)
    nbrOfWords,correctWithCase,correctWithoutCase = 0,0,0
    for token in tokenized.split():
        if isWord(token):
            nbrOfWords += 1
            if token in lexicon: correctWithCase += 1
            if token.lower() in lexiconLowerCase: correctWithoutCase += 1
    return(nbrOfWords,correctWithCase,correctWithoutCase)

def printResults(fileName,nbrOfWords,correctWithCase,correctWithoutCase):
    print(fileName+": Known tokens: Case sensitive: "+str(int(1000*correctWithCase/nbrOfWords)/10)+"% Case insensitive: "+str(int(1000*correctWithoutCase/nbrOfWords)/10)+"%")

def addToLexiconText(lexicon,lexiconLowerCase,text):
    tokenized = tokenize(text)
    for token in tokenized.split(): 
        if isWord(token):
            lexicon[token] = True
            lexiconLowerCase[token.lower()] = True
    return(lexicon,lexiconLowerCase)

def main(argv):
    baseLexicon,baseLexiconLowerCase = readLexicon(LEXICONFILE,{},{})
    baseLexicon,baseLexiconLowerCase = readLexicon(NELEXICONFILE,baseLexicon,baseLexiconLowerCase)
    texts = readTexts(argv)
    for fileName1 in texts:
        lexicon = dict(baseLexicon)
        lexiconLowerCase = dict(baseLexiconLowerCase)
        if USEWORDSFROMOTHERTEXTS:
            for fileName2 in texts: 
                if fileName2 != fileName1:
                    lexicon,lexiconLowerCase = addToLexiconText(lexicon,lexiconLowerCase,texts[fileName2])
        nbrOfWords,correctWithCase,correctWithoutCase = checkText(texts[fileName1],lexicon,lexiconLowerCase)
        printResults(fileName1,nbrOfWords,correctWithCase,correctWithoutCase)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
