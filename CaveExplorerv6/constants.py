# constants.py

# Goals:
#   - Store constant values used throughout the game.
#   - Centralize these values to make them easy to modify.
#   - Avoid "magic numbers" and strings in the code.
#   - Improve code readability and maintainability.

# Interactions:
#   - Any file that needs to use these constants.

# --- Tile Size ---
TILE_SIZE = 32

# --- Screen Dimensions (can be overridden by config.json) ---
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600

# --- Player Defaults ---
DEFAULT_PLAYER_NAME = "Hero"
DEFAULT_PLAYER_CLASS = "warrior"
DEFAULT_START_X = 5
DEFAULT_START_Y = 5

# --- Directions (for movement and facing) ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Colors (example - you'll likely use Kivy's color properties) ---
# These are (red, green, blue, alpha) tuples, values from 0.0 to 1.0
BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
RED = (1, 0, 0, 1)
GREEN = (0, 1, 0, 1)
BLUE = (0, 0, 1, 1)
GREY = (0.5, 0.5, 0.5, 1)

# --- Game States (Example) ---
# You might use these to manage different game states (e.g., exploring, in combat, in menu)
# STATE_EXPLORING = "exploring"
# STATE_COMBAT = "combat"
# STATE_MENU = "menu"

# --- Item Types ---
ITEM_TYPE_CONSUMABLE = "consumable"
ITEM_TYPE_WEAPON = "weapon"
ITEM_TYPE_ARMOR = "armor"
ITEM_TYPE_CURRENCY = "currency"
ITEM_TYPE_INGREDIENT = "ingredient"

# --- Skill Types ---
SKILL_TYPE_ATTACK = "attack"
SKILL_TYPE_HEALING = "healing"
SKILL_TYPE_BUFF = "buff"
SKILL_TYPE_UTILITY = "utility"

# --- Character Classes ---
CLASS_WARRIOR = "warrior"
CLASS_MAGE = "mage"
CLASS_ROGUE = "rogue"
CLASS_CLERIC = "cleric"

# ---File Paths ---
# (It's often better to construct file paths dynamically using os.path.join,
#  but for simple constants, this is sometimes okay.  Just be consistent.)
#MAP_FILE_PATH = "data/maps/{}.json" # Example - use os.path.join in your code

# --- Add more constants as needed --- # Best Practice