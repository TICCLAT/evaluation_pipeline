#!/usr/bin/python3
"""
    hapaxCount.py: determine frequency of known words in text
    usage hapaxCount.py file1.txt [file2.txt ...]
    20181127 erikt(at)xs4all.nl
"""

import nltk
import re
import sys

COMMAND = sys.argv.pop(0)

def isWord(string):
    return(re.search(r"[a-zA-Z]",string))

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

def countWords(text):
    tokenized = tokenize(text)
    nbrOfWords = 0
    for token in tokenized.split():
        if isWord(token): nbrOfWords += 1
    return(nbrOfWords)

def getHapaxes(texts):
    wordCounts = {}
    lowerCaseWordCounts = {}
    for text in texts.values():
        tokenized = tokenize(text)
        for token in tokenized.split():
            if isWord(token): 
                if not token in wordCounts: wordCounts[token] = 0
                if not token.lower() in lowerCaseWordCounts: 
                    lowerCaseWordCounts[token.lower()] = 0
                wordCounts[token] += 1
                lowerCaseWordCounts[token.lower()] += 1
    hapaxes = [x for x in wordCounts.keys() if wordCounts[x] == 1]
    lowerCaseHapaxes = [x for x in lowerCaseWordCounts.keys() if lowerCaseWordCounts[x] == 1]
    return(hapaxes,lowerCaseHapaxes)

def countHapaxes(text,hapaxes,lowerCaseHapaxes):
    nbrOfHapaxes,nbrOfLowerCaseHapaxes = 0,0
    tokenized = tokenize(text)
    for token in tokenized.split():
        if token in hapaxes: nbrOfHapaxes += 1
        if token.lower() in lowerCaseHapaxes: 
            nbrOfLowerCaseHapaxes += 1
    return(nbrOfHapaxes,nbrOfLowerCaseHapaxes)

def printResults(fileName,nbrOfWords,nbrOfHapaxes,nbrOfLowerCaseHapaxes):
    print(fileName+": Number of words: "+str(nbrOfWords)+"; Hapaxes: "+str(int(1000*nbrOfHapaxes/nbrOfWords)/10)+"%"+"; Lower Case Hapaxes: "+str(int(1000*nbrOfLowerCaseHapaxes/nbrOfWords)/10)+"%")

def main(argv):
    texts = readTexts(argv)
    hapaxes,lowerCaseHapaxes = getHapaxes(texts)
    for fileName in texts:
        nbrOfWords = countWords(texts[fileName])
        nbrOfHapaxes,nbrOfLowerCaseHapaxes = countHapaxes(texts[fileName],hapaxes,lowerCaseHapaxes)
        printResults(fileName,nbrOfWords,nbrOfHapaxes,nbrOfLowerCaseHapaxes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
