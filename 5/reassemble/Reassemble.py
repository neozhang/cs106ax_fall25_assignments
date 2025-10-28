# File: Reassemble.py
# -------------------
# This file exports a program that reads in a large number
# of text fragments from a file you choose, and then reconstructs
# the original text so it can be printed out.

from filechooser import chooseInputFile

def extractFragments(filename):
   return [] # placeholder for code that opens and parses the file

def reconstruct(fragments):
   return "[placeholder for reconstruction]"

def Reassemble():
   filename = chooseInputFile("reassemble-files")
   if filename == "":
      print("User canceled file selection. Quitting!")
      return
   fragments = extractFragments(filename)
   if fragments == None:
      print("File didn't respect reassemble file format. Quitting!")
      return
   reconstruction = reconstruct(fragments)
   print(reconstruction)

if __name__ == "__main__":
   Reassemble()
