# Adventure Game Enhancements

This version of the Adventure game builds upon the original implementation with significant new systems for character progression, equipment management, combat, and a refactored command interface.

## Character Progression System

The player is now represented by a full `AdvCharacter` model that goes far beyond a simple inventory list. Key features include:

- **Stat Growth & Leveling**: When a character levels up, they randomly gain points in strength, dexterity, and intelligence. These stats automatically recalculate derived attributes like hit chance and defense, as well as maximum health.
- **Experience Tracking**: Characters accumulate experience points that can trigger multiple level gains at once. The experience system integrates with battles—when you win, `AdvBattle.processReward` feeds XP back to your character.

## Equipment & Gear System

A new `AdvGear` subclass extends the basic item system with equipment management (`AdvObject.py`):

- **Typed Items**: A new `CrowtherGears.txt` data file defines equipment that both the player and rooms can spawn with. Each piece of gear has slots, buffs, and equip status.
  - Disclaimer: An LLM was used to generate the gear data file.
- **Equipment Slots**: Characters can equip one item per slot via the `equip/unequip` methods (`AdvCharacter.py`). Stats automatically recalculate from all equipped buffs
- **UI Integration**: The command prompt now exposes EQUIP and UNEQUIP commands, showing available slots and preventing you from dropping items while they're equipped.

## Consumable Items

Consumable gear (like potions) work differently from equipment:

- When you EQUIP a consumable, it's treated as "using" the item.
- The system automatically applies the item's buffs to your base stats, clamps your health to the new maximum, removes the item from play, and sends you a message.

## Combat System

New contest gameplay adds NPC encounters and turn-based battles:

- **NPC Encounters**: When you visit a room, NPCs can spawn and persist in that room via the `_npcs` collection. Each visit to a room can introduce new encounters.
- **Battle Engine**: A dedicated `AdvBattle` class handles combat with turn order, defense-based damage reduction, and critical hits based on your character stats.
- **Command Integration**: The FIGHT command routes through `AdvPrompt.handleFight`, which returns the outcome to the main game loop.

## Refactored Command System

Command handling has been extracted into a dedicated `AdvPrompt` class that replaces inline logic:

- **New Commands**: Beyond the basic verbs from the original game, you now have ME (status inspection) and enhanced inventory readouts showing item slots and equip state.

## Centralized Configuration

All shared constants have been moved into `AdvConstant` for consistency and reuse:

- The game prefix is imported from constants in `Adventure.py`.
- Modules use the shared `MARKER` constant instead of hardcoding delimiters.
- Character and battle tuning numbers are defined in one place for easy balancing.
