# CONFIG

ADVENTURE_PREFIX = "Crowther"

# TEXT

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT.",
]

WILDCARD = "*"

MARKER = "-----"

# CHARACTER

CHARACTER = {
    "PT_TO_LVL": 30,
    "PT_PER_LEVEL": 5,
    "MAXHEALTH_TO_LVL": 80,
    "MAXHEALTH_TO_STR": 2,
    "HIT_TO_STR": 3,
    "DEFENSE_TO_STR": 1.2,
    "LEVEL_BASE": 100,
    "LEVEL_POWER": 1.5,
    "BASE_CRIT_MULTIPLIER": 1.5,
    "MAX_DEX_BONUS": 5.0,
    "MAX_CRIT_CHANCE": 0.2,
}

# BATTLE

BATTLE = {
    "EXP_TO_LVL": 100,
    "EXP_SQRT_MULTI": 10,
}
