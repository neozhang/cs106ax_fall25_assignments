import random

# Constants
PT_TO_LVL = 30
PT_PER_LEVEL = 5
MAXHEALTH_TO_LVL = 80
MAXHEALTH_TO_STR = 2
HIT_TO_STR = 1.5
DEFENSE_TO_STR = 1
LEVEL_BASE = 100
LEVEL_POWER = 1.5


class AdvCharacter:
    """A class representing a character in the game."""

    def __init__(self, name, level, stats, inventory, position, isNPC, isAlive):
        self._name = name
        self._level = level
        self._stats = stats
        self._inventory = inventory
        self._position = position
        self._isAlive = isAlive
        self._isNPC = isNPC

    def getName(self):
        """Returns the player's name."""
        return self._name

    def setName(self, name):
        """Sets the player's name."""
        self._name = name
        return self._name

    def getPosition(self):
        """Returns the player's position."""
        return self._position

    def setPosition(self, position):
        """Sets the player's position."""
        self._position = position
        return self._position

    def getLevel(self):
        """Returns the player's level."""
        return self._level

    def setLevelUp(self, threshold):
        """Processes level up logic."""
        self._level += 1
        s, d, i = randThreeIntsSum(PT_PER_LEVEL)
        strength = self.getStats()["strength"] + s
        dexterity = self.getStats()["dexterity"] + d
        intelligence = self.getStats()["intelligence"] + i
        maxHealth = strength * MAXHEALTH_TO_STR + MAXHEALTH_TO_LVL
        health = maxHealth
        experience = self._stats["experience"] - threshold
        self._stats = {
            "health": health,
            "maxHealth": maxHealth,
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "experience": experience,
            "hit": strength * HIT_TO_STR,
            "defense": strength * DEFENSE_TO_STR,
        }

    def getStats(self):
        """Returns the player's stats."""
        return self._stats

    def getHealth(self):
        """Returns the player's health."""
        return self._position

    def getExperience(self):
        """Returns the palyer's experience."""
        return self._stats["experience"]

    def setExperience(self, experience: int):
        """Sets the palyer's experience. Levels up when requirement met and returns True."""
        nextLevelThreshold = int(
            LEVEL_BASE * (self.getLevel() + 1) ** LEVEL_POWER
        )  # TODO: consider multiple levels up
        if experience >= nextLevelThreshold:
            print(f"nextLevelThreshold: {nextLevelThreshold}")
            print(f"experience: {experience}")
            self.setLevelUp(nextLevelThreshold)
            return True
        else:
            self._stats["experience"] = experience
            return False

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

    def isAlive(self):
        """Returns True if the player is alive"""
        return self._isAlive

    @staticmethod
    def createRandomCharacter(
        position, name="THE ONE", level=1, isNPC=True, inventory=[]
    ):
        """Creates a random character at given position."""
        # build stats
        p = level * PT_TO_LVL  # = str + dex + int
        strength, dexterity, intelligence = randThreeIntsSum(p)
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
        return AdvCharacter(name, level, stats, inventory, position, isNPC, True)

    @staticmethod
    def readCharacter(f):
        """Reads a character from a file. Only works for NPC."""
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
        return AdvCharacter(name, level, stats, inventory, position, True, isAlive)


def randThreeIntsSum(sum):
    """Generate 3 integers which sum to a given integer."""
    a = random.randint(0, sum)
    b = random.randint(0, sum - a)
    c = sum - a - b
    return a, b, c
