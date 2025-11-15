# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

from AdvCharacters import AdvCharacter
from AdvConstants import WILDCARD
from AdvObject import AdvGear, AdvObject
from AdvPrompt import AdvPrompt, AdvSynonyms
from AdvRoom import AdvRoom

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################


class AdvGame:
    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        self._rooms = self.readRooms(prefix)
        playerGears, npcGears = self.readGears(prefix)
        self._player = AdvCharacter.createRandomCharacter(
            self.getFirstRoom().getName(),
            name="",
            inventory=self.readObjects(prefix),
            gears=playerGears,
            isNPC=False,
        )
        self._npcGears = npcGears
        self._synonyms = AdvSynonyms(prefix + "Synonyms.txt")

    def getRooms(self):
        """Returns the map of rooms"""
        return self._rooms

    def getFirstRoom(self) -> AdvRoom:
        """Returns the first room in the map"""
        return next(iter(self._rooms.values()))

    def getNextRoom(self, currentRoom, verb) -> AdvRoom | None:
        """Returns the next room in the destination."""
        passage = currentRoom.getPassage(verb)
        if not passage:
            return None

        # If passage has an object-specific destination, prefer it when player has object.
        if "objDest" in passage:
            required_obj = passage.get("obj")
            for item in self._player.getInventory():
                if item.getName() == required_obj:
                    dest = passage.get("objDest")
                    break
            else:
                # required object not present
                # fall back to defaultDest if available, otherwise no passage
                dest = passage.get("defaultDest")
        else:
            dest = passage.get("defaultDest")

        if dest is None:
            return None
        return self.getRoomByName(dest)

    def getRoomByName(self, name: str) -> AdvRoom | None:
        """Returns the AdvRoom object by its name"""
        return self._rooms.get(name)

    def createNPC(self, level: int, roomName: str):
        """Creates a NPC with given level in given room, and returns the NPC"""
        room = self.getRoomByName(roomName)
        if room is not None:
            npc = AdvCharacter.createRandomCharacter(
                roomName, name=f"npc_{roomName}", level=level, inventory=[]
            )
            room.addNpc(npc)
            return npc
        else:
            return None

    def readRooms(self, prefix) -> dict[str, AdvRoom]:
        """Reads room data from a file and adds them to the game"""
        rooms = {}
        with open(f"{prefix}Rooms.txt") as f:
            while True:
                currentRoom = AdvRoom.readRoom(f)
                if currentRoom is None:
                    break
                rooms[currentRoom.getName()] = currentRoom
        return rooms

    def readObjects(self, prefix):
        inventory = []
        with open(f"{prefix}Objects.txt") as f:
            while True:
                currentObject = AdvObject.readObject(f)
                if currentObject is None:
                    break
                if currentObject.getInitialLocation() == "PLAYER":
                    inventory.append(currentObject)
                else:
                    room = self.getRoomByName(currentObject.getInitialLocation())
                    if room is not None:
                        room.addObject(currentObject)

        return inventory

    def readGears(self, prefix):
        playerGears = []
        npcGears = []
        with open(f"{prefix}Gears.txt") as f:
            while True:
                currentGear = AdvGear.readGear(f)
                if currentGear is None:
                    break
                if currentGear.getInitialLocation() == "PLAYER":
                    playerGears.append(currentGear)
                elif currentGear.getInitialLocation() == "NPC":
                    npcGears.append(currentGear)
                else:
                    room = self.getRoomByName(currentGear.getInitialLocation())
                    if room is not None:
                        room.addObject(currentGear)
        return playerGears, npcGears

    def run(self):
        """Plays the adventure game stored in this object."""
        current = self.getFirstRoom()

        # Name the player
        print("Welcome to the Adventure!\n" + "Name your hero:")
        playerName = input("> ").strip().upper()
        self._player.setName(playerName)

        prompt = AdvPrompt()

        while prompt.getVerb() != "QUIT":
            # Handle forced passage
            if current.hasForcedPassage():
                next = self.getNextRoom(current, "FORCED")
                if next is not None:
                    current = next
                    self._player.setPosition(current)
                    print(current.getLongDescription())
                    continue
                else:  # End of world. Game over. -> EXIT.
                    break

            # Handle non-forced passage
            if not prompt.isBuiltin():
                if current.hasBeenVisited():
                    print(current.getShortDescription())
                else:
                    print(current.getLongDescription())
                    if len(current.getContents()) > 0:
                        for obj in current.getContents():
                            print(f"There is {obj.getDescription()} here.")
                    current.setVisited()
                npc = self.createNPC(self._player.getLevel(), current.getName())
                print(f"You encountered a NPC: {npc.getName()}. FIGHT?")

            # Get user input
            text = input("> ").strip().upper()
            prompt.setInput(text, self._synonyms)

            # Execute built-in prompt
            handled, result = prompt.execute(current, self._player)
            if handled:
                if result:
                    continue
                else:
                    break

            verb = prompt.getVerb()

            # Handle wildcard passage
            if current.hasPassage(WILDCARD) and not current.hasPassage(verb):
                verb = WILDCARD

            # Handle movement
            next = self.getNextRoom(current, verb)
            if next is None:
                print("You can't go that way.")
            else:
                current = next
                self._player.setPosition(current.getName())
