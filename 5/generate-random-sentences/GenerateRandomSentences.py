# File: GenerateRandomSentences.py
# --------------------------------
# This file exports a program that reads in a grammar file and
# then prints three randomly generated sentences

from filechooser import chooseInputFile
from random import choice

globals = {"punctuation": [".", "?", "!", ",", ":", ";"]}

# FUNCTION DEFINITIONS
# --------------------


# readGrammar(filename)
# Reads grammar rules from a file and returns it as a dictionary.
def readGrammar(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
        result = {}
        nonterm = ""
        productions = []
        curr = 0
        num_of_productions = 0
        for line in lines:
            line = line.strip()
            if line and num_of_productions == 0:
                # initialize when line exists and we haven't reached the productions yet
                if isNonterminal(line):
                    nonterm = line
                    continue
                elif isInteger(line):
                    num_of_productions = int(line)
                    productions = []
                    continue
            elif curr < num_of_productions:
                # otherwise we enter this sub-loop
                productions.append(line)
                curr += 1
                continue
            elif curr == num_of_productions:
                # until we finish all productions, reset curr
                curr = 0
            result[nonterm] = productions
            num_of_productions = 0
    return result


# generateRandomSentence(grammar)
# Generate a random sentence using the given grammar dictionary.
def generateRandomSentence(grammar):
    for k, v in grammar.items():
        if k == "<start>":
            sentence = parseProduction(v[0], grammar)
            return removeSpaceBeforePunctuation(sentence)
    return ""


# parseProduction(grammar, production)
# Parse a production string and generate a sentence using the given grammar dictionary recursively.
def parseProduction(production, grammar):
    tokens = tokenizeProduction(production)
    partials = ""
    for token in tokens:
        if token and isNonterminal(token):
            partials += parseProduction(choice(grammar[token]), grammar)
        else:
            partials += token + " "
    return partials


# GenerateRandomSentences()
# Read grammar and write sentences
def GenerateRandomSentences():
    filename = chooseInputFile("grammars")
    grammar = readGrammar(filename)
    for i in range(3):
        print(generateRandomSentence(grammar))


# HELPERS
# -------


# Helper: getNonterminalIndex(line)
# Returns a list of tuples representing the start and end indices of nonterminal symbols in the given line.
def getNonterminalIndex(line):
    result = []
    while line:
        try:
            startIdx = line.index("<")
            endIdx = line.index(">")
            result.append([startIdx, endIdx])
            line = line[endIdx + 1 :]
        except ValueError:
            break
    return result


# Helper: isNonterminal(line)
# Returns True if the given line is a nonterminal symbol, False otherwise.
def isNonterminal(line):
    return line[0] == "<" and len(getNonterminalIndex(line)) == 1


# Helper: isInteger(line)
# Returns True if the given line is an integer, False otherwise.
def isInteger(line):
    try:
        int(line)
        return True
    except ValueError:
        return False


# Helper: isPunctuation(token)
# Returns True if the given token is a punctuation symbol, False otherwise.
def isPunctuation(token):
    return token in globals["punctuation"]


# Helper: tokenizeProduction(production)
# Tokenizes the given production string into a list of tokens.
def tokenizeProduction(production):
    tokens = []
    lpos, rpos = 0, 0
    remains = production
    while True:
        try:
            lpos = remains.index("<")
            rpos = remains.index(">")
            if lpos > rpos:
                break
            if lpos != 0:
                tokens.extend(remains[:lpos].split())
            tokens.append(remains[lpos : rpos + 1])
            remains = remains[rpos + 1 :].strip()
        except ValueError:
            break
    tokens.extend(remains.split())
    return tokens


# Helper: removeSpaceBeforePunctuation(sentence)
# Removes any space before punctuation symbols in the given sentence.
def removeSpaceBeforePunctuation(sentence):
    for p in globals["punctuation"]:
        sentence = sentence.replace(" " + p, p)
    return sentence


# STARTUP

if __name__ == "__main__":
    GenerateRandomSentences()
