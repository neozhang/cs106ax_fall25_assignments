# File: Reassemble.py
# -------------------
# This file exports a program that reads in a large number
# of text fragments from a file you choose, and then reconstructs
# the original text so it can be printed out.

from typing import List
from filechooser import chooseInputFile


def extractFragments(filename):
    with open(filename) as file:
        lines = file.readlines()
        tokens = []
        for line in lines:
            tokens.extend(tokenizeStr(line, "{", "}"))
    return tokens


def tokenizeStr(str, startSym, endSym):
    tokens = []
    lpos, rpos = 0, 0
    remains = str.strip()
    while True:
        try:
            lpos = remains.index(startSym)
            rpos = remains.index(endSym)
            if lpos > rpos:
                break
            tokens.append(remains[lpos + 1 : rpos])
            remains = remains[rpos + 1 :]
        except ValueError:
            break
    tokens.extend(remains)
    # print(tokens)
    return tokens


def reconstruct(fragments):
    str1, str2, longestMatch = "", "", ["", 0, 0]
    for i in range(len(fragments) - 1):
        for j in range(i + 1, len(fragments)):
            thisMatch = [greedyMatch(fragments[i], fragments[j]), i, j]
            thatMatch = [greedyMatch(fragments[j], fragments[i]), j, i]
            if len(thisMatch[0]) < len(thatMatch[0]):
                thisMatch = thatMatch
            if len(thisMatch[0]) > len(longestMatch[0]):
                longestMatch = thisMatch
                str1 = fragments[longestMatch[1]]
                str2 = fragments[longestMatch[2]]
    superStr = createSuperstring(str1, str2, longestMatch[0])
    fragments.remove(str1)
    fragments.remove(str2)
    fragments.append(superStr)
    if len(fragments) > 1:
        reconstruct(fragments)
    return fragments


def greedyMatch(str1, str2) -> str:
    while True:
        if str1.find(str2) == -1:
            str2 = str2[0:-1]
            continue
        else:
            break
    return str2


def createSuperstring(str1, str2, match):
    return str1 + str2[len(match) :]


def lazyMatch(str1, str2) -> str:
    # assuming str1 is the longer string
    match = ""
    for i, ch in enumerate(str2):
        if ch == str1[i]:
            match += ch
    return match


def Reassemble():
    filename = chooseInputFile("reassemble-files")
    if filename == "":
        print("User canceled file selection. Quitting!")
        return
    fragments = extractFragments(filename)
    print(fragments)
    if fragments == None:
        print("File didn't respect reassemble file format. Quitting!")
        return
    reconstruction = reconstruct(fragments)
    print(reconstruction)


if __name__ == "__main__":
    Reassemble()
    # print(greedyMatch("ell that en", "all is well"))
    # print(createSuperstring("ell that en", "all is well"))

    # [ell that en, hat end, hat en] -> ell that end
    # [ell that end, t ends will, t end] -> ell that ends will
