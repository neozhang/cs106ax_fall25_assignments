# File: GenerateRandomSentences.py
# --------------------------------
# This file exports a program that reads in a grammar file and
# then prints three randomly generated sentences

from filechooser import chooseInputFile
from random import choice


def readGrammar(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
        result = {}
        nonterm = ""
        productions = []
        for line in lines:
            line = line.strip()
            if line and isNonterminal(line):
                nonterm = line
                continue
            elif isInteger(line):
                length_of_productions = int(line)
                curr = 0
                productions = []
                continue
            elif curr < length_of_productions:
                productions.append(line)
                curr += 1
                continue
            result[nonterm] = productions
    return result


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


def isNonterminal(line):
    return line[0] == "<" and len(getNonterminalIndex(line)) == 1


def isInteger(line):
    try:
        int(line)
        return True
    except ValueError:
        return False


def generateRandomSentence(grammar):
    startNonterms = grammar["<start>"][0].split()
    # deal with the punctuation in the start nonterminal
    startNonterms[-1] = startNonterms[-1][0 : len(startNonterms[-1]) - 1]
    sentence = ""
    for nonterm in startNonterms:
        sentence += parseProduction(choice(grammar[nonterm]), grammar)
    return sentence.strip() + "."


def parseProduction(production, grammar):
    tokens = production.split()
    partials = ""
    for token in tokens:
        if token and isNonterminal(token):
            partials += parseProduction(choice(grammar[token]), grammar)
        else:
            partials += token + " "
    return partials


def GenerateRandomSentences():
    filename = chooseInputFile("grammars")
    grammar = readGrammar(filename)
    for i in range(3):
        print(generateRandomSentence(grammar))


if __name__ == "__main__":
    GenerateRandomSentences()
