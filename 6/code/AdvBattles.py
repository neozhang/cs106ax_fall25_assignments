import random
from math import sqrt

EXP_TO_LVL = 100
EXP_SQRT_MULTI = 10


class AdvBattle:
    def __init__(self, player, npc):
        self._player = player
        self._npc = npc
        self._playerStats = player.getStats()
        self._npcStats = npc.getStats()
        self._playerIsAlive = player.isAlive()
        self._npcIsAlive = npc.isAlive()
        self._playerFirstMove = (
            self._playerStats["dexterity"] >= self._npcStats["dexterity"]
        )

    def processRound(self, playerFirstMove):
        """Fight one round of the battle."""
        # Read stats (these are dicts we update)
        phit = self._playerStats["hit"]
        pdef = self._playerStats["defense"]
        # php = current player health (we will update the dict after applying damage)
        php = self._playerStats["health"]
        nhit = self._npcStats["hit"]
        ndef = self._npcStats["defense"]
        # nhp = current npc health (we will update the dict after applying damage)
        nhp = self._npcStats["health"]

        # compute damage amounts (float ok; you may round or int() if you prefer)
        playerDamageToNPC = int(phit * (1 - ndef / (ndef + 100)))
        npcDamageToPlayer = int(nhit * (1 - pdef / (pdef + 100)))

        if playerFirstMove:
            # player hits first
            nhp -= playerDamageToNPC
            # store updated NPC health
            self._npcStats["health"] = nhp
            print(
                f"{self._player.getName()} attacked the NPC and caused {playerDamageToNPC} points of damage."
            )
            if nhp <= 0:
                self._npcIsAlive = False
                return

            # NPC retaliates
            php -= npcDamageToPlayer
            # store updated player health
            self._playerStats["health"] = php
            print(
                f"The NPC fought back and caused {npcDamageToPlayer} points of damage."
            )
            if php <= 0:
                self._playerIsAlive = False
                return
        else:
            # NPC hits first
            php -= npcDamageToPlayer
            self._playerStats["health"] = php
            print(
                f"The NPC attacked {self._player.getName()} and caused {npcDamageToPlayer} points of damage."
            )
            if php <= 0:
                self._playerIsAlive = False
                return

            # player retaliates
            nhp -= playerDamageToNPC
            self._npcStats["health"] = nhp
            print(
                f"{self._player.getName()} fought back and caused {playerDamageToNPC} points of damage."
            )
            if nhp <= 0:
                self._npcIsAlive = False
                return

    def processReward(self):
        """Returns the experience points gained from the battle."""
        exp = sqrt(self._npc.getLevel() * EXP_TO_LVL) * EXP_SQRT_MULTI
        return self._player.setExperience(self._player.getExperience() + exp)

    def fight(self):
        """Fights the battle until one survivor. Returns True if the Player won."""
        while True:
            if not (self._npcIsAlive and self._playerIsAlive):
                break
            self.processRound(self._playerFirstMove)
        if self._playerIsAlive:
            if self.processReward():
                print(f"{self._player.getName()} won the battle and leveled up!")
            else:
                print(f"{self._player.getName()} won the battle brilliantly!")
            return True
        else:
            print(f"{self._player.getName()} died in the battle with honor.")
            return False
