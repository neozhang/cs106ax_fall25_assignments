# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

###########################################################################
# Your job for Milestone #1 is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the getNextRoom method into the AdvGame class and replace  #
# it with a getPassages method that returns the dictionary of passages.   #
###########################################################################

# Constants

MARKER = "-----"


class AdvRoom:
    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._shortdesc = shortdesc
        self._longdesc = longdesc
        self._passages = passages
        self._visited = False
        self._objects = []

    def getName(self):
        """Returns the name of this room.."""
        return self._name

    def getShortDescription(self):
        """Returns a one-line short description of this room.."""
        return self._shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self._longdesc

    def getNextRoom(self, verb):
        """Returns the name of the destination room after applying verb."""
        return self._passages.get(verb)

    def setVisited(self):
        if not self._visited:
            self._visited = True

    def hasBeenVisited(self):
        return self._visited

    def addObject(self, obj):
        self._objects.append(obj)

    def removeObject(self, obj):
        self._objects.remove(obj)

    def getContents(self):
        return self._objects

    def containsObject(self, obj):
        return obj in self._objects

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""
        name = f.readline().rstrip()
        if name == "":
            return None
        shortdesc = f.readline().rstrip()
        longdesc = ""
        while True:
            line = f.readline().rstrip()
            if line == MARKER:
                break
            longdesc += line + "\n"
        passages = {}
        while True:
            line = f.readline().rstrip()
            if line == "":
                break
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            verb = line[:colon].strip().upper()
            destination = line[colon + 1 :].strip()
            passages[verb] = destination
        return AdvRoom(name, shortdesc, longdesc, passages)
