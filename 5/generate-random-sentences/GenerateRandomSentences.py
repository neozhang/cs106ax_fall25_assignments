# File: GenerateRandomSentences.py
# --------------------------------
# This file exports a program that reads in a grammar file and
# then prints three randomly generated sentences

from webbrowser import get
from filechooser import chooseInputFile
from random import choice


def readGrammar(filename):
    with open(filename) as file:
        lines = file.read().splitlines()
        result = {}
        nonterm = ""
        for line in lines:
            line = line.strip()
            if line[0] == "<" and len(getNonterminalIndex(line)) == 1:
                nonterm = line[1:-1]  # Remove the brackets
                continue
            elif isInteger(line):
                length_of_expansions = int(line)
                curr = 0
                expansions = []
                continue
            elif curr < length_of_expansions:
                expansions.append(line)
                curr += 1
                continue
            result[nonterm] = expansions
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


def isInteger(line):
    try:
        int(line)
        return True
    except ValueError:
        return False


def generateRandomSentence(grammar):
    print(grammar)
    return "[placeholder for a random sentence]"  # replace this with your own implementation


def GenerateRandomSentences():
    filename = chooseInputFile("grammars")
    grammar = readGrammar(filename)
    for i in range(3):
        print(generateRandomSentence(grammar))


if __name__ == "__main__":
    GenerateRandomSentences()
