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

    def getName(self):
        """Returns the name of this room.."""

    def getShortDescription(self):
        """Returns a one-line short description of this room.."""

    def getLongDescription(self):
        """Returns the list of lines describing this room."""

    def getNextRoom(self, verb):
        """Returns the name of the destination room after applying verb."""

    @staticmethod
    def readRoom(f):
        """Reads a room from the data file."""
