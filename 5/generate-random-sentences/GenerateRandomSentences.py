# File: GenerateRandomSentences.py
# --------------------------------
# This file exports a program that reads in a grammar file and
# then prints three randomly generated sentences

from string import punctuation
from filechooser import chooseInputFile
from random import choice

globals = {"punctuation": [".", "?", "!", ",", ":", ";"]}


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
            if line and num_of_productions == 0 and isNonterminal(line):
                nonterm = line
                continue
            elif isInteger(line):
                num_of_productions = int(line)
                curr = 0
                productions = []
                continue
            elif curr < num_of_productions:
                productions.append(line)
                curr += 1
                continue
            result[nonterm] = productions
            num_of_productions = 0
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


def isPunctuation(token):
    return token in globals["punctuation"]


def generateRandomSentence(grammar):
    for k, v in grammar.items():
        if k == "<start>":
            sentence = parseProduction(v[0], grammar)
            return removeSpaceBeforePunctuation(sentence)
    return ""


def parseProduction(production, grammar):
    tokens = tokenizeProduction(production)
    partials = ""
    for token in tokens:
        if token and isNonterminal(token):
            partials += parseProduction(choice(grammar[token]), grammar)
        else:
            partials += token + " "
    return partials


def tokenizeProduction(production):
    # need to add whitespace around nonterminals before splitting
    # to deal with the punctuation issues
    for ch in production:
        if ch == "<":
            production = production.replace(ch, " <")
        elif ch == ">":
            production = production.replace(ch, "> ")
    return production.split()


def removeSpaceBeforePunctuation(sentence):
    for p in globals["punctuation"]:
        sentence = sentence.replace(" " + p, p)
    return sentence


def GenerateRandomSentences():
    filename = chooseInputFile("grammars")
    grammar = readGrammar(filename)
    # print(grammar)
    # print("_____________")
    for i in range(3):
        print(generateRandomSentence(grammar))


if __name__ == "__main__":
    GenerateRandomSentences()
