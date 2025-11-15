import random

from AdvConstant import CHARACTER as C


class AdvCharacter:
    """A class representing a character in the game."""

    def __init__(
        self,
        name: str,
        level: int,
        stats: dict,
        items: list,
        position: str,
        isNPC: bool,
        isAlive: bool,
    ):
        self._name = name
        self._level = level
        self._base_stats = stats
        self._stats = None
        self._items = items
        self.recalculateStats()
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
        s, d, i = randThreeIntsSum(C["PT_PER_LEVEL"])
        self._base_stats["strength"] += s
        self._base_stats["dexterity"] += d
        self._base_stats["intelligence"] += i
        # recalc health (keeps the original per-level constant behavior)
        self._base_stats["maxHealth"] = (
            self._base_stats["strength"] * C["MAXHEALTH_TO_STR"]
            + self._level * C["MAXHEALTH_TO_LVL"]
        )
        self._base_stats["health"] = self._base_stats["maxHealth"]
        # update derived stats in base_stats
        self._base_stats["hit"] = self._base_stats["strength"] * C["HIT_TO_STR"]
        self._base_stats["defense"] = self._base_stats["strength"] * C["DEFENSE_TO_STR"]

        self.recalculateStats()

    def getStats(self):
        """Returns the player's stats."""
        return self._stats

    def getHealth(self):
        """Returns the player's health."""
        return self._position

    def getExperience(self):
        """Returns the player's experience."""
        return self._base_stats["experience"]

    def setExperience(self, experience: int):
        """Sets the player's experience as remaining XP. Each level-up reduces XP by the per-level threshold.
        Returns True if at least one level-up occurred, otherwise False.
        """
        # treat incoming value as the remaining XP to store (int)
        experience = int(experience)
        leveled = False
        # repeatedly level up while remaining XP meets the per-level cost for the next level
        while True:
            nextLevelThreshold = int(
                C["LEVEL_BASE"] * (self.getLevel() + 1) ** C["LEVEL_POWER"]
            )
            if experience >= nextLevelThreshold:
                # consume the XP cost for this level and perform one level-up
                experience -= nextLevelThreshold
                self.setLevelUp()
                leveled = True
                # continue loop to check for additional possible level-ups
                continue
            break
        # store the remaining XP
        self._base_stats["experience"] = experience
        if leveled:
            self.recalculateStats()  # Recalculate stats in case level up happened
        return leveled

    def getCritMultiplier(self):
        critChance = min(self._stats["intelligence"] / 100, C["MAX_CRIT_CHANCE"])
        dexBonus = min(self._stats["dexterity"] / 100, C["MAX_DEX_BONUS"])
        if random.random() < critChance:
            return C["BASE_CRIT_MULTIPLIER"] + dexBonus
        return 1.0

    def getItems(self):
        """Returns the player's items."""
        return self._items

    def getEquippedItems(self):
        """Returns a list of equipped items."""
        return [
            item
            for item in self._items
            if hasattr(item, "isEquipped") and item.isEquipped()
        ]

    @staticmethod
    def _normalizeSlot(slot):
        return (slot or "GENERAL").upper()

    @staticmethod
    def _formatSlot(slot):
        return AdvCharacter._normalizeSlot(slot).replace("_", " ").title()

    def _findEquippedItemInSlot(self, slot, exclude=None):
        normalized = self._normalizeSlot(slot)
        for item in self.getEquippedItems():
            if item is exclude:
                continue
            if hasattr(item, "getEquipSlot"):
                item_slot = self._normalizeSlot(item.getEquipSlot())
            else:
                item_slot = "GENERAL"
            if item_slot == normalized:
                return item
        return None

    def addItem(self, item):
        """Adds an item to the player's inventory."""
        self._items.append(item)

    def removeItem(self, item):
        """Removes an item from the player's inventory."""
        self._items.remove(item)

    def hasItem(self, itemName):
        """Returns True if the player has the given item."""
        for item in self._items:
            if item.getName().upper() == itemName.upper():
                return True
        return False

    def recalculateStats(self):
        """Recalculates stats by applying buffs from equipped items to base stats."""
        self._stats = self._base_stats.copy()
        for item in self.getEquippedItems():
            buff = item.getBuff()
            if buff:
                for key, value in buff.items():
                    if key in self._stats:
                        self._stats[key] += value
                    else:
                        self._stats[key] = value

    def _applyBuffToBaseStats(self, buff):
        if not buff:
            return
        for key, value in buff.items():
            current = self._base_stats.get(key, 0)
            self._base_stats[key] = current + value
        if "health" in self._base_stats and "maxHealth" in self._base_stats:
            max_health = self._base_stats["maxHealth"]
            if max_health is not None:
                self._base_stats["health"] = max(
                    0, min(self._base_stats["health"], max_health)
                )

    def _consumeItem(self, item):
        self._applyBuffToBaseStats(item.getBuff() if hasattr(item, "getBuff") else None)
        if hasattr(item, "setEquipped"):
            item.setEquipped(False)
        if item in self._items:
            self.removeItem(item)
        self.recalculateStats()
        return True, f"You consume {item.getName()} and feel its effects immediately."

    def equip(self, itemName):
        """Equips an item from the inventory, enforcing one item per slot."""
        target = (itemName or "").upper()
        for item in self._items:
            if item.getName().upper() == target:
                if not hasattr(item, "isEquippable") or not item.isEquippable():
                    return False, f"You can't equip {item.getName()}."
                if item.isEquipped():
                    return False, f"{item.getName()} is already equipped."
                slot = (
                    self._normalizeSlot(item.getEquipSlot())
                    if hasattr(item, "getEquipSlot")
                    else "GENERAL"
                )
                if slot == "CONSUMABLE":
                    return self._consumeItem(item)
                slot_label = self._formatSlot(slot)
                conflict = self._findEquippedItemInSlot(slot, exclude=item)
                if conflict is not None:
                    return (
                        False,
                        f"You already have {conflict.getName()} equipped in the {slot_label} slot. "
                        "Unequip it first.",
                    )
                item.setEquipped(True)
                self.recalculateStats()
                return True, f"{item.getName()} equipped."
        return False, f"You don't have {itemName}."

    def unequip(self, itemName):
        """Unequips an item by name or slot."""
        target = (itemName or "").upper()
        for item in self._items:
            if item.getName().upper() == target:
                if hasattr(item, "isEquipped") and item.isEquipped():
                    item.setEquipped(False)
                    self.recalculateStats()
                    return True, f"{item.getName()} unequipped."
                if hasattr(item, "isEquippable") and item.isEquippable():
                    return False, f"{item.getName()} is not equipped."
                return False, f"You can't unequip {item.getName()}."
        slot_item = self._findEquippedItemInSlot(target)
        if slot_item is not None:
            slot_item.setEquipped(False)
            self.recalculateStats()
            return True, f"{slot_item.getName()} unequipped."
        return False, f"You don't have {itemName} equipped."

    def isAlive(self):
        """Returns True if the player is alive"""
        return self._isAlive

    @staticmethod
    def createRandomCharacter(position, name="THE ONE", level=1, isNPC=True, items=[]):
        """Creates a random character at given position."""
        # build stats
        p = level * C["PT_TO_LVL"]  # = str + dex + int
        strength, dexterity, intelligence = randThreeIntsSum(p)
        maxHealth = strength * C["MAXHEALTH_TO_STR"] + level * C["MAXHEALTH_TO_LVL"]
        health = maxHealth
        base_stats = {
            "health": health,
            "maxHealth": maxHealth,
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "experience": 0,
            "hit": strength * C["HIT_TO_STR"] if not isNPC else strength,
            "defense": strength * C["DEFENSE_TO_STR"],
        }

        # Equip any equippable items passed in
        occupied_slots = []
        for item in items:
            if hasattr(item, "isEquippable") and item.isEquippable():
                slot = (
                    AdvCharacter._normalizeSlot(item.getEquipSlot())
                    if hasattr(item, "getEquipSlot")
                    else "GENERAL"
                )
                if slot in occupied_slots:
                    item.setEquipped(False)
                else:
                    item.setEquipped(True)
                    occupied_slots.append(slot)

        return AdvCharacter(name, level, base_stats, items, position, isNPC, True)

    @staticmethod
    def readCharacter(f):  # TODO: needs to be implemented
        """Reads a character from a file. Only works for NPC."""
        name = f.readline().strip()
        if name == "":
            return None
        level = int(f.readline().strip())
        stats = {}
        while True:
            line = f.readline().strip()
            if line == "":
                break
            key, value = line.strip().split(":")
            stats[key] = int(value)

        items = []
        while True:
            line = f.readline().strip()
            if line == "":
                break
            items.append(line.strip())  # This should be creating AdvObjects

        position = f.readline().strip()
        isAlive = f.readline().strip() == "True"
        return AdvCharacter(name, level, stats, items, position, True, isAlive)


def randThreeIntsSum(sum):
    """Generate 3 integers which sum to a given integer."""
    floor = max(sum // 4, 1)
    a = random.randint(floor, sum - floor * 2)
    b = random.randint(floor, sum - floor - a)
    c = sum - a - b
    return a, b, c
