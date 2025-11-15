# TODO: Dynamic Equipment System

This is a list of tasks to implement a dynamic equipment system where players can equip and unequip items.

## Core Feature: Dynamic Equipment

- [x] **Merge `inventory` and `gears` in `AdvCharacter`:**
    - [x] Modify `AdvCharacter.__init__` to use a single list for all items.
    - [x] Update `createRandomCharacter` and `readCharacter` to reflect this change.

- [x] **Enhance `AdvObject` for Equipment:**
    - [x] Add an `is_equipped` boolean attribute to the `AdvObject` class to track its state.
    - [x] Consider adding an `is_equippable` attribute to differentiate between equippable and non-equippable items.
    - [x] Consider adding an `equip_slot` attribute (e.g., "weapon", "armor") for more advanced equipment logic.

- [x] **Implement Equipment Management in `AdvCharacter`:**
    - [x] Create an `equip(item)` method in `AdvCharacter` to equip an item. This method should apply the item's buffs to the character's stats.
    - [x] Create an `unequip(item)` method in `AdvCharacter` to unequip an item. This method should remove the item's buffs.
    - [x] Modify stat calculation (e.g., in `getStats` or a new `recalculateStats` method) to dynamically account for buffs from all equipped items.

- [x] **Integrate into Game Loop:**
    - [x] Add `EQUIP` and `UNEQUIP` to the list of recognized commands in the game.
    - [x] Implement the logic in the main game loop (`AdvGame.py` or `Adventure.py`) to handle these new commands.

- [x] **Update Item Representation:**
    - [x] Ensure that item descriptions indicate whether they are equippable.
    - [x] When displaying inventory, show which items are currently equipped.