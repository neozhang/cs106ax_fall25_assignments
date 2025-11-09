import random

# Constants
TOTAL_CAP_TO_LVL = 30
MAXHEALTH_TO_LVL = 80
MAXHEALTH_TO_STR = 2
HIT_TO_STR = 1.5
DEFENSE_TO_STR = 1


class AdvCharacter:
    """A class representing a character in the game."""

    def __init__(self, name, level, stats, inventory, position, isAlive):
        self._name = name
        self._level = level
        self._stats = stats
        self._inventory = inventory
        self._position = position
        self._isAlive = isAlive

    def getName(self):
        """Returns the player's name."""
        return self._name

    def setName(self, name):
        """Sets the player's name."""
        self._name = name
        return self._name

    def getInventory(self):
        """Returns the player's inventory."""
        return self._inventory

    def addItem(self, item):
        """Adds an item to the player's inventory."""
        self._inventory.append(item)

    def removeItem(self, item):
        """Removes an item from the player's inventory."""
        self._inventory.remove(item)

    def hasItem(self, item):
        """Returns True if the player has the given item."""
        return item in self._inventory

    @staticmethod
    def createRandomCharacter(position, name="THE ONE", level=1, inventory=[]):
        """Creates a random character at given position."""
        # build stats
        totalCap = level * TOTAL_CAP_TO_LVL  # = str + dex + int
        strength = random.randint(1, totalCap)
        dexterity = random.randint(1, totalCap - strength)
        intelligence = totalCap - strength - dexterity
        maxHealth = strength * MAXHEALTH_TO_STR + level * MAXHEALTH_TO_LVL
        health = maxHealth
        stats = {
            "health": health,
            "maxHealth": maxHealth,
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "experience": 0,
            "hit": strength * HIT_TO_STR,
            "defense": strength * DEFENSE_TO_STR,
        }
        return AdvCharacter(name, level, stats, inventory, position, True)

    @staticmethod
    def readCharacter(f):
        """Reads a character from a file."""
        name = f.readline().strip()
        level = int(f.readline().strip())
        stats = {}
        for line in f:
            key, value = line.strip().split(":")
            stats[key] = int(value)
        inventory = []
        for line in f:
            inventory.append(line.strip())
        position = f.readline().strip()
        isAlive = f.readline().strip() == "True"
        return AdvCharacter(name, level, stats, inventory, position, isAlive)
