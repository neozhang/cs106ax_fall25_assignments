"""
This module defines a class that models an object in Adventure.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# You won't need to work with this file until Milestone #4.  In my        #
# solution, none of the milestones required any public methods beyond     #
# the ones defined in this starter file.                                  #
###########################################################################

from AdvConstant import MARKER


class AdvObject:
    def __init__(self, name: str, description: str, location: str):
        """Creates an AdvObject from the specified properties."""
        self._name = name.upper()
        self._description = description
        self._location = location

    def getName(self):
        """Returns the name of this object."""
        return self._name

    def getDescription(self):
        """Returns the description of this object."""
        return self._description

    def getInitialLocation(self):
        """Returns the initial location of this object."""
        return self._location

    @staticmethod
    def readObject(f):
        """Reads and returns the next object from the file."""
        name = ""
        description = ""
        location = ""
        line = f.readline().strip()
        if line == "":
            return None
        name = line
        while True:
            line = f.readline().strip()
            if line == "":
                break
            description = line
            line = f.readline().strip()
            if line == "":
                break
            location = line
            line = f.readline().strip()
        return AdvObject(name, description, location)


class AdvGear(AdvObject):
    def __init__(self, name, description, location, buff, gearType="GENERAL"):
        super().__init__(name, description, location)
        self._buff = buff
        self._isEquipped = False
        self._isEquippable = True
        self._equipSlot = (gearType or "GENERAL").upper()

    def getBuff(self):
        return self._buff

    def isEquipped(self):
        return self._isEquipped

    def setEquipped(self, state):
        self._isEquipped = state

    def isEquippable(self):
        return self._isEquippable

    def getEquipSlot(self):
        return self._equipSlot

    def setEquipSlot(self, slot):
        self._equipSlot = (slot or "GENERAL").upper()

    @staticmethod
    def readGear(f):
        """Reads and returns the next gear from the file."""
        name = f.readline().strip()
        if name == "":
            return None

        description = f.readline().strip()
        gearType = f.readline().strip() or "GENERAL"
        location = f.readline().strip()

        marker = f.readline().strip()
        buff = {}
        if marker == MARKER:
            while True:
                line = f.readline().strip()
                if line == "":
                    break
                key, value = line.split(":")
                buff[key.strip()] = int(value.strip())

        return AdvGear(name, description, location, buff, gearType)
