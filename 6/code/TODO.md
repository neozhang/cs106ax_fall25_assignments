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

## Refactor Equip Slot System

- [x] Add a `type` field to every gear entry in `CrowtherGears.txt` and document expected values.
- [x] Extend `AdvGear` to store/read the type and expose helpers for slot comparisons.
- [x] Update `AdvCharacter.equip`/`unequip` to enforce one equipped item per slot and to auto-handle swaps when desired.
- [x] Improve `AdvPrompt` equip/unequip handlers to provide clearer messaging and streamline successful operations.
- [x] Retest inventory display and stat recalculation to ensure gear slot restrictions behave correctly.

## Consumable Gear Support

- [x] Detect the `CONSUMABLE` slot when equipping so those items trigger an instant "use" instead of staying equipped.
- [x] Apply consumable buffs directly to the character's base stats, clamp health to the updated max, and purge the item from the player's inventory.
- [x] Allow EQUIP to auto-grab consumables from the current room so they are removed from the map before being consumed, and surface a confirmation message to the player.
