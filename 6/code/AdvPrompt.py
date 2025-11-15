from AdvBattle import AdvBattle
from AdvConstant import HELP_TEXT, MARKER
from tokenscanner import TokenScanner


class AdvPrompt:
    """A class representing a prompt, handles user input and executes built-in commands."""

    def __init__(self, input=""):
        self._builtins = {
            "QUIT": self.handleQuit,
            "HELP": self.handleHelp,
            "ME": self.handleMe,
            "INVENTORY": self.handleInventory,
            "GEAR": self.handleGears,
            "LOOK": self.handleLook,
            "TAKE": self.handleTake,
            "DROP": self.handleDrop,
            "FIGHT": self.handleFight,
        }
        self.setInput(input)

    def getVerb(self):
        return self._tokenized["verb"]

    def getObj(self):
        return self._tokenized["obj"]

    def setInput(self, input, synonyms=None):
        """Sets the input for the prompt."""
        self._raw = input
        self._tokenized = {}
        scanner = TokenScanner(input)
        verb = scanner.nextToken().strip().upper() if scanner.hasMoreTokens() else None
        if synonyms is not None and verb in synonyms.getSynonyms():
            verb = synonyms.getSynonym(verb)
        self._tokenized["verb"] = verb
        self._tokenized["obj"] = ""
        while scanner.hasMoreTokens():
            self._tokenized["obj"] += scanner.nextToken().strip().upper()

    def isBuiltin(self):
        return self._tokenized["verb"] in self._builtins

    def execute(self, room, player):
        """Routes built-in commands to the right handlers; returns True if handled"""
        verb = self.getVerb()
        if verb in self._builtins:
            handler = self._builtins[verb]
            obj = self.getObj()
            return True, handler(obj, room, player)
        return False, None

    def handleQuit(self, obj, room, player):
        return

    def handleHelp(self, obj, room, player):
        print("\n".join(HELP_TEXT))
        return True

    def handleLook(self, obj, room, player):
        print(room.getLongDescription())
        if room.getContents():
            for item in room.getContents():
                print(f"There is {item.getDescription()}.")
        return True

    def handleMe(self, obj, room, player):
        print(f"{player.getName()}: LEVEL {player.getLevel()} @ {player.getPosition()}")
        print(MARKER)
        stats = player.getStats()
        for k, v in stats.items():
            print(f"{k}: {v}")
        print(MARKER)
        self.handleInventory(obj, room, player)
        print(MARKER)
        self.handleGears(obj, room, player)
        return True

    def handleInventory(self, obj, room, player):
        inventory = player.getInventory()
        if len(inventory) == 0:
            print("You are empty-handed.")
        else:
            print("You are carrying:")
            for item in inventory:
                print(f"{item.getDescription()}")
        return True

    def handleGears(self, obj, room, player):
        gears = player.getGears()
        if len(gears) == 0:
            print("You are not wearing anything.")
        else:
            print("You are wearing:")
            for item in gears:
                print(f"{item.getDescription()}")
        return True

    def handleTake(self, obj, room, player):
        if not obj:
            print("Take what?")
            return True
        for item in room.getContents():
            if item.getName() == obj:
                player.addItem(item)
                room.removeObject(item)
                print("Taken.")
                return True

    def handleDrop(self, obj, room, player):
        if not obj:
            print("Drop what?")
            return True
        for item in player.getInventory():
            if item.getName() == obj:
                player.removeItem(item)
                room.addObject(item)
                print("Dropped.")
                return True

    def handleFight(self, obj, room, player):
        npc = room.getNpcs()[-1]
        battle = AdvBattle(player, npc)
        return battle.fight()


class AdvSynonyms:
    """A class representing a set of synonyms for words."""

    def __init__(self, filename):
        self._synonyms = {}
        try:
            with open(filename, "r") as f:
                for line in f:
                    words = line.strip().split("=")
                    if len(words) > 1:
                        self._synonyms[words[0].strip().upper()] = (
                            words[1].strip().upper()
                        )
        except FileNotFoundError:
            self._synonyms = {}

    def getSynonym(self, word):
        """Returns the synonym for the given word."""
        return self._synonyms.get(word)

    def getSynonyms(self):
        """Returns a dictionary of synonyms."""
        return self._synonyms

    def isSynonym(self, word):
        """Returns True if the given word is a synonym."""
        return word in self._synonyms
