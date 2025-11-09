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
        self._npcs = []

    def getName(self):
        """Returns the name of this room."""
        return self._name

    def getShortDescription(self):
        """Returns a one-line short description of this room."""
        return self._shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self._longdesc

    def getPassage(self, verb):
        """Returns the destination list of this room."""
        return self._passages.get(verb)

    def hasPassage(self, verb):
        """Returns True if this room has a passage for the given verb."""
        return verb in self._passages

    def hasForcedPassage(self):
        """Returns True if this room has a forced passage."""
        return self._passages.get("FORCED") is not None

    def setVisited(self):
        """Sets the visited status of this room."""
        if not self._visited:
            self._visited = True

    def hasBeenVisited(self):
        """Returns True if this room has been visited."""
        return self._visited

    def addObject(self, obj):
        """Adds an object to this room."""
        self._objects.append(obj)

    def removeObject(self, obj):
        """Removes an object from this room."""
        self._objects.remove(obj)

    def getContents(self):
        """Returns the contents of this room."""
        return self._objects

    def containsObject(self, obj):
        """Returns True if this room contains the given object."""
        return obj in self._objects

    def addNpc(self, npc):
        """Adds a NPC to this room"""
        self._npcs.append(npc)

    def removeNpc(self, npc):
        """Adds a NPC to this room"""
        self._npcs.remove(npc)

    def getNpcs(self):
        return self._npcs

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""

        # Read room name
        name = f.readline().rstrip()
        if name == "":
            return None

        # Read room descriptions
        shortdesc = f.readline().rstrip()
        longdesc = ""
        while True:
            line = f.readline().rstrip()
            if line == MARKER:
                break
            longdesc += line + "\n"
        longdesc = longdesc.rstrip()

        # Read room passages
        passages = {}
        while True:
            line = f.readline().rstrip()
            if line == "":
                break
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            verb = line[:colon].strip().upper()
            destination = line[colon + 1 :].strip()  # take the part after the colon

            # Handle conditional destinations
            if verb not in passages:
                passages[verb] = {}
            if "/" in destination:
                passages[verb]["objDest"], passages[verb]["obj"] = destination.split(
                    "/"
                )
            else:
                passages[verb]["defaultDest"] = destination

        return AdvRoom(name, shortdesc, longdesc, passages)
