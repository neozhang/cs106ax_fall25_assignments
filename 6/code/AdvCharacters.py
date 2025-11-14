import random

# Constants
PT_TO_LVL = 30
PT_PER_LEVEL = 5
MAXHEALTH_TO_LVL = 80
MAXHEALTH_TO_STR = 2
HIT_TO_STR = 3
DEFENSE_TO_STR = 1.2
LEVEL_BASE = 100
LEVEL_POWER = 1.5
BASE_CRIT_MULTIPLIER = 1.5
MAX_DEX_BONUS = 5.0
MAX_CRIT_CHANCE = 0.2


class AdvCharacter:
    """A class representing a character in the game."""

    def __init__(
        self,
        name: str,
        level: int,
        stats: dict,
        inventory: list,
        gears: list,
        position: str,
        isNPC: bool,
        isAlive: bool,
    ):
        self._name = name
        self._level = level
        self._stats = stats
        self._inventory = inventory
        self._gears = gears
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

    def setLevelUp(self):
        """Processes level up logic (one level). Does NOT modify stored experience."""
        # increment level
        self._level += 1
        # distribute stat points for this one level-up
        s, d, i = randThreeIntsSum(PT_PER_LEVEL)
        strength = self.getStats()["strength"] + s
        dexterity = self.getStats()["dexterity"] + d
        intelligence = self.getStats()["intelligence"] + i
        # recalc health (keeps the original per-level constant behavior)
        maxHealth = strength * MAXHEALTH_TO_STR + self._level * MAXHEALTH_TO_LVL
        health = maxHealth
        # preserve existing experience (we do level-subtraction in setExperience)
        experience = self._stats.get("experience")
        # update stats in-place
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
        """Returns the player's experience."""
        return self._stats["experience"]

    def setExperience(self, experience: int):
        """Sets the player's experience as remaining XP. Each level-up reduces XP by the per-level threshold.
        Returns True if at least one level-up occurred, otherwise False.
        """
        # treat incoming value as the remaining XP to store (int)
        experience = int(experience)
        leveled = False
        # repeatedly level up while remaining XP meets the per-level cost for the next level
        while True:
            nextLevelThreshold = int(LEVEL_BASE * (self.getLevel() + 1) ** LEVEL_POWER)
            if experience >= nextLevelThreshold:
                # consume the XP cost for this level and perform one level-up
                experience -= nextLevelThreshold
                self.setLevelUp()
                leveled = True
                # continue loop to check for additional possible level-ups
                continue
            break
        # store the remaining XP
        self._stats["experience"] = experience
        return leveled

    def getCritMultiplier(self):
        critChance = min(self._stats["intelligence"] / 100, MAX_CRIT_CHANCE)
        dexBonus = min(self._stats["dexterity"] / 100, MAX_DEX_BONUS)
        if random.random() < critChance:
            return BASE_CRIT_MULTIPLIER + dexBonus
        return 1.0

    def getInventory(self):
        """Returns the player's inventory."""
        return self._inventory

    def getGears(self):
        """Returns the player's gear."""
        return self._gears

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
        position, name="THE ONE", level=1, isNPC=True, inventory=[], gears=[]
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
            "hit": strength * HIT_TO_STR if not isNPC else strength,
            "defense": strength * DEFENSE_TO_STR,
        }
        # adding buffs
        if gears != []:
            for gear in gears:
                buff = gear.getBuff()
                if buff != []:
                    stats["health"] += buff.get("health", 0)
                    stats["maxHealth"] += buff.get("maxHealth", 0)
                    stats["strength"] += buff.get("strength", 0)
                    stats["dexterity"] += buff.get("dexterity", 0)
                    stats["intelligence"] += buff.get("intelligence", 0)
                    stats["hit"] += buff.get("hit", 0)
                    stats["defense"] += buff.get("defense", 0)
        return AdvCharacter(name, level, stats, inventory, gears, position, isNPC, True)

    @staticmethod
    def readCharacter(f):  # TODO: needs to be implemented
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
        gears = []
        for line in f:
            gears.append(line.strip())
        position = f.readline().strip()
        isAlive = f.readline().strip() == "True"
        return AdvCharacter(
            name, level, stats, inventory, gears, position, True, isAlive
        )


def randThreeIntsSum(sum):
    """Generate 3 integers which sum to a given integer."""
    floor = max(sum // 4, 1)
    a = random.randint(floor, sum - floor * 2)
    b = random.randint(floor, sum - floor - a)
    c = sum - a - b
    return a, b, c
