# File: Reassemble.py
# -------------------
# This file exports a program that reads in a large number
# of text fragments from a file you choose, and then reconstructs
# the original text so it can be printed out.

from filechooser import chooseInputFile


# Reads a file containing text fragments enclosed in curly braces {}
# and returns them as a list of strings.
def extractFragments(filename):
    with open(filename) as file:
        lines = file.readlines()
        tokens = []
        partial = ""
        for line in lines:
            tokenized = tokenizeStr(partial + line, "{", "}")
            tokens.extend(tokenized["fragments"])  # save the complete fragments
            partial = tokenized["partial"]  # this will be merged into the next line
    return tokens


# Scans a string to find and extract substrings delimited by start and end symbols.
# Returns a dict where the "fragments" key stores the complete fragments,
# and the "partial" key stores the incomplete ones.
def tokenizeStr(s, startSym, endSym):
    tokens = {"fragments": [], "partial": ""}
    lpos, rpos = 0, 0
    pos = 0
    while pos < len(s):
        try:
            lpos = s.index(startSym, pos)
            rpos = s.index(endSym, pos)
            if lpos > rpos:  # deal with an edge case
                s = s[pos:]
                break
            fragment = s[lpos + len(startSym) : rpos]
            tokens["fragments"].append(fragment)  # add the complete fragment
            s = s[rpos + 1 :]
        except ValueError:
            tokens["partial"] = s  # add the incomplete fragment (partial)
            break
    return tokens


# Reconstructs a single string from a list of fragments using a greedy algorithm.
# It repeatedly finds the pair of fragments with the largest overlap, merges them,
# and continues until only one fragment remains.
def reconstruct(fragments):
    while len(fragments) > 1:
        best_overlap_len = -1
        best_merged_str = ""
        best_pair_indices = [-1, -1]

        # Find the best overlapping pair in this iteration
        for i in range(len(fragments)):
            for j in range(i + 1, len(fragments)):
                merged_str, overlap_str = greedyMatch(fragments[i], fragments[j])
                if len(overlap_str) > best_overlap_len:
                    best_overlap_len = len(overlap_str)
                    best_merged_str = merged_str
                    best_pair_indices = [i, j]

        # If no overlap was found, merge the first two fragments
        if best_pair_indices == [-1, -1]:
            pair = fragments[:2]
            merged = pair[0] + pair[1]
            fragments.pop(0)
            fragments.pop(0)
            fragments.append(merged)
        else:
            # Otherwise, remove the best pair and add their merged version
            # Important to remove the fragment with the larger index first
            fragments.pop(max(best_pair_indices))
            fragments.pop(min(best_pair_indices))
            fragments.append(best_merged_str)

    return fragments[0] if fragments else ""


# Finds the best overlap between two strings and merges them.
# Returns the merged string and the overlapping segment.
def greedyMatch(s1, s2):
    # Case 1: One string is completely contained in the other
    if s1 in s2:
        return [s2, s1]
    if s2 in s1:
        return [s1, s2]

    best_overlap = ""
    merged_string = s1 + s2  # Default if no overlap

    # Case 2: Suffix of s1 matches prefix of s2
    for i in range(s2, 0, -1):
        if s1.endswith(s2[:i]):
            if len(s2[:i]) > len(best_overlap):
                best_overlap = s2[:i]
                merged_string = s1 + s2[i:]
            break  # Found the longest possible for this case

    # Case 3: Suffix of s2 matches prefix of s1
    for i in range(s1, 0, -1):
        if s2.endswith(s1[:i]):
            if len(s1[:i]) > len(best_overlap):
                best_overlap = s1[:i]
                merged_string = s2 + s1[i:]
            break  # Found the longest possible for this case

    return [merged_string, best_overlap]


# The main function that drives the reassembly process. It prompts the user
# to choose a file, extracts fragments from it, reconstructs the original
# text, and prints it to the console.
def Reassemble():
    filename = chooseInputFile("reassemble-files")
    if filename == "":
        print("User canceled file selection. Quitting!")
        return
    fragments = extractFragments(filename)
    if not fragments:
        print("File did not contain any fragments or was empty. Quitting!")
        return
    reconstruction = reconstruct(fragments)
    print(reconstruction)


if __name__ == "__main__":
    Reassemble()
