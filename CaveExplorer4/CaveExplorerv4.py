import pygame
import random
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# --- Initialization ---
pygame.init()
pygame.font.init()
# --- Constants ---
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
PURPLE=(80,0,80)
BROWN = (139, 69, 19)  # SaddleBrown
# --- Screen Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
image_path = resource_path("images/town.png") # Use resource_path
town_bg_image = pygame.image.load(image_path)
image_path = resource_path("images/tavern.png") # Use resource_path
tavern_bg_image = pygame.image.load(image_path)
# --- Fonts ---
TITLE_FONT = pygame.font.Font("freesansbold.ttf", 64)
BUTTON_FONT = pygame.font.Font("freesansbold.ttf", 20)
CHARACTER_FONT = pygame.font.Font("freesansbold.ttf", 20)
STATUS_FONT = pygame.font.Font(None, 24)
SMALL_FONT = pygame.font.Font(None, 20)
line_spacing = 20
# --- Menu Variables ---
MENU_TITLE_TEXT = TITLE_FONT.render("Cave Explorer", True, WHITE)
MENU_TITLE_RECT = MENU_TITLE_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 150))
MENU_BUTTON_WIDTH = 250
MENU_BUTTON_HEIGHT = 60
MENU_BUTTON_SPACING = 30
MENU_BUTTON_X_SPACING = 50
MENU_BUTTON_Y = 300
MENU_BUTTON_X = SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH - MENU_BUTTON_X_SPACING // 2
NEW_GAME_BUTTON_RECT = pygame.Rect(MENU_BUTTON_X, MENU_BUTTON_Y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
LOAD_GAME_BUTTON_RECT = pygame.Rect(MENU_BUTTON_X + MENU_BUTTON_WIDTH + MENU_BUTTON_X_SPACING, MENU_BUTTON_Y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
OPTIONS_BUTTON_RECT = pygame.Rect(MENU_BUTTON_X, MENU_BUTTON_Y + MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
QUIT_BUTTON_RECT = pygame.Rect(MENU_BUTTON_X + MENU_BUTTON_WIDTH + MENU_BUTTON_X_SPACING, MENU_BUTTON_Y + MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
NEW_GAME_TEXT = BUTTON_FONT.render("New Game", True, BLACK)
LOAD_GAME_TEXT = BUTTON_FONT.render("Load Game", True, BLACK)
OPTIONS_TEXT = BUTTON_FONT.render("Options", True, BLACK)
QUIT_TEXT = BUTTON_FONT.render("Quit", True, BLACK)
RETRY_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50) # Centered below "Game Over" text
OUTLINE_COLOR = BLACK  # Define outline color globally
TEXT_COLOR = WHITE   # Define main text color globally
shop_scroll_offset = 0
# --- Character Creation Variables ---
CHARACTER_TITLE_TEXT = CHARACTER_FONT.render("Character Creation", True, WHITE)
CHARACTER_TITLE_RECT = CHARACTER_TITLE_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 100))
NAME_INPUT_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 150, 150, 300, 50)
CLASS_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250, 300, 50)
START_GAME_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - 150, 350, 300, 50)
INPUT_ACTIVE = False
PLAYER_NAME = ""
PLAYER_CLASS_NAME = None
PLAYER = None
#Exploration Variables
ROOMS_PER_FLOOR = 10  # Number of rooms to explore before staircase appears
BASE_ROOMS_PER_FLOOR = 10 # Base number of rooms per floor
ROOMS_PER_LEVEL_INCREASE_FACTOR = 2 # Factor to increase rooms per floor with roomlvl
roomlvl = 0  # Starting room level (level 0 is the first floor)
rooms_explored_this_floor = 0 # Counter for rooms explored on the current floor
rooms={}
# --- Combat State Variables ---
player_turn = True
current_enemy = None
combat_log_messages = []
ability_menu_open = False
turn_counter = 1 
# --- Game State ---
MENU = "MENU"
CHARACTER_CREATION = "CHARACTER_CREATION"
TOWN = "TOWN"
DUNGEON = "DUNGEON"
COMBAT = "COMBAT"
GAME_OVER = "GAME_OVER"
CURRENT_STATE = MENU
SHOP = "SHOP"
INVENTORY_IN_COMBAT = "Inventory_in_Combat"
TAVERN="TAVERN"
EQUIPMENT_MENU = "EQUIPMENT_MENU"
SELL = "SELL"
#Shop data
SHOP_CATEGORIES = ["Armor", "Weapons", "Potions", "Scrolls", "Misc."] # Global SHOP_CATEGORIES
current_shop_category_index = 0
SELECTED_TAB_COLOR = (150, 140, 180) 
current_shop_items = []
current_inventory_items=[]
current_inventory_category_index=0
INVENTORY_CATEGORIES=["Armor","Weapons","Potions","Scrolls","Misc"]
STATUS_BUTTON_WIDTH = 100
STATUS_BUTTON_HEIGHT = 30
STATUS_BUTTON_SPACING = 10
STATUS_BAR_HEIGHT = 100
STATUS_BAR_RECT = pygame.Rect(0, SCREEN_HEIGHT - STATUS_BAR_HEIGHT, SCREEN_WIDTH, STATUS_BAR_HEIGHT)
GRID_X = SCREEN_WIDTH - 2 * (STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING) - 10
GRID_Y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 15
BUTTON1_RECT = pygame.Rect(GRID_X, GRID_Y, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON2_RECT = pygame.Rect(GRID_X + STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING, GRID_Y, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON3_RECT = pygame.Rect(GRID_X, GRID_Y + STATUS_BUTTON_HEIGHT + STATUS_BUTTON_SPACING, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON4_RECT = pygame.Rect(GRID_X + STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING, GRID_Y + STATUS_BUTTON_HEIGHT + STATUS_BUTTON_SPACING, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
# --- Status Bar (Add these new constants near the existing button constants) ---
EQUIPMENT_BUTTON_WIDTH = STATUS_BUTTON_WIDTH  # Same width as other buttons
EQUIPMENT_BUTTON_HEIGHT = STATUS_BUTTON_HEIGHT  # Same height
EQUIPMENT_BUTTON_SPACING = STATUS_BUTTON_SPACING  # Same spacing
EQUIPMENT_BUTTON_X = SCREEN_WIDTH - 3 * (STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING) -10 #status button width is 100,
EQUIPMENT_BUTTON_Y = GRID_Y  # Same Y as other buttons
EQUIPMENT_BUTTON_RECT = pygame.Rect(EQUIPMENT_BUTTON_X, EQUIPMENT_BUTTON_Y, EQUIPMENT_BUTTON_WIDTH, EQUIPMENT_BUTTON_HEIGHT)

# --- Shift existing buttons
GRID_X = SCREEN_WIDTH - 2 * (STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING) - 10
GRID_X = EQUIPMENT_BUTTON_X + EQUIPMENT_BUTTON_WIDTH + EQUIPMENT_BUTTON_SPACING # <--- NOW, define relative to EQUIPMENT_BUTTON
GRID_Y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 15
BUTTON1_RECT = pygame.Rect(GRID_X, GRID_Y, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON2_RECT = pygame.Rect(GRID_X + STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING, GRID_Y, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON3_RECT = pygame.Rect(GRID_X, GRID_Y + STATUS_BUTTON_HEIGHT + STATUS_BUTTON_SPACING, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)
BUTTON4_RECT = pygame.Rect(GRID_X + STATUS_BUTTON_WIDTH + STATUS_BUTTON_SPACING, GRID_Y + STATUS_BUTTON_HEIGHT + STATUS_BUTTON_SPACING, STATUS_BUTTON_WIDTH, STATUS_BUTTON_HEIGHT)

# --- Global Variables (Add these) ---
selected_shop_item = None  # ID of the selected item in the shop
selected_inventory_item = None  # ID of the selected item in the inventory

TOWN_BUTTON_TEXTS = ["Tavern", "Shop", "Dungeon", "Menu"]
DUNGEON_BUTTON_TEXTS = ["Attack", "Abilities", "Deeper", "Town"]
COMBAT_BUTTON_TEXTS = ["Attack","Abilities","Items","Run"]
SHOP_BUTTON_TEXTS = ["Buy","Sell","Examine","Leave"]
INVENTORY_IN_COMBAT_TEXTS = ["Use","Examine","Drop","Close",]
TAVERN_BUTTON_TEXTS = ["Rest","Quest","Gamble","Leave"]
EQUIPMENT_MENU_BUTTON_TEXTS =["","","","Close"]
BUTTON_TEXTS = {
    TOWN: TOWN_BUTTON_TEXTS,
    DUNGEON: DUNGEON_BUTTON_TEXTS,
    COMBAT: COMBAT_BUTTON_TEXTS,
    SHOP: SHOP_BUTTON_TEXTS,
    TAVERN: TAVERN_BUTTON_TEXTS,
    EQUIPMENT_MENU:EQUIPMENT_MENU_BUTTON_TEXTS
}
# --- Combat Log UI Constants ---
COMBAT_LOG_X = 0  # X position of the log area (from left edge)
COMBAT_LOG_Y = 370 # Y position of the log area (from top edge) - Adjust based on your screen layout
COMBAT_LOG_WIDTH = 400 # Width of the log area (leave some margin on right/left)
COMBAT_LOG_HEIGHT = 130 # Height of the log area - Adjust as needed to fit messages
COMBAT_LOG_BG_COLOR = BLACK  # Background color of the log area (you can use a darker gray too)
COMBAT_LOG_BORDER_COLOR = WHITE # Border color (optional - you can use GRAY or None for no border)
COMBAT_LOG_BORDER_WIDTH = 1     # Border width in pixels (0 for no border)
COMBAT_LOG_TEXT_COLOR = WHITE # Text color for the log messages
#Tavern Rest UI
SHOW_REST_OPTIONS_BOX = False
REST_OPTION_BUTTON_RECTS = {
    "Barn Loft": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 40), # Example positions, adjust
    "Simple Room": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 300, 40),
    "Private Room": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 70, 300, 40),
}
TAVERN_REST_EXIT_BUTTON_RECT = None 

# --- Quest Data and Functions ---

QUEST_TYPES = ["Exploration", "Extermination"]
QUEST_TYPE_DESCRIPTIONS = {
    "Exploration": "Explore the dungeon and discover new areas.",
    "Extermination": "Defeat dangerous creatures lurking in the dungeon."
}

QUEST_DATA = [
    {
        "type": "Exploration",
        "objective": "Explore the dungeon and discover new areas.",
        "target": 15,  # Explore 15 rooms
        "current_progress": 0,
        "reward": {"coins": 100, "experience": 50},
        "description": "Venture deep into the dungeon and explore 15 rooms. Uncover its secrets and return for a handsome reward."
    },
    {
        "type": "Extermination",
        "objective": "Defeat dangerous creatures lurking in the dungeon.",
        "target": {"monster_type": "Greenskin", "count": 5},  # Kill 5 Greenskins
        "current_progress": 0,
        "reward": {"coins": 150, "experience": 75},
        "description": "Protect the realm by eliminating 5 Greenskin creatures infesting the dungeon. Your bravery will be rewarded."
    },
    # ... more quests
]
# --- Constants for Equipment Screen (Add near other UI constants) ---
EQUIPMENT_MENU_WIDTH = 300
EQUIPMENT_MENU_HEIGHT = 400
EQUIPMENT_MENU_X = 50
EQUIPMENT_MENU_Y = 20  # Moved up!
EQUIPMENT_MENU_RECT = pygame.Rect(EQUIPMENT_MENU_X, EQUIPMENT_MENU_Y, EQUIPMENT_MENU_WIDTH, EQUIPMENT_MENU_HEIGHT)

EQUIPMENT_SLOT_SIZE = 64
EQUIPMENT_SLOT_SPACING = 10
EQUIPMENT_SLOT_START_X = EQUIPMENT_MENU_X + 20
EQUIPMENT_SLOT_START_Y = EQUIPMENT_MENU_Y + 20

# Define positions of equipment slots (adjust as needed for layout)
EQUIPMENT_SLOT_RECTS = {
    "head": pygame.Rect(EQUIPMENT_SLOT_START_X, EQUIPMENT_SLOT_START_Y, EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
    "chest": pygame.Rect(EQUIPMENT_SLOT_START_X, EQUIPMENT_SLOT_START_Y + EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING, EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
    "main_hand": pygame.Rect(EQUIPMENT_SLOT_START_X, EQUIPMENT_SLOT_START_Y + 2 * (EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING), EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
    "off_hand": pygame.Rect(EQUIPMENT_SLOT_START_X + EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING, EQUIPMENT_SLOT_START_Y + 2 * (EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING), EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
    "ring1": pygame.Rect(EQUIPMENT_SLOT_START_X, EQUIPMENT_SLOT_START_Y + 3 * (EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING), EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
    "ring2": pygame.Rect(EQUIPMENT_SLOT_START_X + EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING, EQUIPMENT_SLOT_START_Y + 3 * (EQUIPMENT_SLOT_SIZE + EQUIPMENT_SLOT_SPACING), EQUIPMENT_SLOT_SIZE, EQUIPMENT_SLOT_SIZE),
}
# --- Inventory Display Constants (Add these near your other UI constants) ---
INVENTORY_DISPLAY_WIDTH = 350
INVENTORY_DISPLAY_HEIGHT = 400
INVENTORY_DISPLAY_X = SCREEN_WIDTH - INVENTORY_DISPLAY_WIDTH - 25 # Right side
INVENTORY_DISPLAY_Y = 20  # Moved up!  Match EQUIPMENT_MENU_Y
INVENTORY_DISPLAY_RECT = pygame.Rect(INVENTORY_DISPLAY_X, INVENTORY_DISPLAY_Y, INVENTORY_DISPLAY_WIDTH, INVENTORY_DISPLAY_HEIGHT)

INVENTORY_SLOT_SIZE = 64  # Keep this for image size, but we'll adjust slot height
INVENTORY_SLOT_HEIGHT = 80 # New, taller slot to fit info
INVENTORY_SLOT_SPACING = 10
INVENTORY_SLOTS_PER_ROW = 1 # One item per row
INVENTORY_ROWS = 4  # Display 4 items at a time
INVENTORY_START_X = INVENTORY_DISPLAY_X + 20
INVENTORY_START_Y = INVENTORY_DISPLAY_Y + 30 # Start below tabs.
INVENTORY_CAPACITY = INVENTORY_SLOTS_PER_ROW * INVENTORY_ROWS #max visible, not max capacity

# --- Inventory Scrolling (Similar to Shop Scrolling) ---
inventory_scroll_offset = 0
INVENTORY_SCROLL_BUTTON_WIDTH = 30
INVENTORY_SCROLL_BUTTON_HEIGHT = 30
INVENTORY_SCROLL_UP_BUTTON_X = INVENTORY_DISPLAY_X + INVENTORY_DISPLAY_WIDTH - INVENTORY_SCROLL_BUTTON_WIDTH -10
INVENTORY_SCROLL_UP_BUTTON_Y = INVENTORY_DISPLAY_Y + 10 + 25 # Below tabs
INVENTORY_SCROLL_DOWN_BUTTON_X = INVENTORY_DISPLAY_X + INVENTORY_DISPLAY_WIDTH - INVENTORY_SCROLL_BUTTON_WIDTH - 10
INVENTORY_SCROLL_DOWN_BUTTON_Y = INVENTORY_DISPLAY_Y + INVENTORY_DISPLAY_HEIGHT - INVENTORY_SCROLL_BUTTON_HEIGHT - 10
INVENTORY_SCROLL_UP_BUTTON_RECT = pygame.Rect(INVENTORY_SCROLL_UP_BUTTON_X,INVENTORY_SCROLL_UP_BUTTON_Y, INVENTORY_SCROLL_BUTTON_WIDTH, INVENTORY_SCROLL_BUTTON_HEIGHT)
INVENTORY_SCROLL_DOWN_BUTTON_RECT = pygame.Rect(INVENTORY_SCROLL_DOWN_BUTTON_X, INVENTORY_SCROLL_DOWN_BUTTON_Y, INVENTORY_SCROLL_BUTTON_WIDTH, INVENTORY_SCROLL_BUTTON_HEIGHT)
selected_slot = None #inventory slot

# --- Inventory Tabs ---
INVENTORY_TAB_WIDTH = 60
INVENTORY_TAB_HEIGHT = 25
INVENTORY_TAB_START_X = INVENTORY_DISPLAY_X + 20
INVENTORY_TAB_Y = INVENTORY_DISPLAY_Y -15# Above slots
current_inventory_category_index = 0  # Start with the first category
# --- Shop UI Constants (These should be correct already) ---
SHOP_MENU_WIDTH = INVENTORY_DISPLAY_WIDTH
SHOP_MENU_HEIGHT = INVENTORY_DISPLAY_HEIGHT
SHOP_MENU_X = EQUIPMENT_MENU_X
SHOP_MENU_Y = INVENTORY_DISPLAY_Y
SHOP_MENU_RECT = pygame.Rect(SHOP_MENU_X, SHOP_MENU_Y, SHOP_MENU_WIDTH, SHOP_MENU_HEIGHT)

SHOP_MENU_COLOR = (100, 90, 130)
TAB_COLOR = (120, 110, 150)
SLOT_COLOR = (80, 70, 100)
BUTTON_COLOR = (120, 120, 120)
TAB_WIDTH = 75
TAB_HEIGHT = 25
TAB_START_X = SHOP_MENU_RECT.x + 20
TAB_Y = SHOP_MENU_RECT.y - TAB_HEIGHT
ITEM_SLOT_WIDTH = SHOP_MENU_RECT.width - 60
ITEM_SLOT_HEIGHT = 80
ITEM_SLOTS_START_X = SHOP_MENU_RECT.x + 30
ITEM_SLOTS_START_Y = SHOP_MENU_RECT.y + 20 + TAB_HEIGHT  # Account for tabs!
ITEM_SLOT_SPACING_Y = 10
SCROLL_BUTTON_WIDTH = 30
SCROLL_BUTTON_HEIGHT = 30
SHOP_SCROLL_UP_BUTTON_X = SHOP_MENU_RECT.right - SCROLL_BUTTON_WIDTH -10
SHOP_SCROLL_UP_BUTTON_Y = SHOP_MENU_RECT.y + 10 + TAB_HEIGHT #make the button appear below
SHOP_SCROLL_DOWN_BUTTON_X = SHOP_MENU_RECT.right - SCROLL_BUTTON_WIDTH - 10
SHOP_SCROLL_DOWN_BUTTON_Y = SHOP_MENU_RECT.bottom - SCROLL_BUTTON_HEIGHT - 10
SHOP_SCROLL_UP_BUTTON_RECT = pygame.Rect(SHOP_SCROLL_UP_BUTTON_X, SHOP_SCROLL_UP_BUTTON_Y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
SHOP_SCROLL_DOWN_BUTTON_RECT = pygame.Rect(SHOP_SCROLL_DOWN_BUTTON_X, SHOP_SCROLL_DOWN_BUTTON_Y, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
SHOP_CATEGORIES = ["Armor", "Weapons", "Potions", "Scrolls", "Misc."]
SHOP_TAB_RECTS = {} # Create the dictionary in global


# --- Player Class ---
class Player:
    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name
        self.stats = CLASS_STATS[class_name].copy()  # Start with base stats
        self.stats["attack"] = list(CLASS_STATS[class_name]["attack"]) #attack is a list.
        self.current_health = self.stats['health']
        self.current_mana = self.stats['mana']
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.coins = 500
        self.max_experience = self._calculate_max_experience()
        self.buffs = []
        self.equipment = {
            "head": None,
            "chest": None,
            "main_hand": None,
            "off_hand": None,
            "ring1": None,
            "ring2": None,
        }
    def calculate_damage(self):
        """Calculates the damage for an attack, considering a range and buffs."""
        base_attack_range = self.stats['attack']
        min_damage = base_attack_range[0]
        max_damage = base_attack_range[1]

        buffed_attack = 0
        percentage_buff_multiplier = 1.0

        for buff in self.buffs:
            if buff['stat'] == 'attack_buff':
                if buff.get('is_percentage_buff'):
                    percentage_buff_multiplier += buff['amount']
                else:
                    buffed_attack += buff['amount']

        # Apply percentage multiplier FIRST
        min_damage = round(min_damage * percentage_buff_multiplier)
        max_damage = round(max_damage * percentage_buff_multiplier)

        # THEN add flat buffs/debuffs
        min_damage += buffed_attack
        max_damage += buffed_attack

        # --- Clamp to prevent negative values AND ensure min <= max ---
        min_damage = max(0, min_damage)  # Ensure min_damage is not negative
        max_damage = max(0, max_damage)  # Ensure max_damage is not negative
        min_damage = min(min_damage, max_damage) #Ensure min damage is not more than max

        return random.randint(min_damage, max_damage)
    
    def get_defense(self):
        base_defense = self.stats['defense']
        buffed_defense = base_defense
        for buff in self.buffs: 
            if buff['stat'] == 'defense_buff':
                if buff.get('is_percentage_buff'): 
                    percentage_increase = buff['amount'] 
                    buff_amount = base_defense * percentage_increase
                    buffed_defense += buff_amount
                else: # Flat buff (existing logic)
                    buff_amount = buff['amount']
                    buffed_defense += buff_amount
        return round(buffed_defense)
    def get_name(self):
        return self.name
    def sell_item(self, item_id):
        if item_id in self.inventory:
            item_data = shop_items_data.get(item_id)
            if item_data:  # Make sure item_data exists
                if item_data['category'] == "Loot":
                  sell_price = item_data['price']
                else:
                    sell_price = int(item_data['price'] * 0.6)  # Example: Sell for 60% of buy price
                self.inventory.remove(item_id)
                self.coins += sell_price
                add_combat_message(f"Sold {item_data['name']} for {sell_price} gold.")
                return True
            else: #item doesn't exist
                print(f"Trying to sell an item not in shop data: {item_id}") #debug
                return False
        else: #not in inventory
            print("item not in inventory")#debug
            return False
    # --- Inside the Player class ---
    def use_item(self, item_id, target=None):
        """Uses a consumable item from the inventory."""
        if item_id not in self.inventory:
            print(f"Error: {self.name} does not have {item_id} in inventory.") #debug
            add_combat_message(f"You do not have that item.")
            return False

        item_data = shop_items_data[item_id]
        effect = item_data.get("effect")

        if not effect:
            print(f"Error: Item {item_id} has no effect defined.")#debug
            add_combat_message(f"{item_data['name']} has no effect")
            return False

        if effect["type"] == "heal":
            heal_amount = effect["amount"]
            self.current_health = min(self.stats["health"], self.current_health + heal_amount)
            add_combat_message(f"{self.name} used {item_data['name']} and healed for {heal_amount} HP.")
            self.inventory.remove(item_id)  # Remove item after use
            return True

        elif effect["type"] == "mana":
            restore_amount = effect["amount"]
            self.current_mana = min(self.stats["mana"], self.current_mana + restore_amount)
            add_combat_message(f"{self.name} used {item_data['name']} and restored for {restore_amount} MP.")
            self.inventory.remove(item_id)  # Remove item after use
            return True

        elif effect["type"] == "damage":
            if target is None:
                add_combat_message(f"No target for {item_data['name']}.")
                return False
            damage_amount = effect["amount"]
            damage_dealt = target.take_damage(damage_amount)
            add_combat_message(f"{self.name} used {item_data['name']} on {target.get_name()} for {damage_dealt} damage!")
            self.inventory.remove(item_id)  # Remove item
            return True
        # --- Correct Buff Handling ---
        elif effect["type"] == "buff":
            buff_data = {
                "name": item_data['name'],  # Use item name for buff name
                "stat": effect['stat'],
                "amount": effect['amount'],
                "duration_turns": effect['duration_turns'],
                "is_percentage_buff": effect.get('is_percentage_buff', False)  # Default to False if not specified
            }
            self.apply_buff(buff_data)  # Apply the buff
            self.inventory.remove(item_id)
            return True #return true


        elif effect["type"] == "utility":
            # Handle utility effects (e.g., "light" for a torch, "climbing" for rope)
            # This is highly game-specific.  For now, we'll just print a message.
            add_combat_message(f"{self.name} used {item_data['name']}. ({effect.get('use', 'Unknown effect')})")
            self.inventory.remove(item_id)
            return True
        else:
            add_combat_message(f"Unknown effect type: {effect['type']}")
            return False
        
    def apply_equipment_bonuses(self, item_id):
      item_data = shop_items_data.get(item_id)
      if item_data and "stats_bonus" in item_data:
          for stat, bonus in item_data["stats_bonus"].items():
              if stat == "attack":
                  # Apply bonus to both min and max attack
                  self.stats["attack"][0] += bonus[0]  #add to the min
                  self.stats["attack"][1] += bonus[1] #add to the max
              elif stat in self.stats:
                    self.stats[stat] += bonus
    def remove_equipment_bonuses(self, item_id):
      item_data = shop_items_data.get(item_id)
      if item_data and "stats_bonus" in item_data:
          for stat, bonus in item_data["stats_bonus"].items():
            if stat == "attack":
                  # Apply bonus to both min and max attack
                  self.stats["attack"][0] -= bonus[0]  #add to the min
                  self.stats["attack"][1] -= bonus[1] #add to the max
            elif stat in self.stats:
                self.stats[stat] -= bonus
    def take_damage(self, damage):
        actual_damage = max(0, damage)
        if actual_damage > 0: 
            self.current_health -= actual_damage
            return actual_damage
        else:
            return 0
    def attack(self, target):
        """Attacks a target (enemy)."""
        attacker_accuracy = self.get_accuracy()
        target_evasion = target.get_evasion()

        # --- Accuracy Check ---
        hit_chance_percentage = max(5, min(95, attacker_accuracy - target_evasion))
        if random.random() < (hit_chance_percentage / 100.0):  # Hit
            damage = self.calculate_damage()  # Use calculate_damage()
            damage_dealt = target.take_damage(damage)
            if damage_dealt > 0:
                message_text = (f"{self.name} attacks {target.get_name()} for {damage_dealt} damage!")
            else:
                message_text = (f"{self.name}'s attack was blocked by {target.get_name()}'s defense!")
            add_combat_message(message_text)
            return damage_dealt
        else:  # Miss
            message_text = (f"{self.name} attacks {target.get_name()} and misses!")
            add_combat_message(message_text)
            return 0
    def use_ability(self, ability, target):
        """Handles ability use, applying effects based on ability type."""
        if self.use_mana(ability["mana_cost"]):
            ability_name = ability["name"]
            message_text=(f"{self.name} uses {ability_name}!")
            add_combat_message(message_text)
            ability_type = ability["type"]
            if ability_type == "attack" or ability_type == "magic_attack": # Handle both attack types similarly for now
                damage_multiplier = ability.get("damage_multiplier", 1.0) # Default multiplier to 1.0 if not specified
                damage = int(self.calculate_damage() * damage_multiplier)
                if ability_type == "magic_attack":
                    damage = int(damage * 3) # Example: Magic attacks do 20% more base damage for now - balance later
                damage_dealt = target.take_damage(damage)
                message_text=(f"{ability_name} hits {target.get_name()} for {damage_dealt} damage!")
                add_combat_message(message_text)
            elif ability_type == "buff":
                buff_stat = ability["stat"]
                buff_amount = ability["buff_amount"]
                buff_duration = ability.get("duration", 3) # Default duration if not specified
                buff_name = ability_name # Use ability name as buff name
                if buff_stat == "defense": # Warrior Defensive Stance
                    buff_data = {
                        "name": buff_name,
                        "stat": "defense_buff", # Use "defense_buff" for consistency
                        "amount": buff_amount, # buff_amount is a multiplier (e.g., 0.5 for 50% increase)
                        "duration_turns": buff_duration,
                        "is_percentage_buff": True
                    }
                    self.apply_buff(buff_data)
                elif buff_stat == "magic_shield": # Mage Magic Shield (flat buff) - corrected stat name
                    buff_data = {
                        "name": buff_name,
                        "stat": "defense_buff", #  Using defense_buff for magic shield too - adjust logic if needed later
                        "amount": buff_amount, # buff_amount is flat amount (e.g., 50 flat defense)
                        "duration_turns": buff_duration
                    }
                    self.apply_buff(buff_data)
                elif buff_stat == "evasion": # Rogue Evasion
                    buff_data = {
                    "name": ability_name,
                    "stat": "evasion_buff",
                    "amount": buff_amount,
                    "duration_turns": buff_duration,
                    "is_percentage_buff": True
                    }
                    self.apply_buff(buff_data)
            elif ability_type == "heal": # Heal ability
                heal_amount = ability["heal_amount"]
                self.current_health = min(self.stats['health'], self.current_health + heal_amount) # Heal, but not over max HP
                message_text=(f"{ability_name} heals {self.name} for {heal_amount} HP!")
                add_combat_message(message_text)
            elif ability_type == "multi_attack": # For abilities with multiple attacks (like Rogue's Double Attack - not used yet but prepared)
                number_of_attacks = ability.get("number_of_attacks", 1) # Default to 1 attack if not specified
                damage_multiplier = ability.get("damage_multiplier", 1.0)
                for _ in range(number_of_attacks): # Loop for each attack
                    damage = int(self.get_attack_damage() * damage_multiplier)
                    damage_dealt = target.take_damage(damage)
                    message_text=(f"{ability_name} hits {target.get_name()} for {damage_dealt} damage!")
                    add_combat_message(message_text)
            # After ability use, end player's turn
            global player_turn
            player_turn = False
        else:
            message_text=(f"{self.name} does not have enough mana to use {ability['name']}!")
            add_combat_message(message_text)
    def get_evasion(self):
        buffed_evasion_percentage = self.stats['evasion']

        for buff in self.buffs:
            if buff.get('stat') == 'evasion_buff':
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['buff_amount'] 
                    buffed_evasion_percentage += percentage_increase
                else:
                    buffed_evasion_percentage += buff['buff_amount'] 
        return buffed_evasion_percentage
    def get_accuracy(self):
        accuracy_percentage_whole_number = self.stats['accuracy'] 
        return accuracy_percentage_whole_number 
    def is_alive(self):
        return self.current_health > 0
    def gain_experience(self, xp):
        self.experience += xp
        if self.experience >= self.max_experience: 
            self.level_up()
    def _calculate_max_experience(self): 
        return (self.level ** 2) * 100
    def level_up(self):
        if self.experience >= self.max_experience:
            self.level += 1
            self.experience -= self.max_experience
            self.max_experience = int(self.max_experience * 1.5)
            level_up_stats = CLASS_LEVEL_UP_STATS[self.class_name]
            self.stats["health"] += level_up_stats["health"]
            self.stats["mana"] += level_up_stats["mana"]
            # --- Correctly handle attack range increase ---
            attack_increase = level_up_stats["attack"]
            self.stats["attack"][0] += attack_increase #add to min
            self.stats["attack"][1] += attack_increase #add to max

            self.stats["defense"] += level_up_stats["defense"]
            self.stats["accuracy"] += level_up_stats["accuracy"]
            self.stats["evasion"] += level_up_stats["evasion"]
            self.current_health = self.stats["health"]
            self.current_mana = self.stats["mana"]
            message_text=(f"{self.name} leveled up to Level {self.level}!")
            add_combat_message(message_text)
    def gain_coins(self, gold):
        self.coins += gold
        message_text=(f"{self.name} gained {gold} gold.") 
        add_combat_message(message_text)
    def use_mana(self, amount):
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        else:
            message_text=("Not enough mana!")
            add_combat_message(message_text)
            return False
    def apply_buff(self, buff_data):
        buff_name = buff_data['name']
        buff_stat = buff_data['stat']
        buff_duration = buff_data['duration_turns'] if 'duration_turns' in buff_data else 3
        buff_type = buff_data.get('buff_type')
        if buff_type == "rest":
            rest_buffs_to_remove = []
            current_rest_option_name = buff_name.split(" - ")[1].split(" ")[0]
            for buff in self.buffs:
                if buff.get('buff_type') == "rest":
                    existing_rest_buff_option_name = buff['name'].split(" - ")[1].split(" ")[0] 
                    if existing_rest_buff_option_name != current_rest_option_name: 
                        rest_buffs_to_remove.append(buff)
            for buff_to_remove in rest_buffs_to_remove:
                self.buffs.remove(buff_to_remove)
                message_text=(f"Previous rest buff '{buff_to_remove['name']}' removed.")
                add_combat_message(message_text)
        existing_buff_index = -1
        for index, buff in enumerate(self.buffs):
            if buff['name'] == buff_name and buff['stat'] == buff_stat:
                existing_buff_index = index
                break
        if existing_buff_index != -1:
            self.buffs[existing_buff_index]['duration_turns'] = buff_duration
            message_text=(f"{buff_name} duration refreshed on {self.name}.")
            add_combat_message(message_text)
        else:
            buff = buff_data.copy()
            buff['duration_turns'] = buff_duration
            self.buffs.append(buff)
            message_text=(f"{self.name} is buffed with {buff_name}!")
            add_combat_message(message_text)
    def update_buff_durations(self):
        buffs_to_remove = []
        for buff in self.buffs:
            buff['duration_turns'] -= 1
            if buff['duration_turns'] <= 0:
                buffs_to_remove.append(buff)
                message_text=(f"{buff['name']} buff expired from {self.name}.")
                add_combat_message(message_text)
        for buff in buffs_to_remove:
            self.buffs.remove(buff)
    def start_turn(self):
        self.update_buff_durations() 
    def end_turn(self):
        pass # No end of turn actions for now, but can be extended later
    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}") 
    def add_item_to_inventory(self, item_name):
        self.inventory.append(item_name)
CLASS_STATS = {
    "Warrior": {
        "health": 50,
        "mana": 20,
        "attack": [1,7],
        "defense": 5,
        "accuracy": 80,
        "evasion": 10, 
    },
    "Mage": {
        "health": 30,
        "mana": 50,
        "attack": [1,4],
        "defense": 1,
        "accuracy": 70,
        "evasion": 5,
    },
    "Rogue": {
        "health": 40,
        "mana": 20,
        "attack": [1,12],
        "defense": 3,
        "accuracy": 90,
        "evasion": 15,
    },
}
CLASS_LEVEL_UP_STATS = {
    "Warrior": {
        "health": 15,  
        "mana": 3,    
        "attack": 3,   
        "defense": 2,  
        "accuracy": 1,
        "evasion": 1
    },
    "Mage": {
        "health": 10,
        "mana": 7,     
        "attack": 1,   
        "defense": 1,  
        "accuracy": 2, 
        "evasion": 1
    },
    "Rogue": {
        "health": 12,
        "mana": 5,
        "attack": 2,
        "defense": 1,
        "accuracy": 2, 
        "evasion": 2  
    }
}
CLASS_ABILITIES = {
    "Warrior": [
        {
            "name": "Power Attack",
            "description": "A mighty blow dealing increased damage.",
            "mana_cost": 10,
            "type": "attack",
            "damage_multiplier": 1.6, 
        },
        {
            "name": "Defensive Stance",
            "description": "Enter a defensive stance, increasing defense for 3 turns.",
            "mana_cost": 8,
            "type": "buff",
            "stat": "defense",
            "buff_amount": 0.5,
            "duration": 3,
        },
        {
            "name": "Shield Bash",
            "description": "Bash the enemy with your shield, dealing damage and potentially stunning them.",
            "mana_cost": 12, 
            "type": "attack",
            "damage_multiplier": 1.2, 
            # Could add "stun_chance": 0.3,  for 30% chance to stun if we implement status effects
        },
    ],
    "Mage": [
        {
            "name": "Fireball",
            "description": "Hurl a ball of fire, dealing magical damage.",
            "mana_cost": 15, # 
            "type": "magic_attack",
            "damage_multiplier": 4.0,
            "element": "fire", # 
        },
        {
            "name": "Magic Shield",
            "description": "Create a shield of magic, absorbing incoming damage.",
            "mana_cost": 20, 
            "type": "buff", 
            "stat": "magic_shield", 
            "buff_amount": 10, 
            "duration": 3, 
        },
        {
            "name": "Small Heal",
            "description": "Restore a small amount of health.",
            "mana_cost": 10, 
            "type": "heal",
            "heal_amount": 30, 
        },
    ],
    "Rogue": [
        {
            "name": "Double Attack",
            "description": "Strike twice in quick succession.",
            "mana_cost": 12, 
            "type": "attack", 
            "damage_multiplier": 1.0, 
            "number_of_attacks": 2, 
        },
        {
            "name": "Poison Strike",
            "description": "Apply a venomous poison to your weapon, dealing damage over time.",
            "mana_cost": 15, 
            "type": "attack", 
            "damage_multiplier": 0.8, 
            # Status effect parameters - we'll implement status effects later
            # "status_effect": "poison",
            # "poison_damage_per_turn": 5,
            # "poison_duration": 3,
        },
        {
            "name": "Evasion",
            "description": "Focus on evasion, greatly increasing dodge chance for 1 turn.",
            "mana_cost": 10, 
            "type": "buff",
            "stat": "evasion", 
            "buff_amount": 0.8, 
            "duration": 3,
        },
    ],
}
def generate_quest_list(num_quests=2):
    """Generates a list of quests to be offered to the player."""
    return random.sample(QUEST_DATA, num_quests)

def accept_quest(player, quest):
    """Accepts the given quest, updating game state."""
    player.active_quest = quest
    print(f"Quest accepted: {quest['objective']}")

def check_quest_progress(player, current_enemy=None):
    """Checks and updates quest progress based on player actions."""
    # Here you would add logic to:
    # - Check if the player has completed the objective
    # - Update progress if necessary
    # - Give rewards if the quest is complete
    # (Implementation will depend on how you want to store and manage quests)
    pass  # Replace with actual implementation
def draw_outlined_text(surface, text, font, color, outline_color, position):
    """Draws text with an outline for better readability."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)
    outline_thickness = 2 # Adjust for thicker/thinner outline

    # --- Draw Outline ---
    for dx in [-outline_thickness, 0, outline_thickness]:
        for dy in [-outline_thickness, 0, outline_thickness]:
            if dx == 0 and dy == 0: # Skip the center position (main text handles it)
                continue
            outline_pos = (text_rect.x + dx, text_rect.y + dy)
            outline_surface = font.render(text, True, outline_color)
            surface.blit(outline_surface, outline_pos)

    # --- Draw Main Text ---
    surface.blit(text_surface, position)
def render_status_bar():
    global player, screen
    pygame.draw.rect(screen, GRAY, STATUS_BAR_RECT)

    OUTLINE_COLOR = BLACK
    TEXT_COLOR = WHITE

    # --- XP Bar (Top of Status Bar, Full Width) ---
    exp_bar_width = STATUS_BAR_RECT.width
    exp_bar_height = 10
    exp_bar_x = STATUS_BAR_RECT.x
    exp_bar_y = STATUS_BAR_RECT.y
    exp_ratio = player.experience / player.max_experience
    current_exp_width = int(exp_bar_width * exp_ratio)
    pygame.draw.rect(screen, BLACK, (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height))
    pygame.draw.rect(screen, PURPLE, (exp_bar_x, exp_bar_y, current_exp_width, exp_bar_height))
    exp_text_str = f"XP: {player.experience}/{player.max_experience}"
    exp_text_surface = SMALL_FONT.render(exp_text_str, True, TEXT_COLOR)
    exp_text_rect = exp_text_surface.get_rect(center=(exp_bar_x + exp_bar_width // 2, exp_bar_y + exp_bar_height // 2))
    draw_outlined_text(screen, exp_text_str, SMALL_FONT, TEXT_COLOR, OUTLINE_COLOR, exp_text_rect.topleft)


    # --- Character Name and Class (Side-by-Side above HP Bar) ---
    stats_x = 50
    stats_y = exp_bar_y + exp_bar_height + 10
    stat_font = pygame.font.Font(None, 20)
    line_spacing = 20

    name_text_str = f"Name: {player.name}"
    name_text_surface = stat_font.render(name_text_str, True, TEXT_COLOR)
    name_rect = name_text_surface.get_rect(topleft=(stats_x, stats_y))
    draw_outlined_text(screen, name_text_str, stat_font, TEXT_COLOR, OUTLINE_COLOR, name_rect.topleft)

    class_text_str = f"Class: {player.class_name}"
    class_text_surface = stat_font.render(class_text_str, True, TEXT_COLOR)
    class_rect = class_text_surface.get_rect(topleft=(name_rect.right + 10, stats_y))
    draw_outlined_text(screen, class_text_str, stat_font, TEXT_COLOR, OUTLINE_COLOR, class_rect.topleft)


    # --- Health and Mana Bars (Below Name and Class) ---
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 50
    health_bar_y = stats_y + line_spacing + 10
    health_ratio = player.current_health / player.stats["health"]
    current_health_width = int(health_bar_width * health_ratio)
    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))
    health_text_str = f"HP: {player.current_health}/{player.stats['health']}"
    health_text_surface = SMALL_FONT.render(health_text_str, True, TEXT_COLOR)
    health_text_rect = health_text_surface.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y + health_bar_height // 2))
    draw_outlined_text(screen, health_text_str, SMALL_FONT, TEXT_COLOR, OUTLINE_COLOR, health_text_rect.topleft)


    mana_bar_width = 200
    mana_bar_height = 20
    mana_bar_x = 50
    mana_bar_y = health_bar_y + health_bar_height + 5
    mana_ratio = player.current_mana / player.stats["mana"]
    current_mana_width = int(mana_bar_width * mana_ratio)
    pygame.draw.rect(screen, BLACK, (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height))
    pygame.draw.rect(screen, BLUE, (mana_bar_x, mana_bar_y, current_mana_width, mana_bar_height))
    mana_text_str = f"MP: {player.current_mana}/{player.stats['mana']}"
    mana_text_surface = SMALL_FONT.render(mana_text_str, True, TEXT_COLOR)
    mana_text_rect = mana_text_surface.get_rect(center=(mana_bar_x + mana_bar_width // 2, mana_bar_y + mana_bar_height//2)) #mana_bar_y + health_bar_height // 2))
    draw_outlined_text(screen, mana_text_str, SMALL_FONT, TEXT_COLOR, OUTLINE_COLOR, mana_text_rect.topleft)

    # --- Character Stats (Attack, Defense, Dodge - Right of HP/Mana) ---
    stats_x_right = health_bar_x + health_bar_width + 40
    stats_y_right = stats_y
    stat_font = pygame.font.Font(None, 20)

    # Initialize this variable here:
    attack_defense_stats_y_right = stats_y_right

    # --- Attack Range ---
    attack_range = player.stats['attack']
    # Calculate buffed attack range (for display only)
    min_damage = attack_range[0]
    max_damage = attack_range[1]

    buffed_attack = 0
    percentage_buff_multiplier = 1.0

    for buff in player.buffs:  # Corrected: Use player.buffs
        if buff['stat'] == 'attack_buff':
            if buff.get('is_percentage_buff'):
                percentage_buff_multiplier += buff['amount']
            else:
                buffed_attack += buff['amount']


    # Apply percentage buff first, *then* add the flat buff
    min_damage = round(min_damage * percentage_buff_multiplier)
    max_damage = round(max_damage * percentage_buff_multiplier)

    min_damage += buffed_attack  # Add flat buff to min
    max_damage += buffed_attack  # Add flat buff to max


    attack_range_string = f"Attack: {min_damage}-{max_damage}"
    attack_stat_text_surface = stat_font.render(attack_range_string, True, TEXT_COLOR)
    attack_stat_text_rect = attack_stat_text_surface.get_rect(topleft=(stats_x_right, attack_defense_stats_y_right))
    draw_outlined_text(screen, attack_range_string, stat_font, TEXT_COLOR, OUTLINE_COLOR, attack_stat_text_rect.topleft)
    attack_defense_stats_y_right += line_spacing  # NOW it's safe to increment


    # --- Defense ---
    defense_value = player.get_defense() # Use a method to get this like attack!
    defense_text_str = f"Defense: {defense_value}"
    defense_text_surface = stat_font.render(defense_text_str, True, TEXT_COLOR)
    defense_text_rect = defense_text_surface.get_rect(topleft=(stats_x_right, attack_defense_stats_y_right))
    draw_outlined_text(screen, defense_text_str, stat_font, TEXT_COLOR, OUTLINE_COLOR, defense_text_rect.topleft)
    attack_defense_stats_y_right += line_spacing

    # --- Dodge Chance ---
    dodge_chance = player.get_evasion()
    dodge_text_str = f"Dodge: {dodge_chance}%"
    dodge_text_surface = stat_font.render(dodge_text_str, True, TEXT_COLOR)
    dodge_text_rect = dodge_text_surface.get_rect(topleft=(stats_x_right, attack_defense_stats_y_right))
    draw_outlined_text(screen, dodge_text_str, stat_font, TEXT_COLOR, OUTLINE_COLOR, dodge_text_rect.topleft)
    attack_defense_stats_y_right += line_spacing
     # --- Coins (Below Dodge) ---
    coin_text_str = f"Coins: {player.coins}"
    coin_text_surface = SMALL_FONT.render(coin_text_str, True, TEXT_COLOR)
    coin_text_rect = coin_text_surface.get_rect(topleft=(stats_x_right, attack_defense_stats_y_right))
    draw_outlined_text(screen, coin_text_str, SMALL_FONT, TEXT_COLOR, OUTLINE_COLOR, coin_text_rect.topleft)

     # --- NEW BUFF TEXT LIST DISPLAY SECTION ABOVE BUTTONS ---
    buff_list_rect_x = BUTTON1_RECT.x
    buff_list_rect_y = BUTTON1_RECT.y - 120 #above button 1
    buff_list_rect_width = BUTTON4_RECT.right - BUTTON1_RECT.left
    buff_list_rect_height = 100
    BUFF_TEXT_LIST_RECT = pygame.Rect(buff_list_rect_x, buff_list_rect_y, buff_list_rect_width, buff_list_rect_height) # Define Rect

    # --- ADD BACKGROUND FILL FOR BUFF TEXT LIST RECTANGLE ---
    BUFF_BOX_BACKGROUND_COLOR = (150, 150, 150)  # Example: Light Gray - Adjust as desired!
    pygame.draw.rect(screen, BUFF_BOX_BACKGROUND_COLOR, BUFF_TEXT_LIST_RECT)
    pygame.draw.rect(screen, GRAY, BUFF_TEXT_LIST_RECT, 1)

    buff_list_text_x = BUFF_TEXT_LIST_RECT.x + 10
    buff_list_text_y = BUFF_TEXT_LIST_RECT.y + 10
    buff_text_line_spacing = 18
    current_buff_text_y = buff_list_text_y

    buff_list_title_text_str = "Active Buffs:"
    buff_list_title_text_surface = stat_font.render(buff_list_title_text_str, True, BLACK) # Title in black
    buff_list_title_rect = buff_list_title_text_surface.get_rect(topleft=(buff_list_text_x, current_buff_text_y))
    draw_outlined_text(screen, buff_list_title_text_str, stat_font, BLACK, WHITE, buff_list_title_rect.topleft) # Outlined title (Black main, White outline - reversed colors)
    current_buff_text_y += buff_text_line_spacing + 5

    for buff in player.buffs:
        buff_text_str = f"- {buff['name']} ({buff['duration_turns']} turns)"
        buff_text_surface = stat_font.render(buff_text_str, True, TEXT_COLOR) # Buff text in white
        buff_text_rect = buff_text_surface.get_rect(topleft=(buff_list_text_x, current_buff_text_y))
        draw_outlined_text(screen, buff_text_str, stat_font, TEXT_COLOR, OUTLINE_COLOR, buff_text_rect.topleft)
        current_buff_text_y += buff_text_line_spacing
   # --- Buttons --- (Conditional Text and Highlighting)
    pygame.draw.rect(screen, WHITE, EQUIPMENT_BUTTON_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON1_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON2_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON3_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON4_RECT)


    if CURRENT_STATE in BUTTON_TEXTS:
        button_texts = BUTTON_TEXTS[CURRENT_STATE]
        equipment_button_text = BUTTON_FONT.render("Equip", True, BLACK)
        button1_text = BUTTON_FONT.render(button_texts[0], True, BLACK)  # Use texts from list
        button2_text = BUTTON_FONT.render(button_texts[1], True, BLACK)
        button3_text = BUTTON_FONT.render(button_texts[2], True, BLACK)
        button4_text = BUTTON_FONT.render(button_texts[3], True, BLACK)

        screen.blit(equipment_button_text, equipment_button_text.get_rect(center=EQUIPMENT_BUTTON_RECT.center))
        screen.blit(button1_text, button1_text.get_rect(center=BUTTON1_RECT.center))
        screen.blit(button2_text, button2_text.get_rect(center=BUTTON2_RECT.center))
        screen.blit(button3_text, button3_text.get_rect(center=BUTTON3_RECT.center))
        screen.blit(button4_text, button4_text.get_rect(center=BUTTON4_RECT.center))
    # --- Combat-Specific Button Changes ---
    if CURRENT_STATE == COMBAT:
        items_button_text = BUTTON_FONT.render("Items", True, BLACK)
        screen.blit(items_button_text, items_button_text.get_rect(center=BUTTON3_RECT.center)) # Blit the new text
    # --- SHOP-Specific Button Changes ---
    if CURRENT_STATE == SHOP:
        button1_text = BUTTON_FONT.render("Buy", True, BLACK)
        button2_text = BUTTON_FONT.render("Sell", True, BLACK)
        screen.blit(button1_text, button1_text.get_rect(center=BUTTON1_RECT.center))
        screen.blit(button2_text, button2_text.get_rect(center=BUTTON2_RECT.center))

    render_combat_buttons() #keep combat buttons.

def render_monster_status_bar():
    global current_enemy
    if current_enemy:
        status_bar_x = 0
        status_bar_y = 0
        status_bar_width = SCREEN_WIDTH
        status_bar_height = 80
        STATUS_BAR_RECT = pygame.Rect(status_bar_x, status_bar_y, status_bar_width, status_bar_height)

        pygame.draw.rect(screen, GRAY, STATUS_BAR_RECT)  # Background

        stat_font = pygame.font.Font(None, 24)
        line_spacing = 24

        # --- Monster Name and Type (Top Left, side-by-side) ---
        name_text = stat_font.render(f"Name: {current_enemy.get_name()}", True, WHITE)
        name_rect = name_text.get_rect(topleft=(status_bar_x + 10, status_bar_y + 10))
        # Use draw_outlined_text:
        draw_outlined_text(screen, f"Name: {current_enemy.get_name()}", stat_font, WHITE, BLACK, name_rect.topleft)


        type_text = stat_font.render(f"Type: {current_enemy.monster_type}", True, WHITE)
        type_rect = type_text.get_rect(topleft=(name_rect.right + 10, status_bar_y + 10))
        # Use draw_outlined_text:
        draw_outlined_text(screen, f"Type: {current_enemy.monster_type}", stat_font, WHITE, BLACK, type_rect.topleft)


        # --- Health Bar (Under Name & Type, Spanning Width) ---
        health_bar_width = name_rect.width + type_rect.width + 20
        health_bar_height = 20
        health_bar_x = status_bar_x + 10
        health_bar_y = name_rect.bottom + 5
        health_ratio = current_enemy.current_health / current_enemy.stats["health"] if current_enemy.stats["health"] > 0 else 0
        current_health_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))
        health_text = SMALL_FONT.render(f"HP: {current_enemy.current_health}/{current_enemy.stats['health']}", True, BLACK)
        health_text_rect = health_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y + health_bar_height // 2))
        screen.blit(health_text, health_text_rect) #keep as is

        # --- Attack, Defense, Dodge Stats (Right Column) ---
        attack_defense_stats_x = type_rect.right + 50
        attack_defense_stats_y = status_bar_y + 10

        attack_range = current_enemy.stats['attack']
        min_attack_value = attack_range[0]
        max_attack_value = attack_range[1]
        buffed_min_attack = min_attack_value
        buffed_max_attack = max_attack_value
        percentage_attack_buff_multiplier = 1.0
        for buff in current_enemy.buffs:
            if buff['stat'] == 'attack_buff':
                if buff.get('is_percentage_buff'):
                    percentage_attack_buff_multiplier += buff['amount']
                else:
                    buffed_min_attack += buff['amount']
                    buffed_max_attack += buff['amount']

        buffed_min_attack = int(buffed_min_attack * percentage_attack_buff_multiplier)
        buffed_max_attack = int(buffed_max_attack * percentage_attack_buff_multiplier)

        attack_range_string = f"Attack: {buffed_min_attack}-{buffed_max_attack}"
        # Use draw_outlined_text:
        draw_outlined_text(screen, attack_range_string, stat_font, WHITE, BLACK, (attack_defense_stats_x, attack_defense_stats_y))
        attack_defense_stats_y += line_spacing

        defense_value = current_enemy.get_defense()
        defense_text = stat_font.render(f"Defense: {defense_value}", True, WHITE)
        # Use draw_outlined_text:
        draw_outlined_text(screen, f"Defense: {defense_value}", stat_font, WHITE, BLACK, (attack_defense_stats_x, attack_defense_stats_y))
        attack_defense_stats_y += line_spacing

        dodge_chance = current_enemy.get_evasion()
        # Use draw_outlined_text:
        draw_outlined_text(screen, f"Dodge: {dodge_chance}%", stat_font, WHITE, BLACK, (attack_defense_stats_x, attack_defense_stats_y))
        attack_defense_stats_y += line_spacing

        # --- Buffs Display Section (Monster Buffs) ---
        buff_display_x = attack_defense_stats_x + 150
        buff_display_y = status_bar_y + 10
        # Use draw_outlined_text for the title:
        draw_outlined_text(screen, "Buffs:", stat_font, WHITE, BLACK, (buff_display_x, buff_display_y))
        buff_display_y += line_spacing

        for buff in current_enemy.buffs:
            # Use draw_outlined_text for each buff:
            buff_text_str = f"- {buff['name']} ({buff['duration_turns']} turns)"
            draw_outlined_text(screen, buff_text_str, stat_font, WHITE, BLACK, (buff_display_x, buff_display_y))
            buff_display_y += line_spacing

def render_combat_log():
    global combat_log_messages
    combat_log_rect = pygame.Rect(COMBAT_LOG_X, COMBAT_LOG_Y, COMBAT_LOG_WIDTH, COMBAT_LOG_HEIGHT)

    # --- Draw Solid Background ---
    pygame.draw.rect(screen, COMBAT_LOG_BG_COLOR, combat_log_rect)

    if COMBAT_LOG_BORDER_WIDTH > 0: # Optional border
        pygame.draw.rect(screen, COMBAT_LOG_BORDER_COLOR, combat_log_rect, COMBAT_LOG_BORDER_WIDTH)

    # --- Render Combat Log Messages (Scrolling Logic) ---
    log_y_offset = COMBAT_LOG_Y + COMBAT_LOG_HEIGHT - 10  # Start Y at the *bottom* of the log area, with padding
    line_spacing = 20
    max_lines_visible = COMBAT_LOG_HEIGHT // line_spacing  # Calculate max lines based on log height and line spacing
    max_messages_to_display = min(len(combat_log_messages), max_lines_visible) # Display up to max lines or all messages

    messages_to_render = combat_log_messages[-max_messages_to_display:] # Get the *last* 'max_messages_to_display' messages (newest)

    for message in reversed(messages_to_render): # Iterate through messages in *reverse* order (newest to oldest)
        text_surface = SMALL_FONT.render(message, True, COMBAT_LOG_TEXT_COLOR)
        text_rect = text_surface.get_rect(bottomleft=(COMBAT_LOG_X + 10, log_y_offset)) # Position text at bottom-left, adjust Y offset upwards
        screen.blit(text_surface, text_rect)
        log_y_offset -= line_spacing # Move Y position *upwards* for the next (older) message

def add_combat_message(message): 
    global combat_log_messages
    combat_log_messages.append(message) 
    max_messages_history = 50  
    if len(combat_log_messages) > max_messages_history:
        combat_log_messages.pop(0) 
#Monster Classes
class Monster:
    def __init__(self, name, monster_type, health, attack_damage, defense, accuracy, evasion, experience, gold, image_path, abilities):
        self.name = name
        self.monster_type = monster_type
        self.stats = {
            "health": health,
            "attack": attack_damage,
            "defense": defense,
            "accuracy": accuracy,
            "evasion": evasion
        }
        self.current_health = health
        self.experience = experience
        self.gold = gold
        # --- USE resource_path HERE! ---
        full_image_path = resource_path(image_path) # Get FULL resource path
        self.image = pygame.image.load(full_image_path).convert_alpha() # Load image using FULL path
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.buffs = []  # <--- Use buffs instead of statuses, initialize as empty list
        self.abilities = abilities

    def choose_ability(self, target):
        if not self.abilities:
            return None
        ability_chance = 0.3
        if random.random() < ability_chance:
            ability_set_name = self.abilities[0]
            ability_choices = MONSTER_ABILITIES.get(ability_set_name)
            if ability_choices:
                chosen_ability = random.choice(ability_choices)
                return chosen_ability
        return None

    def use_ability(self, ability, target):
        ability_name = ability['name']
        if ability['type'] == 'attack':
            damage_multiplier = ability.get('damage_multiplier', 1.0)
            base_damage = self.get_attack_damage()
            damage = max(0, int(base_damage * damage_multiplier) - target.get_defense())
            damage_dealt = target.take_damage(damage)
            message_text = (f"{self.name} uses {ability_name} and hits you for {damage_dealt} damage!") # <--- MESSAGE including ability name and damage
            add_combat_message(message_text) # <--- ADD add_combat_message to log damage from ability

        elif ability['type'] == 'buff':
            buff_stat = ability['stat']
            buff_amount = ability['buff_amount']
            duration_turns = ability['duration_turns']
            buff_name = ability['name']

            buff_dict = {  # <--- CORRECT WAY TO CREATE buff_dict - DICTIONARY
                'name': ability_name,  # or buff_name if ability_name and buff_name are the same here
                'stat': buff_stat,
                'amount': buff_amount,  # Corrected key name here
                'duration_turns': duration_turns,
                'is_percentage_buff': ability.get('is_percentage_buff', False) #get the percentage
            }

            print("Monster Buff Ability - Debug Info:")  # <--- ADD DEBUG PRINTING
            print("  Ability Name:", ability_name)
            print("  Buff Stat:", buff_stat)
            print("  Buff Amount:", buff_amount)
            print("  Buff Dict:", buff_dict)
            self.apply_buff(buff_dict)  # Apply to SELF
            message_text = (f"{self.name} uses {ability_name} and buffs its {buff_stat} by {buff_amount * 100 if buff_dict['is_percentage_buff'] else buff_amount}% for {duration_turns} turns!")
            add_combat_message(message_text)

        elif ability['type'] == 'debuff':
            debuff_stat = ability['stat']
            debuff_amount = ability['buff_amount']  # Corrected key name
            duration_turns = ability['duration_turns']
            debuff_name = ability['name']

            # --- CORRECTLY CREATE debuff_dict ---
            debuff_dict = {
                'name': debuff_name,
                'stat': debuff_stat,
                'amount': debuff_amount,  # Corrected key name
                'duration_turns': duration_turns,
                'is_percentage_buff': ability.get('is_percentage_buff', False)  # Get is_percentage, default to False
            }
            target.apply_buff(debuff_dict)  # Apply to TARGET (the player)
            message_text = (f"{self.name} uses {ability_name} and debuffs your {debuff_stat} by {abs(debuff_amount) * 100 if debuff_dict['is_percentage_buff'] else abs(debuff_amount)}% for {duration_turns} turns!")
            add_combat_message(message_text)


        else:
            print(f"{self.name} tried to use unknown ability type: {ability['type']}")
    def get_evasion(self):
        buffed_evasion_percentage = self.stats['evasion']
        for buff in self.buffs:
            print(f"  Inspecting buff: {buff}")
            if buff.get('stat') == 'evasion_buff':
                print(f"   Found evasion buff: {buff}")
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['amount']  # Access 'amount' here
                    buffed_evasion_percentage += percentage_increase
                else:
                    buffed_evasion_percentage += buff['amount'] # Access 'amount' here
        buffed_evasion_percentage = max(0, buffed_evasion_percentage) # prevent below 0
        return buffed_evasion_percentage
    def get_accuracy(self):
        """Retrieves monster accuracy, including buffs, returning WHOLE NUMBER PERCENTAGE (0-100)."""
        base_accuracy_percentage = self.stats['accuracy']
        buffed_accuracy_percentage = base_accuracy_percentage

        for buff in self.buffs:  # <--- Iterate through buffs, not statuses
            if buff.get('stat') == 'accuracy_buff':
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['amount']
                    buffed_accuracy_percentage += percentage_increase
                else:
                    buffed_accuracy_percentage += buff['amount']  # Corrected key name

        buffed_accuracy_percentage = max(0, buffed_accuracy_percentage) # prevent below 0
        return int(buffed_accuracy_percentage)  # Return as integer
    def apply_buff(self, buff_data):
        """Applies a buff to the monster, handling duration and refresh."""
        buff_name = buff_data['name']
        buff_stat = buff_data['stat']
        buff_duration = buff_data.get('duration_turns', 3)  # Use .get() with a default value
        #buff_type = buff_data.get('buff_type') #not needed

        print(f"{self.name} applying buff: Name='{buff_name}', Stat='{buff_stat}'")

        existing_buff_index = -1
        for index, buff in enumerate(self.buffs):
            if buff['name'] == buff_name and buff['stat'] == buff_stat:
                existing_buff_index = index
                break

        if existing_buff_index != -1:
            self.buffs[existing_buff_index]['duration_turns'] = buff_duration
            print(f"  Buff '{buff_name}' duration refreshed on {self.name}.")
        else:
            buff = buff_data.copy()  # Make a copy to avoid modifying the original
            buff['duration_turns'] = buff_duration
            self.buffs.append(buff)
            print(f"  {self.name} buffed with '{buff_name}'!")
    def update_buff_durations(self):
        """Updates buff durations for the monster, removing expired buffs."""
        buffs_to_remove = []
        for buff in self.buffs:  # <--- Iterate through buffs, not statuses
            buff['duration_turns'] -= 1  # Use 'duration_turns'
            if buff['duration_turns'] <= 0:
                buffs_to_remove.append(buff)
                print(f"Buff '{buff['name']}' expired from {self.name}.")

        for buff in buffs_to_remove:
            self.buffs.remove(buff)

    def get_name(self):
        return self.name
    def get_health(self):
        return self.current_health
    def take_damage(self, damage):
        damage_taken = max(0, damage)  # Ensure damage is not negative
        self.current_health -= damage_taken
        return damage_taken
    def get_experience(self):
        return self.experience
    def get_attack_damage(self):
        """Gets attack damage (now with a range)."""
        attack_range = self.stats["attack"]
        min_damage = attack_range[0]
        max_damage = attack_range[1]
        return random.randint(min_damage, max_damage)
    def get_defense(self):
      return self.stats["defense"]
    def is_alive(self):
        return self.current_health > 0
    def is_stunned(self):
        for buff in self.buffs:  # <--- Check buffs list, not statuses
            if buff["name"] == "stun" and buff["duration_turns"] > 0:  # Check 'duration_turns'
                return True
        return False
    def attack(self, target):
        """Monster attacks a target (player)."""
        if self.is_stunned():
            message_text = (f"{self.get_name()} is stunned and cannot attack!")
            add_combat_message(message_text)
            print(f"{self.get_name()} is stunned and cannot attack!")
            return 0

        # --- Accuracy Check ---
        accuracy_roll = random.random()
        monster_accuracy_percentage = self.get_accuracy()
        monster_accuracy_decimal = monster_accuracy_percentage / 100.0

        print(f"Debug (Accuracy Check): Monster: {self.get_name()}, Accuracy Roll: {accuracy_roll:.2f}, Monster Accuracy: {int(monster_accuracy_percentage)}%")

        if accuracy_roll < monster_accuracy_decimal:
            print(f"Debug (Accuracy Check): Accuracy check passed for {self.get_name()}.")

            # --- Evasion Check ---
            evasion_roll = random.random()
            player_evasion_percentage = target.get_evasion()
            player_evasion_decimal = player_evasion_percentage / 100.0

            print(f"Debug (Evasion Check): Monster: {self.get_name()}, Player: {target.get_name()}, Evasion Roll: {evasion_roll:.2f}, Player Evasion: {int(player_evasion_percentage)}%")

            if evasion_roll < player_evasion_decimal:
                message_text = (f"{target.get_name()} dodged the attack from the {self.get_name()}!") # Message for DODGE
                add_combat_message(message_text)
                print(f"{target.get_name()} dodged the attack from the {self.get_name()}!")
                return 0

            else:  # Hit and Damage
                print(f"Debug (Evasion Check): Evasion check failed - proceeding with hit.")
                attack_range = self.stats['attack']
                base_damage = random.randint(attack_range[0], attack_range[1])
                damage = max(0, base_damage - target.get_defense())
                print(f"Debug: {self.get_name()} attacks {target.get_name()}, Damage: {damage}")
                damage_dealt = target.take_damage(damage)
                if damage_dealt > 0:  # Damage was actually dealt (after defense)
                    message_text = (f"{self.get_name()} attacks you for {damage_dealt} damage!")  # Message for DAMAGE dealt
                    add_combat_message(message_text)
                    print(f"{self.get_name()} attacks you and for {damage_dealt} damage!")
                else:  # Damage was zero because of defense
                    message_text = (f"{self.get_name()}'s attack was blocked by your defense!")  # <--- NEW MESSAGE: Attack BLOCKED by defense
                    add_combat_message(message_text)
                    print(f"{self.get_name()} attacks you but deals no damage!")  # Keep print if needed
                return damage_dealt
        else:  # Miss due to inaccuracy
            message_text = (f"{self.get_name()} attacks but misses you!")  # Message for TRUE MISS due to inaccuracy
            add_combat_message(message_text)
            return 0
        
def get_monster_stat_multiplier_by_floor(roomlvl): # Use roomlvl as parameter
    """Calculates monster stat multiplier based on dungeon roomlvl."""
    multiplier = 1.0 + (roomlvl) * 0.25  # 25% increase per roomlvl
    return multiplier
monster_data = {
    "Goblin": {
        "name": "Goblin",
        "health": 40,
        "attack": [5, 9],
        "defense": 3,
        "experience": 25,
        "description": "A more aggressive and tougher green-skinned pest.",
        "gold_min": 5,
        "gold_max": 10,
        "image": None,
        "accuracy": 65,
        "evasion": 20,
        "monster_type": "Greenskin",
        "image_path": "images/Goblin.png",
        "attack_sound_path": "sounds/goblin_attack.wav",
        "abilities": ["Goblin Abilities"]
    },
    "Rat": {
        "name": "Rat",
        "health": 10,
        "attack": [2, 4],
        "defense": 1,
        "experience": 15,
        "description": "Still rats, but these ones bite harder!",
        "gold_min": 0,
        "gold_max": 2,
        "image": None,
        "accuracy": 75,
        "evasion": 30,
        "monster_type": "Beast",
        "image_path": "images/rat.png",
        "attack_sound_path": "sounds/rat_attack.wav",
        "abilities": []
    },
    "Big Rat": {
        "name": "Big Rat",
        "health": 25,
        "attack": [4, 7],
        "defense": 2,
        "experience": 30,
        "description": "This Big Rat is truly menacing now!",
        "gold_min": 2,
        "gold_max": 6,
        "image": None,
        "accuracy": 70,
        "evasion": 27,
        "monster_type": "Beast",
        "image_path": "images/bigrat.png",
        "attack_sound_path": "sounds/rat_attack.wav",
        "abilities": []
    },
    "Spider": {
        "name": "Spider",
        "health": 30,
        "attack": [5, 8],
        "defense": 2,
        "experience": 30,
        "description": "Larger and more venomous spiders infest these levels.",
        "gold_min": 4,
        "gold_max": 9,
        "image": None,
        "accuracy": 70,
        "evasion": 45,
        "monster_type": "Beast",
        "image_path": "images/spider.png",
        "attack_sound_path": "sounds/spider_attack.wav",
        "abilities": []
    },
    "Skeleton Warrior": {
        "name": "Skeleton Warrior",
        "health": 80,
        "attack": [9, 15],
        "defense": 9,
        "experience": 70,
        "description": "Elite undead warriors, clad in decaying armor and wielding rusty weapons.",
        "gold_min": 8,
        "gold_max": 18,
        "image": None,
        "accuracy": 80,
        "evasion": 15,
        "monster_type": "Undead",
        "image_path": "images/skeleton_warrior.png",
        "attack_sound_path": "sounds/skeleton_attack.wav",
        "abilities": []
    },
    "Giant Rat": {
        "name": "Giant Rat",
        "health": 45,
        "attack": [7, 11],
        "defense": 4,
        "experience": 60,
        "description": "These Giant Rats are apex predators of the dungeon depths!",
        "gold_min": 5,
        "gold_max": 15,
        "image": None,
        "accuracy": 80,
        "evasion": 30,
        "monster_type": "Beast",
        "image_path": "images/giant_rat.png",
        "attack_sound_path": "sounds/rat_attack.wav",
        "abilities": []
    },
    "Siren": {
        "name": "Siren",
        "health": 60,
        "attack": [8, 13],
        "defense": 4,
        "experience": 75,
        "description": "Their enchanting songs mask deadly intent and sharp claws.",
        "gold_min": 10,
        "gold_max": 22,
        "image": None,
        "accuracy": 90,
        "evasion": 35,
        "monster_type": "Fey",
        "image_path": "images/siren.png",
        "attack_sound_path": "sounds/siren_attack.wav",
        "abilities": []
    },
    "Mimic": {
        "name": "Mimic",
        "health": 55,
        "attack": [9, 16],
        "defense": 12,
        "experience": 80,
        "description": "Deceptively sturdy, these treasure chests bite back with surprising ferocity!",
        "gold_min": 20,
        "gold_max": 40,
        "image": None,
        "accuracy": 75,
        "evasion": 20,
        "monster_type": "Construct",
        "image_path": "images/mimic.png",
        "attack_sound_path": "sounds/mimic_attack.wav",
        "abilities": []
    },
    "Orc": {
        "name": "Orc",
        "health": 120,
        "attack": [13, 19],
        "defense": 8,
        "experience": 120,
        "description": "Brutal Orcish warriors, masters of axe and carnage!",
        "gold_min": 15,
        "gold_max": 30,
        "image": None,
        "accuracy": 85,
        "evasion": 15,
        "monster_type": "Greenskin",
        "image_path": "images/orc.png",
        "attack_sound_path": "sounds/orc_attack.wav",
        "abilities": ["Orc Abilities"]
    },
    "Succubus": {
        "name": "Succubus",
        "health": 80,
        "attack": [12, 18],
        "defense": 5,
        "experience": 120,
        "description": "Even more alluring and sinister in the deeper levels, their charm is deadly.",
        "gold_min": 25,
        "gold_max": 50,
        "image": None,
        "accuracy": 85,
        "evasion": 45,
        "monster_type": "Fiend",
        "image_path": "images/succubus.png",
        "attack_sound_path": "sounds/succubus_charm.wav",
        "abilities": []
    },
    "Lich": {
        "name": "Lich",
        "health": 150,
        "attack": [15, 22],
        "defense": 10,
        "experience": 150,
        "description": "Undead sorcerers wielding necromantic power, truly formidable foes.",
        "gold_min": 30,
        "gold_max": 60,
        "image": None,
        "accuracy": 95,
        "evasion": 20,
        "monster_type": "Undead",
        "image_path": "images/lich.png",
        "attack_sound_path": "sounds/lich_attack.wav",
        "abilities": []
    },
    "Dragon": {
        "name": "Dragon",
        "health": 350,
        "attack": [25, 35],
        "defense": 20,
        "experience": 300,
        "description": "A true apex predator, its fiery breath and armored scales spell doom!",
        "gold_min": 100,
        "gold_max": 200,
        "image": None,
        "accuracy": 95,
        "evasion": 35,
        "monster_type": "Dragon",
        "image_path": "images/dragon.png",
        "attack_sound_path": "sounds/dragon_roar.wav",
        "abilities": []
    }
}
MONSTER_ABILITIES = {
    "Goblin Abilities": [  # Abilities for Goblins - this name is referenced in monster_data for Goblin
        {
            "name": "Quick Strike",
            "description": "A fast attack that can sometimes hit twice.",
            "type": "attack",
            "damage_multiplier": 1.1,  # Slightly increased damage (110% of normal attack)
        },
        {
            "name": "Nimble Dodge",
            "description": "A quick dodge, increasing evasion for 2 turns.",
            "type": "buff",
            "stat": "evasion_buff", 
            "buff_amount": 15, 
            "duration_turns": 2,
            "is_percentage_buff": True 
        }
    ],
    "Orc Abilities": [  # Abilities for Orcs - this name is referenced in monster_data for Orc
        {
            "name": "Power Slam",
            "description": "A heavy slam that deals significant damage.",
            "type": "attack",
            "damage_multiplier": 1.8,  # High damage (180% of normal attack)
        },
        {
            "name": "Fearsome Roar",
            "description": "A terrifying roar that decreases player attack (attack debuff) for 3 turns.",
            "type": "debuff",
            "stat": "attack_buff",  # Correctly using "attack_buff" for attack debuff
            "buff_amount": -10,     # <--- CORRECTED to whole number percentage (-10%)
            "duration_turns": 3,
            "is_percentage_buff": True # <--- ADDED to specify percentage debuff
        },
    ],
    "Spider Abilities": [
        {
            "name": "Venomous Bite",
            "description": "A bite that deals poison damage over time.",
            "type": "attack",
            "damage_multiplier": 1.0, # Normal damage
            # In a more advanced system, you could add "status_effect": "poison", "poison_damage": 5, "poison_duration": 3
            # For now, we'll keep it simpler and just focus on attack/buff/debuff types.
        }
    ],
    "Skeleton Warrior Abilities": [
        {
            "name": "Crushing Blow",
            "description": "A slow but powerful attack that can lower enemy defense.",
            "type": "attack",
            "damage_multiplier": 1.5, # Increased damage
            # In a more advanced system, you could add "debuff_effect": "defense_debuff", "debuff_amount": -0.10, "debuff_duration": 2
        },
        {
            "name": "Undead Resilience",
            "description": "Undead resilience temporarily boosts defense.",
            "type": "buff",
            "stat": "defense_buff",
            "buff_amount": 0.20, # 20% defense buff
            "duration_turns": 2,
        }
    ],
    "Giant Rat Abilities": [
        {
            "name": "Gnawing Bite",
            "description": "A flurry of bites that can sometimes cause bleeding.",
            "type": "attack",
            "damage_multiplier": 1.2, # Slightly increased damage
            # In a more advanced system, you could add "status_effect": "bleed", "bleed_damage": 3, "bleed_duration": 2
        }
    ],
    "Siren Abilities": [
        {
            "name": "Enchanting Song",
            "description": "A mesmerizing song that can lower enemy accuracy (evasion debuff).",
            "type": "debuff",
            "stat": "evasion", # Debuffing evasion makes the target easier to hit
            "buff_amount": -0.15, # -15% evasion debuff
            "duration_turns": 3,
        },
        {
            "name": "Sharp Claws",
            "description": "A swift claw attack.",
            "type": "attack",
            "damage_multiplier": 1.1, # Slightly increased damage
        }
    ],
    "Mimic Abilities": [
        {
            "name": "Surprise Attack!",
            "description": "A powerful opening attack when the Mimic reveals itself.",
            "type": "attack",
            "damage_multiplier": 2.0, # High damage, represents surprise and strong bite
        },
        {
            "name": "Harden Shell",
            "description": "Mimics hardens its shell, greatly increasing defense.",
            "type": "buff",
            "stat": "defense_buff",
            "buff_amount": 0.40, # 40% defense buff - Mimics become very tanky
            "duration_turns": 3,
        }
    ],
    "Lich Abilities": [
        {
            "name": "Necrotic Bolt",
            "description": "A bolt of necrotic energy dealing increased damage and draining mana.",
            "type": "attack",
            "damage_multiplier": 1.6, # Increased damage
            # In a more advanced system, you could add "mana_drain": 5
        },
        {
            "name": "Frost Armor",
            "description": "Summons frost armor, increasing defense and chilling attackers.",
            "type": "buff",
            "stat": "defense_buff",
            "buff_amount": 0.25, # 25% defense buff
            "duration_turns": 3,
            # In a more advanced system, you could add "on_hit_effect": "chill", "chill_chance": 0.2
        }
    ],
    "Dragon Abilities": [
        {
            "name": "Fiery Breath",
            "description": "Unleashes a cone of fire, dealing massive damage.",
            "type": "attack",
            "damage_multiplier": 2.5, # Very high damage - Dragon's signature move
            # Could be AoE in a more advanced system
        },
        {
            "name": "Dragon Scales",
            "description": "Reinforces scales, granting incredibly high defense.",
            "type": "buff",
            "stat": "defense_buff",
            "buff_amount": 0.60, # 60% defense buff - Dragons become incredibly tanky
            "duration_turns": 4, # Long duration to represent tough scales
        },
        {
            "name": "Tail Swipe",
            "description": "A powerful tail swipe that can knock back and stun.",
            "type": "attack",
            "damage_multiplier": 1.3, # Moderate damage
            # In a more advanced system, you could add "status_effect": "stun", "stun_chance": 0.4
        }
    ],
    "Succubus Abilities": [
        {
            "name": "Life Drain Kiss",
            "description": "Steals life force, damaging enemy and healing the Succubus.",
            "type": "attack",
            "damage_multiplier": 1.4, # Increased damage
            # In a more advanced system, you could add "heal_self_percentage": 0.3
        },
        {
            "name": "Alluring Gaze",
            "description": "Reduces enemy accuracy with a mesmerizing gaze.",
            "type": "debuff",
            "stat": "accuracy", # Debuffing accuracy makes the target less likely to hit
            "buff_amount": -0.20, # -20% accuracy debuff
            "duration_turns": 3,
        }
    ]
}

shop_items_data = {
    # --- Weapons ---
    "weapon_001": {"name": "Rusty Dagger", "category": "Weapons", "price": 10, "equip_slot": "main_hand","stats_bonus": {"attack": [1, 3]}, "image_path": "images/items/weapons/weapon_001.png"},
    "weapon_002": {"name": "Short Sword", "category": "Weapons", "price": 25, "equip_slot": "main_hand","stats_bonus": {"attack": [2, 5]}, "image_path": "images/items/weapons/weapon_002.png"},
    "weapon_003": {"name": "Iron Axe", "category": "Weapons", "price": 35, "equip_slot": "main_hand", "stats_bonus": {"attack": [3, 7]}, "image_path": "images/items/weapons/weapon_003.png"},
    "weapon_004": {"name": "Steel Sword", "category": "Weapons", "price": 50, "equip_slot": "main_hand", "stats_bonus": {"attack": [4, 9]}, "image_path": "images/items/weapons/weapon_004.png"},
    "weapon_005": {"name": "Mace", "category": "Weapons", "price": 40, "equip_slot": "main_hand", "stats_bonus": {"attack": [5, 8], "accuracy": 2}, "image_path": "images/items/weapons/weapon_005.png"},
    "weapon_006": {"name": "Broadsword", "category": "Weapons", "price": 75, "equip_slot": "main_hand", "stats_bonus": {"attack": [6, 11]}, "image_path": "images/items/weapons/weapon_006.png"},
    "weapon_007": {"name": "War Hammer", "category": "Weapons", "price": 90, "equip_slot": "main_hand", "stats_bonus": {"attack": [8, 12], "accuracy": -1}, "image_path": "images/items/weapons/weapon_007.png"},
    "weapon_008": {"name": "Scimitar", "category": "Weapons", "price": 80, "equip_slot": "main_hand", "stats_bonus": {"attack": [7, 10], "evasion": 2}, "image_path": "images/items/weapons/weapon_008.png"},
    "weapon_009": {"name": "Silver Dagger", "category": "Weapons", "price": 120, "equip_slot": "main_hand", "stats_bonus": {"attack": [9, 14]}, "image_path": "images/items/weapons/weapon_009.png"},
    "weapon_010": {"name": "Longsword", "category": "Weapons", "price": 110, "equip_slot": "main_hand", "stats_bonus": {"attack": [10, 16]}, "image_path": "images/items/weapons/weapon_010.png"},
    "weapon_011": {"name": "Battle Axe", "category": "Weapons", "price": 150, "equip_slot": "main_hand", "stats_bonus": {"attack": [12, 18], "accuracy": 1}, "image_path": "images/items/weapons/weapon_011.png"},
    "weapon_012": {"name": "Flaming Sword", "category": "Weapons", "price": 200, "equip_slot": "main_hand", "stats_bonus": {"attack": [14, 20], "defense": 1}, "image_path": "images/items/weapons/weapon_012.png"},
    "weapon_013": {"name": "Frost Mace", "category": "Weapons", "price": 180, "equip_slot": "main_hand", "stats_bonus": {"attack": [13, 19]}, "image_path": "images/items/weapons/weapon_013.png"},
    "weapon_014": {"name": "Greatsword", "category": "Weapons", "price": 220, "equip_slot": "main_hand", "stats_bonus": {"attack": [16, 23]}, "image_path": "images/items/weapons/weapon_014.png"},
    "weapon_015": {"name": "Halberd", "category": "Weapons", "price": 210, "equip_slot": "main_hand", "stats_bonus": {"attack": [15, 22], "evasion": 1}, "image_path": "images/items/weapons/weapon_015.png"},
    "weapon_016": {"name": "Golden Axe", "category": "Weapons", "price": 250, "equip_slot": "main_hand", "stats_bonus": {"attack": [18, 25]}, "image_path": "images/items/weapons/weapon_016.png"},
    "weapon_017": {"name": "Blessed Blade", "category": "Weapons", "price": 280, "equip_slot": "main_hand", "stats_bonus": {"attack": [20, 27], "accuracy": 3}, "image_path": "images/items/weapons/weapon_017.png"},
    "weapon_018": {"name": "Cursed Scythe", "category": "Weapons", "price": 260, "equip_slot": "main_hand", "stats_bonus": {"attack": [22, 26], "health": -5}, "image_path": "images/items/weapons/weapon_018.png"},
    "weapon_019": {"name": "Dragonslayer", "category": "Weapons", "price": 350, "equip_slot": "main_hand", "stats_bonus": {"attack": [24, 30]}, "image_path": "images/items/weapons/weapon_019.png"},
    "weapon_020": {"name": "Stormcaller", "category": "Weapons", "price": 320, "equip_slot": "main_hand", "stats_bonus": {"attack": [21, 28], "mana": 5}, "image_path": "images/items/weapons/weapon_020.png"},
    "weapon_021": {"name": "Rune Sword", "category": "Weapons", "price": 300, "equip_slot": "main_hand", "stats_bonus": {"attack": [19, 26], "accuracy": 2}, "image_path": "images/items/weapons/weapon_021.png"},
    "weapon_022": {"name": "Warbringer", "category": "Weapons", "price": 380, "equip_slot": "main_hand", "stats_bonus": {"attack": [26, 33]}, "image_path": "images/items/weapons/weapon_022.png"},
    "weapon_023": {"name": "Soul Reaver", "category": "Weapons", "price": 400, "equip_slot": "main_hand", "stats_bonus": {"attack": [28, 35], "health": 2}, "image_path": "images/items/weapons/weapon_023.png"},
    "weapon_024": {"name": "Lightbringer", "category": "Weapons", "price": 420, "equip_slot": "main_hand", "stats_bonus": {"attack": [25, 32], "defense": 3}, "image_path": "images/items/weapons/weapon_024.png"},
    "weapon_025": {"name": "Kingsblade", "category": "Weapons", "price": 500, "equip_slot": "main_hand", "stats_bonus": {"attack": [30, 40]}, "image_path": "images/items/weapons/weapon_025.png"},

    # --- Armor ---
    "armor_001": {"name": "Cloth Tunic", "category": "Armor", "price": 15, "equip_slot": "chest", "stats_bonus": {"defense": 1}, "image_path": "images/items/armor/armor_001.png"},
    "armor_002": {"name": "Leather Armor", "category": "Armor", "price": 30, "equip_slot": "chest", "stats_bonus": {"defense": 2, "evasion": 1}, "image_path": "images/items/armor/armor_002.png"},
    "armor_003": {"name": "Studded Leather", "category": "Armor", "price": 45, "equip_slot": "chest", "stats_bonus": {"defense": 3, "evasion": 1}, "image_path": "images/items/armor/armor_003.png"},
    "armor_004": {"name": "Chainmail", "category": "Armor", "price": 60, "equip_slot": "chest", "stats_bonus": {"defense": 4}, "image_path": "images/items/armor/armor_004.png"},
    "armor_005": {"name": "Scale Mail", "category": "Armor", "price": 75, "equip_slot": "chest", "stats_bonus": {"defense": 5, "evasion": -1}, "image_path": "images/items/armor/armor_005.png"},
    "armor_006": {"name": "Bronze Plate", "category": "Armor", "price": 100, "equip_slot": "chest", "stats_bonus": {"defense": 6}, "image_path": "images/items/armor/armor_006.png"},
    "armor_007": {"name": "Steel Plate", "category": "Armor", "price": 120, "equip_slot": "chest", "stats_bonus": {"defense": 7}, "image_path": "images/items/armor/armor_007.png"},
    "armor_008": {"name": "Elven Chainmail", "category": "Armor", "price": 150, "equip_slot": "chest", "stats_bonus": {"defense": 5, "evasion": 3}, "image_path": "images/items/armor/armor_008.png"},
    "armor_009": {"name": "Mithril Armor", "category": "Armor", "price": 200, "equip_slot": "chest", "stats_bonus": {"defense": 8, "evasion": 1}, "image_path": "images/items/armor/armor_009.png"},
    "armor_010": {"name": "Dragonscale Armor", "category": "Armor", "price": 250, "equip_slot": "chest", "stats_bonus": {"defense": 10}, "image_path": "images/items/armor/armor_010.png"},
    "armor_011": {"name": "Shadow Cloak", "category": "Armor", "price": 180, "equip_slot": "chest", "stats_bonus": {"defense": 6, "evasion": 4}, "image_path": "images/items/armor/armor_011.png"},
    "armor_012": {"name": "Knight's Armor", "category": "Armor", "price": 160, "equip_slot": "chest", "stats_bonus": {"defense": 9}, "image_path": "images/items/armor/armor_012.png"},
     "armor_013": {"name": "Full Plate Armor", "category": "Armor", "price": 220, "equip_slot": "chest", "stats_bonus": {"defense": 11}, "image_path": "images/items/armor/armor_013.png"},
    "armor_014": {"name": "Ancient Armor", "category": "Armor", "price": 280, "equip_slot": "chest", "stats_bonus": {"defense": 12, "health": 5}, "image_path": "images/items/armor/armor_014.png"},
    "armor_015": {"name": "Blessed Platemail", "category": "Armor", "price": 300, "equip_slot": "chest", "stats_bonus": {"defense": 13, "mana": 5}, "image_path": "images/items/armor/armor_015.png"},
    "armor_016": {"name": "Cursed Armor", "category": "Armor", "price": 260, "equip_slot": "chest", "stats_bonus": {"defense": 14, "attack": [-2, -2]}, "image_path": "images/items/armor/armor_016.png"},
    "armor_017": {"name": "Demonhide Armor", "category": "Armor", "price": 320, "equip_slot": "chest", "stats_bonus": {"defense": 10, "evasion": 2}, "image_path": "images/items/armor/armor_017.png"},
    "armor_018": {"name": "Robe of the Archmage", "category": "Armor", "price": 350, "equip_slot": "chest", "stats_bonus": {"defense": 5, "mana": 15}, "image_path": "images/items/armor/armor_018.png"},
    "armor_019": {"name": "Thief's Garb", "category": "Armor", "price": 190, "equip_slot": "chest", "stats_bonus": {"defense": 4, "evasion": 6}, "image_path": "images/items/armor/armor_019.png"},
    "armor_020": {"name": "Guardian's Armor", "category": "Armor", "price": 400, "equip_slot": "chest", "stats_bonus": {"defense": 15}, "image_path": "images/items/armor/armor_020.png"},
     "armor_021": {"name": "Armor of Thorns", "category": "Armor", "price": 380, "equip_slot": "chest", "stats_bonus": {"defense": 12}, "image_path": "images/items/armor/armor_021.png"},  # Could add a thorns effect later
    "armor_022": {"name": "Celestial Armor", "category": "Armor", "price": 450, "equip_slot": "chest", "stats_bonus": {"defense": 14, "health": 10}, "image_path": "images/items/armor/armor_022.png"},
    "armor_023": {"name": "Void Armor", "category": "Armor", "price": 420, "equip_slot": "chest", "stats_bonus": {"defense": 13, "evasion": 3}, "image_path": "images/items/armor/armor_023.png"},
    "armor_024": {"name": "Phoenix Armor", "category": "Armor", "price": 480, "equip_slot": "chest", "stats_bonus": {"defense": 11, "mana": 10}, "image_path": "images/items/armor/armor_024.png"},
    "armor_025": {"name": "Armor of the Gods", "category": "Armor", "price": 600, "equip_slot": "chest", "stats_bonus": {"defense": 18}, "image_path": "images/items/armor/armor_025.png"},
    # --- Helmets --- (Continued)
    "helmet_001": {"name": "Leather Cap", "category": "Helmets", "price": 10, "equip_slot": "head", "stats_bonus": {"defense": 1}, "image_path": "images/items/helmets/helmet_001.png"},
    "helmet_002": {"name": "Iron Helmet", "category": "Helmets", "price": 25, "equip_slot": "head", "stats_bonus": {"defense": 2}, "image_path": "images/items/helmets/helmet_002.png"},
    "helmet_003": {"name": "Steel Helmet", "category": "Helmets", "price": 40, "equip_slot": "head", "stats_bonus": {"defense": 3}, "image_path": "images/items/helmets/helmet_003.png"},
    "helmet_004": {"name": "Viking Helmet", "category": "Helmets", "price": 55, "equip_slot": "head", "stats_bonus": {"defense": 4, "attack": [1, 1]}, "image_path": "images/items/helmets/helmet_004.png"},
    "helmet_005": {"name": "Knight's Helm", "category": "Helmets", "price": 70, "equip_slot": "head", "stats_bonus": {"defense": 5}, "image_path": "images/items/helmets/helmet_005.png"},
    "helmet_006": {"name": "Horned Helmet", "category": "Helmets", "price": 85, "equip_slot": "head", "stats_bonus": {"defense": 3, "attack": [2, 2]}, "image_path": "images/items/helmets/helmet_006.png"},
    "helmet_007": {"name": "Full Helm", "category": "Helmets", "price": 100, "equip_slot": "head", "stats_bonus": {"defense": 6}, "image_path": "images/items/helmets/helmet_007.png"},
    "helmet_008": {"name": "Winged Helmet", "category": "Helmets", "price": 120, "equip_slot": "head", "stats_bonus": {"defense": 4, "evasion": 2}, "image_path": "images/items/helmets/helmet_008.png"},
    "helmet_009": {"name": "Dragon Helm", "category": "Helmets", "price": 150, "equip_slot": "head", "stats_bonus": {"defense": 7}, "image_path": "images/items/helmets/helmet_009.png"},
    "helmet_010": {"name": "Cursed Helm", "category": "Helmets", "price": 130, "equip_slot": "head", "stats_bonus": {"defense": 8, "health": -5}, "image_path": "images/items/helmets/helmet_010.png"},
    "helmet_011": {"name": "Blessed Helm", "category": "Helmets", "price": 140, "equip_slot": "head", "stats_bonus": {"defense": 5, "mana": 5}, "image_path": "images/items/helmets/helmet_011.png"},
    "helmet_012": {"name": "Thief's Hood", "category": "Helmets", "price": 90, "equip_slot": "head", "stats_bonus": {"defense": 2, "evasion": 4}, "image_path": "images/items/helmets/helmet_012.png"},
    "helmet_013": {"name": "Mage's Hat", "category": "Helmets", "price": 80, "equip_slot": "head", "stats_bonus": {"defense": 1, "mana": 10}, "image_path": "images/items/helmets/helmet_013.png"},
    "helmet_014": {"name": "Warrior's Helm", "category": "Helmets", "price": 110, "equip_slot": "head", "stats_bonus": {"defense": 6, "attack":[1,1]}, "image_path": "images/items/helmets/helmet_014.png"},
    "helmet_015": {"name": "Royal Crown", "category": "Helmets", "price": 200, "equip_slot": "head", "stats_bonus": {"defense": 5, "health": 10, "mana": 10}, "image_path": "images/items/helmets/helmet_015.png"},
    "helmet_016": {"name": "Barbarian Helm", "category": "Helmets", "price": 160, "equip_slot": "head", "stats_bonus": {"defense": 4, "attack": [3,3]}, "image_path": "images/items/helmets/helmet_016.png"},
    "helmet_017": {"name": "Shadow Mask", "category": "Helmets", "price": 140, "equip_slot": "head", "stats_bonus": {"defense": 3, "evasion": 5}, "image_path": "images/items/helmets/helmet_017.png"},
    "helmet_018": {"name": "Helm of Light", "category": "Helmets", "price": 180, "equip_slot": "head", "stats_bonus": {"defense": 7, "accuracy": 2}, "image_path": "images/items/helmets/helmet_018.png"},
    "helmet_019": {"name": "Helm of Darkness", "category": "Helmets", "price": 170, "equip_slot": "head", "stats_bonus": {"defense": 6, "attack": [2, 4]}, "image_path": "images/items/helmets/helmet_019.png"},
    "helmet_020": {"name": "Ancient Helm", "category": "Helmets", "price": 220, "equip_slot": "head", "stats_bonus": {"defense": 9}, "image_path": "images/items/helmets/helmet_020.png"},
    "helmet_021": {"name": "Mystic Circlet", "category": "Helmets", "price": 210, "equip_slot": "head", "stats_bonus": {"defense": 3, "mana": 15}, "image_path": "images/items/helmets/helmet_021.png"},
    "helmet_022": {"name": "Berserker Helm", "category": "Helmets", "price": 190, "equip_slot": "head", "stats_bonus": {"defense": 5, "attack": [4,4]}, "image_path": "images/items/helmets/helmet_022.png"},
    "helmet_023": {"name": "Helm of Valor", "category": "Helmets", "price": 250, "equip_slot": "head", "stats_bonus": {"defense": 8, "health": 8}, "image_path": "images/items/helmets/helmet_023.png"},
    "helmet_024": {"name": "Helm of Wisdom", "category": "Helmets", "price": 240, "equip_slot": "head", "stats_bonus": {"defense": 4, "mana": 20}, "image_path": "images/items/helmets/helmet_024.png"},
    "helmet_025": {"name": "Godly Helm", "category": "Helmets", "price": 300, "equip_slot": "head", "stats_bonus": {"defense": 10, "attack": [2,2]}, "image_path": "images/items/helmets/helmet_025.png"},
    # --- Off-Hands ---
    "offhand_001": {"name": "Wooden Shield", "category": "Weapons", "price": 20, "equip_slot": "off_hand", "stats_bonus": {"defense": 2}, "image_path": "images/items/offhands/offhand_001.png"},
    "offhand_002": {"name": "Buckler", "category": "Weapons", "price": 35, "equip_slot": "off_hand", "stats_bonus": {"defense": 1, "evasion": 2}, "image_path": "images/items/offhands/offhand_002.png"},
    "offhand_003": {"name": "Iron Shield", "category": "Weapons", "price": 50, "equip_slot": "off_hand", "stats_bonus": {"defense": 3}, "image_path": "images/items/offhands/offhand_003.png"},
    "offhand_004": {"name": "Steel Shield", "category": "Weapons", "price": 70, "equip_slot": "off_hand", "stats_bonus": {"defense": 4}, "image_path": "images/items/offhands/offhand_004.png"},
    "offhand_005": {"name": "Tower Shield", "category": "Weapons", "price": 90, "equip_slot": "off_hand", "stats_bonus": {"defense": 6, "evasion": -2}, "image_path": "images/items/offhands/offhand_005.png"},
    "offhand_006": {"name": "Spiked Shield", "category": "Weapons", "price": 80, "equip_slot": "off_hand", "stats_bonus": {"defense": 4, "attack": [1, 1]}, "image_path": "images/items/offhands/offhand_006.png"},
    "offhand_007": {"name": "Elven Shield", "category": "Weapons", "price": 110, "equip_slot": "off_hand", "stats_bonus": {"defense": 3, "evasion": 3}, "image_path": "images/items/offhands/offhand_007.png"},
    "offhand_008": {"name": "Dwarf Shield", "category": "Weapons", "price": 130, "equip_slot": "off_hand", "stats_bonus": {"defense": 7}, "image_path": "images/items/offhands/offhand_008.png"},
    "offhand_009": {"name": "Kite Shield", "category": "Weapons", "price": 100, "equip_slot": "off_hand", "stats_bonus": {"defense": 5, "evasion": 1}, "image_path": "images/items/offhands/offhand_009.png"},
    "offhand_010": {"name": "Magic Orb", "category": "Weapons", "price": 150, "equip_slot": "off_hand", "stats_bonus": {"mana": 10}, "image_path": "images/items/offhands/offhand_010.png"}, #for mages
    "offhand_011": {"name": "Ancient Tome", "category": "Weapons", "price": 140, "equip_slot": "off_hand", "stats_bonus": {"mana": 15}, "image_path": "images/items/offhands/offhand_011.png"}, # For mages
    "offhand_012": {"name": "Guardian Shield", "category": "Weapons", "price": 180, "equip_slot": "off_hand", "stats_bonus":{"defense": 9}, "image_path": "images/items/offhands/offhand_012.png"},
     "offhand_013": {"name": "Shield of Thorns", "category": "Weapons", "price": 160, "equip_slot": "off_hand", "stats_bonus": {"defense": 6}, "image_path": "images/items/offhands/offhand_013.png"}, # Could add thorns effect later
    "offhand_014": {"name": "Blessed Shield", "category": "Weapons", "price": 200, "equip_slot": "off_hand", "stats_bonus": {"defense": 7, "health": 5}, "image_path": "images/items/offhands/offhand_014.png"},
    "offhand_015": {"name": "Cursed Shield", "category": "Weapons", "price": 190, "equip_slot": "off_hand", "stats_bonus": {"defense": 10, "attack": [-1, -1]}, "image_path": "images/items/offhands/offhand_015.png"},
     "offhand_016": {"name": "Rune Shield", "category": "Weapons", "price": 220, "equip_slot": "off_hand", "stats_bonus":{"defense": 8, "mana": 5}, "image_path": "images/items/offhands/offhand_016.png"},
    "offhand_017": {"name": "Dragon Shield", "category": "Weapons", "price": 250, "equip_slot": "off_hand", "stats_bonus": {"defense": 12}, "image_path": "images/items/offhands/offhand_017.png"},
    "offhand_018": {"name": "Skull Shield", "category": "Weapons", "price": 230, "equip_slot": "off_hand", "stats_bonus": {"defense": 9, "accuracy": 1}, "image_path": "images/items/offhands/offhand_018.png"},
    "offhand_019": {"name": "Mirror Shield", "category": "Weapons", "price": 240, "equip_slot": "off_hand", "stats_bonus":{"defense": 7, "evasion": 4}, "image_path": "images/items/offhands/offhand_019.png"},
    "offhand_020": {"name": "Tome of Wisdom", "category": "Weapons", "price": 260, "equip_slot": "off_hand", "stats_bonus": {"mana": 25}, "image_path": "images/items/offhands/offhand_020.png"},  # For mages
    "offhand_021": {"name": "Tome of Power", "category": "Weapons", "price": 280, "equip_slot": "off_hand", "stats_bonus": {"mana": 20, "attack": [2, 2]}, "image_path": "images/items/offhands/offhand_021.png"},  # For mages
    "offhand_022": {"name": "Shield of Light", "category": "Weapons", "price": 300, "equip_slot": "off_hand", "stats_bonus": {"defense": 11, "accuracy": 2}, "image_path": "images/items/offhands/offhand_022.png"},
    "offhand_023": {"name": "Shield of Darkness", "category": "Weapons", "price": 320, "equip_slot": "off_hand", "stats_bonus":{"defense": 14}, "image_path": "images/items/offhands/offhand_023.png"},
    "offhand_024": {"name": "Aegis of the Gods", "category": "Weapons", "price": 400, "equip_slot": "off_hand", "stats_bonus":{"defense": 15}, "image_path": "images/items/offhands/offhand_024.png"},
    "offhand_025": {"name": "Grimoire of Souls", "category": "Weapons", "price": 350, "equip_slot": "off_hand", "stats_bonus":{"mana": 30}, "image_path": "images/items/offhands/offhand_025.png"},  # For mages
    # --- Rings ---
    "ring_001": {"name": "Ring of Minor Health", "category": "Rings", "price": 40, "equip_slot": "ring1", "stats_bonus": {"health": 5}, "image_path": "images/items/rings/ring_001.png"},
    "ring_002": {"name": "Ring of Minor Mana", "category": "Rings", "price": 40, "equip_slot": "ring1", "stats_bonus": {"mana": 5}, "image_path": "images/items/rings/ring_002.png"},
    "ring_003": {"name": "Ring of Protection", "category": "Rings", "price": 60, "equip_slot": "ring1", "stats_bonus": {"defense": 2}, "image_path": "images/items/rings/ring_003.png"},
    "ring_004": {"name": "Ring of Strength", "category": "Rings", "price": 60, "equip_slot": "ring1", "stats_bonus": {"attack": [1, 1]}, "image_path": "images/items/rings/ring_004.png"},
    "ring_005": {"name": "Ring of Evasion", "category": "Rings", "price": 50, "equip_slot": "ring1", "stats_bonus": {"evasion": 3}, "image_path": "images/items/rings/ring_005.png"},
    "ring_006": {"name": "Ring of Accuracy", "category": "Rings", "price": 50, "equip_slot": "ring1", "stats_bonus": {"accuracy": 3}, "image_path": "images/items/rings/ring_006.png"},
    "ring_007": {"name": "Ring of Life", "category": "Rings", "price": 80, "equip_slot": "ring1", "stats_bonus": {"health": 10}, "image_path": "images/items/rings/ring_007.png"},
    "ring_008": {"name": "Ring of Energy", "category": "Rings", "price": 80, "equip_slot": "ring1", "stats_bonus": {"mana": 10}, "image_path": "images/items/rings/ring_008.png"},
    "ring_009": {"name": "Ring of the Warrior", "category": "Rings", "price": 100, "equip_slot": "ring1", "stats_bonus": {"attack": [2, 2]}, "image_path": "images/items/rings/ring_009.png"},
    "ring_010": {"name": "Ring of the Defender", "category": "Rings", "price": 100, "equip_slot": "ring1", "stats_bonus": {"defense": 4}, "image_path": "images/items/rings/ring_010.png"},
    "ring_011": {"name": "Ring of the Thief", "category": "Rings", "price": 90, "equip_slot": "ring1", "stats_bonus": {"evasion": 5}, "image_path": "images/items/rings/ring_011.png"},
    "ring_012": {"name": "Ring of the Sniper", "category": "Rings", "price": 90, "equip_slot": "ring1", "stats_bonus": {"accuracy": 5}, "image_path": "images/items/rings/ring_012.png"},
    "ring_013": {"name": "Ring of Regeneration", "category": "Rings", "price": 120, "equip_slot": "ring1", "stats_bonus": {"health": 2}, "image_path": "images/items/rings/ring_013.png"}, #  Could add regen effect later.
    "ring_014": {"name": "Ring of Magic", "category": "Rings", "price": 120, "equip_slot": "ring1", "stats_bonus": {"mana": 15}, "image_path": "images/items/rings/ring_014.png"},
    "ring_015": {"name": "Cursed Ring", "category": "Rings", "price": 50, "equip_slot": "ring1", "stats_bonus": {"attack": [3,3], "health": -10}, "image_path": "images/items/rings/ring_015.png"},
    "ring_016": {"name": "Blessed Ring", "category": "Rings", "price": 150, "equip_slot": "ring1", "stats_bonus": {"health": 8, "mana": 8}, "image_path": "images/items/rings/ring_016.png"},
    "ring_017": {"name": "Ring of Fire", "category": "Rings", "price": 140, "equip_slot": "ring1", "stats_bonus": {"attack": [1, 4]}, "image_path": "images/items/rings/ring_017.png"},  # Could add fire damage later
    "ring_018": {"name": "Ring of Ice", "category": "Rings", "price": 140, "equip_slot": "ring1", "stats_bonus": {"defense": 3, "evasion": 2}, "image_path": "images/items/rings/ring_018.png"}, # Could add cold effect later.
    "ring_019": {"name": "Ring of Shadows", "category": "Rings", "price": 160, "equip_slot": "ring1", "stats_bonus": {"evasion": 7}, "image_path": "images/items/rings/ring_019.png"},
    "ring_020": {"name": "Ring of Precision", "category": "Rings", "price": 160, "equip_slot": "ring1", "stats_bonus": {"accuracy": 7}, "image_path": "images/items/rings/ring_020.png"},
    "ring_021": {"name": "Ring of the Elements", "category": "Rings", "price": 180, "equip_slot": "ring1", "stats_bonus": {"attack": [2,2], "defense":2}, "image_path": "images/items/rings/ring_021.png"}, #could add elemental damage later
    "ring_022": {"name": "Ancient Ring", "category": "Rings", "price": 200, "equip_slot": "ring1", "stats_bonus": {"health": 12, "mana": 12}, "image_path": "images/items/rings/ring_022.png"},
    "ring_023": {"name": "Dragon Ring", "category": "Rings", "price": 250, "equip_slot": "ring1", "stats_bonus": {"attack": [4,4], "defense": 4}, "image_path": "images/items/rings/ring_023.png"},
    "ring_024": {"name": "Godly Ring", "category": "Rings", "price": 300, "equip_slot": "ring1", "stats_bonus": {"health": 15, "mana": 15}, "image_path": "images/items/rings/ring_024.png"},
    "ring_025": {"name": "Ring of Ultimate Power", "category": "Rings", "price": 350, "equip_slot": "ring1", "stats_bonus": {"attack": [5,5], "defense": 5, "accuracy": 5, "evasion":5}, "image_path": "images/items/rings/ring_025.png"},
# --- Potions ---
    "potion_001": {"name": "Minor Healing Potion", "category": "Potions", "price": 10, "equip_slot": None, "effect": {"type": "heal", "amount": 20}, "image_path": "images/items/potions/potion_001.png", "description": "Restores a small amount of HP."},
    "potion_002": {"name": "Healing Potion", "category": "Potions", "price": 25, "equip_slot": None, "effect": {"type": "heal", "amount": 50}, "image_path": "images/items/potions/potion_002.png", "description": "Restores a moderate amount of HP."},
    "potion_003": {"name": "Greater Healing Potion", "category": "Potions", "price": 50, "equip_slot": None, "effect": {"type": "heal", "amount": 100}, "image_path": "images/items/potions/potion_003.png", "description":"Restores a large amount of HP."},
    "potion_004": {"name": "Minor Mana Potion", "category": "Potions", "price": 15, "equip_slot": None, "effect": {"type": "mana", "amount": 20}, "image_path": "images/items/potions/potion_004.png", "description":"Restores a small amount of MP"},
    "potion_005": {"name": "Mana Potion", "category": "Potions", "price": 35, "equip_slot": None, "effect": {"type": "mana", "amount": 50}, "image_path": "images/items/potions/potion_005.png", "description":"Restores a moderate amount of MP"},
    "potion_006": {"name": "Greater Mana Potion", "category": "Potions", "price": 70, "equip_slot": None, "effect": {"type": "mana", "amount": 100}, "image_path": "images/items/potions/potion_006.png", "description": "Restores a large amount of MP."},
    "potion_007": {"name": "Potion of Strength", "category": "Potions", "price": 40, "equip_slot": None, "effect": {"type": "buff", "stat": "attack_buff", "amount": 0.10, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_007.png", "description":"Temporarily increases attack damage by 10%."},
    "potion_008": {"name": "Potion of Defense", "category": "Potions", "price": 40, "equip_slot": None, "effect": {"type": "buff", "stat": "defense_buff", "amount": 0.10, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_008.png", "description":"Temporarily increases defense by 10%."},
    "potion_009": {"name": "Potion of Agility", "category": "Potions", "price": 30, "equip_slot": None, "effect": {"type": "buff", "stat": "evasion_buff", "amount": 10, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_009.png", "description":"Temporarily increases evasion by 10%."},
    "potion_010": {"name": "Potion of Accuracy", "category": "Potions", "price": 30, "equip_slot": None, "effect": {"type": "buff", "stat": "accuracy_buff", "amount": 10, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_010.png", "description":"Temporarily increases accuracy by 10%."},
    "potion_011": {"name": "Elixir of Life", "category": "Potions", "price": 100, "equip_slot": None, "effect": {"type": "heal", "amount": 200}, "image_path": "images/items/potions/potion_011.png", "description":"Restores a very large amount of HP."},
    "potion_012": {"name": "Elixir of Mana", "category": "Potions", "price": 120, "equip_slot": None, "effect": {"type": "mana", "amount": 200}, "image_path": "images/items/potions/potion_012.png", "description":"Restores a large amount of MP"},
    "potion_013": {"name": "Potion of Greater Strength", "category": "Potions", "price": 80, "equip_slot": None, "effect": {"type": "buff", "stat": "attack_buff", "amount": 0.20, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_013.png", "description":"Temporarily increases attack damage by 20%."},
    "potion_014": {"name": "Potion of Greater Defense", "category": "Potions", "price": 80, "equip_slot": None, "effect": {"type": "buff", "stat": "defense_buff", "amount": 0.20, "duration_turns": 5, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_014.png", "description":"Temporarily increases defense by 20%."},
    "potion_015": {"name": "Potion of Swiftness", "category": "Potions", "price": 60, "equip_slot": None, "effect": {"type": "buff", "stat": "evasion_buff", "amount": 15, "duration_turns": 4, "is_percentage_buff":True}, "image_path": "images/items/potions/potion_015.png", "description":"Temporarily increases evasion."},
    "potion_016": {"name": "Potion of Focus", "category": "Potions", "price": 60, "equip_slot": None, "effect": {"type": "buff", "stat": "accuracy_buff", "amount": 15, "duration_turns": 4, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_016.png", "description":"Temporarily increases accuracy."},
    "potion_017": {"name": "Antidote", "category": "Potions", "price": 30, "equip_slot": None, "effect": {"type": "cure", "status": "poison"}, "image_path": "images/items/potions/potion_017.png", "description":"Cures poison."}, #  Need to implement status effects
    "potion_018": {"name": "Potion of Invisibility", "category": "Potions", "price": 150, "equip_slot": None, "effect": {"type": "buff", "stat": "invisible", "duration_turns": 3}, "image_path": "images/items/potions/potion_018.png", "description":"Turns you invisible for a short time."},  # Need to implement invisibility
    "potion_019": {"name": "Full Restore Potion", "category": "Potions", "price": 200, "equip_slot": None, "effect": {"type": "heal", "amount": 9999}, "image_path": "images/items/potions/potion_019.png", "description":"Fully restores HP."}, #Could also make full mana restore potion.
    "potion_020": {"name": "Potion of Rage", "category": "Potions", "price": 90, "equip_slot": None, "effect": {"type": "buff", "stat": "attack_buff", "amount": 0.30, "duration_turns": 3, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_020.png", "description":"Greatly increases attack, but for a short time."},
    "potion_021": {"name": "Potion of Stoneskin", "category": "Potions", "price": 90, "equip_slot": None, "effect": {"type": "buff", "stat": "defense_buff", "amount": 0.30, "duration_turns": 3, "is_percentage_buff": True}, "image_path": "images/items/potions/potion_021.png", "description":"Greatly increases defense for a short time."},
    "potion_022": {"name": "Potion of Haste", "category": "Potions", "price": 110, "equip_slot": None, "effect": {"type": "buff", "stat": "evasion_buff", "amount": 20, "duration_turns": 3, "is_percentage_buff":True}, "image_path": "images/items/potions/potion_022.png", "description":"Greatly increases evasion for a short time."},
    "potion_023": {"name": "Potion of Precision", "category": "Potions", "price": 110, "equip_slot": None, "effect": {"type": "buff", "stat": "accuracy_buff", "amount": 20, "duration_turns": 3, "is_percentage_buff":True}, "image_path": "images/items/potions/potion_023.png", "description":"Greatly increases accuracy for a short time."},
    "potion_024": {"name": "Mysterious Potion", "category": "Potions", "price": 50, "equip_slot": None, "effect": {"type": "random"}, "image_path": "images/items/potions/potion_024.png", "description":"Has an unknown effect..."},  # Need to implement random effect
    "potion_025": {"name": "Elixir of Immortality", "category": "Potions", "price": 500, "equip_slot": None, "effect": {"type": "buff", "stat": "invincible", "duration_turns": 1}, "image_path": "images/items/potions/potion_025.png", "description":"Grants invincibility for one turn!"}, # Need to implement
    # --- Scrolls ---
    "scroll_001": {"name": "Scroll of Minor Damage", "category": "Scrolls", "price": 20, "equip_slot": None, "effect": {"type": "damage", "amount": 15, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_001.png", "description":"Inflicts minor magical damage."},
    "scroll_002": {"name": "Scroll of Firebolt", "category": "Scrolls", "price": 40, "equip_slot": None, "effect": {"type": "damage", "amount": 30, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_002.png", "description":"Unleashes a fiery bolt."},
    "scroll_003": {"name": "Scroll of Frost", "category": "Scrolls", "price": 40, "equip_slot": None, "effect": {"type": "damage", "amount": 25, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_003.png", "description":"Deals frost damage"},
    "scroll_004": {"name": "Scroll of Lightning", "category": "Scrolls", "price": 50, "equip_slot": None, "effect": {"type": "damage", "amount": 35, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_004.png", "description":"Strikes with a bolt of lightning."},
    "scroll_005": {"name": "Scroll of Confusion", "category": "Scrolls", "price": 60, "equip_slot": None, "effect": {"type": "debuff", "stat": "accuracy_debuff", "amount": -20, "duration_turns": 3, "target": "enemy", "is_percentage_buff" : True}, "image_path": "images/items/scrolls/scroll_005.png", "description":"Confuses the enemy, reducing accuracy."},
    "scroll_006": {"name": "Scroll of Weakness", "category": "Scrolls", "price": 60, "equip_slot": None, "effect": {"type": "debuff", "stat": "attack_debuff", "amount": -0.15, "duration_turns": 3, "target": "enemy", "is_percentage_buff" : True}, "image_path": "images/items/scrolls/scroll_006.png", "description":"Weakens the enemy's attacks."},
    "scroll_007": {"name": "Scroll of Vulnerability", "category": "Scrolls", "price": 60, "equip_slot": None, "effect": {"type": "debuff", "stat": "defense_debuff", "amount": -0.15, "duration_turns": 3, "target": "enemy", "is_percentage_buff" : True}, "image_path": "images/items/scrolls/scroll_007.png", "description": "Reduces the enemy's defenses."},
    "scroll_008": {"name": "Scroll of Healing", "category": "Scrolls", "price": 75, "equip_slot": None, "effect": {"type": "heal", "amount": 75}, "image_path": "images/items/scrolls/scroll_010.png", "description":"Restores a significant amount of HP."}, #  Reuse existing images if possible
    "scroll_009": {"name": "Scroll of Greater Firebolt", "category": "Scrolls", "price": 90, "equip_slot": None, "effect": {"type": "damage", "amount": 50, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_011.png", "description":"A more powerful firebolt."}, #  Reuse existing images if possible
    "scroll_010": {"name": "Scroll of Greater Frost", "category": "Scrolls", "price": 90, "equip_slot": None, "effect": {"type": "damage", "amount": 45, "target": "enemy"}, "image_path": "images/items/scrolls/scroll_012.png", "description":"Stronger frost damage."},  # Reuse existing images if possible
    # --- Miscellaneous Items ---
    "misc_001": {"name": "Apple", "category": "Misc", "price": 5, "equip_slot": None, "effect": {"type": "buff", "stat": "health_buff", "amount": 5, "duration_turns": 3, "is_percentage_buff":False}, "image_path": "images/items/misc/misc_001.png", "description": "A crisp, refreshing apple. Slightly increases health."},
    "misc_002": {"name": "Bread", "category": "Misc", "price": 8, "equip_slot": None, "effect": {"type": "buff", "stat": "attack_buff", "amount": .05, "duration_turns": 2, "is_percentage_buff":True}, "image_path": "images/items/misc/misc_002.png", "description": "A loaf of freshly baked bread. Slightly increases attack."},
    "misc_003": {"name": "Cheese", "category": "Misc", "price": 7, "equip_slot": None, "effect": {"type": "buff", "stat": "defense_buff", "amount": .05, "duration_turns": 2, "is_percentage_buff": True}, "image_path": "images/items/misc/misc_003.png", "description": "A wedge of cheese. Slightly increases defense."},
    "misc_004": {"name": "Dried Meat", "category": "Misc", "price": 12, "equip_slot": None, "effect": {"type": "buff", "stat": "health_buff", "amount": 10, "duration_turns": 5, "is_percentage_buff": False}, "image_path": "images/items/misc/misc_004.png", "description": "Preserved meat. Provides a small, lasting health boost."},
    "misc_005": {"name": "Berries", "category": "Misc", "price": 6, "equip_slot": None, "effect": {"type": "buff", "stat": "evasion_buff", "amount": 5, "duration_turns": 2, "is_percentage_buff": True}, "image_path": "images/items/misc/misc_005.png", "description": "A handful of berries. Slightly increases evasion."},
     "misc_006": {"name": "Roasted Chicken Leg", "category": "Misc", "price": 20, "equip_slot": None, "effect": {"type": "buff", "stat": "health_buff", "amount": 15, "duration_turns": 4, "is_percentage_buff": False}, "image_path": "images/items/misc/misc_006.png", "description":"Small HP increase"},
    "misc_007": {"name": "Bottle of Wine", "category": "Misc", "price": 25, "equip_slot": None, "effect": {"type": "buff", "stat": "attack_buff", "amount": 0.10, "duration_turns": 2, "is_percentage_buff": True}, "image_path": "images/items/misc/misc_007.png", "description":"Small Attack boost"},
    "misc_008": {"name": "Spiced Nuts", "category": "Misc", "price": 15, "equip_slot": None, "effect": {"type": "buff", "stat": "accuracy_buff", "amount": 7, "duration_turns": 3, "is_percentage_buff": True}, "image_path": "images/items/misc/misc_008.png", "description":"Improves aim slightly."},
    "misc_009": {"name": "Energy Drink", "category": "Misc", "price": 30, "equip_slot": None, "effect": {"type": "buff", "stat": "evasion_buff", "amount": 12, "duration_turns": 1, "is_percentage_buff":True}, "image_path": "images/items/misc/misc_009.png", "description":"A short burst of incredible speed!"},
    "misc_010": {"name": "Herbal Tea", "category": "Misc", "price": 22, "equip_slot": None, "effect": {"type": "buff", "stat": "mana", "amount": 10, "duration_turns": 3, "is_percentage_buff":False}, "image_path": "images/items/misc/misc_010.png", "description":"Slightly increases mana"},
    "misc_011": {"name": "Rope", "category": "Misc", "price": 10, "equip_slot": None, "effect": {"type": "utility", "use": "climb/bind"}, "image_path": "images/items/misc/misc_011.png", "description": "A sturdy length of rope. Useful for climbing or binding."},
    "misc_012": {"name": "Torch", "category": "Misc", "price": 5, "equip_slot": None, "effect": {"type": "utility", "use": "light"}, "image_path": "images/items/misc/misc_012.png", "description": "Provides light in dark places."},
    "misc_013": {"name": "Lockpick", "category": "Misc", "price": 50, "equip_slot": None, "effect": {"type": "utility", "use": "unlock"}, "image_path": "images/items/misc/misc_013.png", "description": "A tool for opening simple locks."},
    "misc_014": {"name": "Trap Disarm Kit", "category": "Misc", "price": 75, "equip_slot": None, "effect": {"type": "utility", "use": "disarm_trap"}, "image_path": "images/items/misc/misc_014.png", "description": "Tools for safely disarming traps."},
    "misc_015": {"name": "Small Healing Salve", "category": "Misc", "price": 18,"equip_slot": None, "effect": {"type": "heal", "amount": 30}, "image_path": "images/items/misc/misc_015.png", "description": "A soothing salve that heals minor wounds."},
    "misc_016": {"name": "Flint and Steel", "category": "Misc", "price": 8, "equip_slot": None, "effect": {"type": "utility", "use": "start_fire"}, "image_path": "images/items/misc/misc_016.png", "description": "Used to start a fire."},
    "misc_017": {"name": "Grappling Hook", "category": "Misc", "price": 60, "equip_slot": None, "effect":{"type": "utility", "use":"grapple"}, "image_path": "images/items/misc/misc_017.png", "description":"Used for scaling"},
    "misc_018": {"name": "Crowbar", "category": "Misc", "price": 35, "equip_slot": None, "effect": {"type": "utility", "use": "force_open"}, "image_path": "images/items/misc/misc_018.png", "description": "For prying things open."},
    "misc_019": {"name": "Map", "category": "Misc", "price": 20, "equip_slot": None, "effect": {"type": "utility", "use": "reveal_map"}, "image_path": "images/items/misc/misc_019.png", "description": "Helps you find your way."},
    "misc_020": {"name": "Compass", "category": "Misc", "price": 25, "equip_slot": None, "effect": {"type": "utility", "use": "navigation"}, "image_path": "images/items/misc/misc_020.png", "description": "Always points north."},
    "misc_021": {"name": "Spyglass", "category": "Misc", "price": 40, "equip_slot": None, "effect":{"type": "utility", "use":"scout"}, "image_path": "images/items/misc/misc_021.png", "description": "For seeing things far away."},
    "misc_022": {"name": "Shovel", "category": "Misc", "price": 15, "equip_slot": None, "effect": {"type": "utility", "use": "dig"}, "image_path": "images/items/misc/misc_022.png", "description": "For digging."},
     "misc_023": {"name": "Empty Vial", "category": "Misc", "price": 3, "equip_slot":None, "effect": {"type": "utility", "use": "collect_liquid"}, "image_path": "images/items/misc/misc_023.png", "description":"Used for storing liquids"},
    "misc_024": {"name": "Magnifying Glass", "category": "Misc", "price": 12, "equip_slot": None, "effect":{"type": "utility", "use":"examine"}, "image_path": "images/items/misc/misc_024.png", "description": "For close inspection."},
    "misc_025": {"name": "Whistle", "category": "Misc", "price": 2, "equip_slot": None, "effect": {"type": "utility", "use": "signal"}, "image_path": "images/items/misc/misc_025.png", "description": "Makes a loud noise."},
    # --- Add Loot Items to shop_items_data (Example) ---
    "loot_001": {"name": "Rat Tail", "category": "Loot", "price": 2, "equip_slot": None, "image_path": "images/items/loot/loot_001.png", "description": "A severed rat tail. Not very valuable."},
    "loot_002": {"name": "Goblin Tooth", "category": "Loot", "price": 5, "equip_slot": None, "image_path": "images/items/loot/loot_002.png", "description": "A chipped goblin tooth."},
    "loot_003": {"name": "Spider Silk", "category": "Loot", "price": 8, "equip_slot": None, "image_path": "images/items/loot/loot_003.png", "description": "A surprisingly strong strand of spider silk."},
    "loot_004": {"name": "Broken Bone", "category": "Loot", "price": 3, "equip_slot": None, "image_path": "images/items/loot/loot_004.png", "description": "A brittle, broken bone. Probably from a skeleton."},
    "loot_005": {"name": "Torn Cloth", "category": "Loot", "price": 1, "equip_slot": None, "image_path": "images/items/loot/loot_005.png", "description": "A scrap of dirty cloth."},
    "loot_006": {"name": "Small Gemstone", "category": "Loot", "price": 25, "equip_slot": None, "image_path": "images/items/loot/loot_006.png", "description": "A small, uncut gemstone."},
    "loot_007": {"name": "Silver Ring", "category": "Loot", "price": 35, "equip_slot": None, "image_path": "images/items/loot/loot_007.png", "description": "A tarnished silver ring."},
     "loot_008": {"name": "Gold Necklace", "category": "Loot", "price": 50, "equip_slot": None, "image_path": "images/items/loot/loot_008.png", "description":"Small but valuable"},
    "loot_009": {"name": "Orcish Battle Totem", "category": "Loot", "price": 15, "equip_slot": None, "image_path": "images/items/loot/loot_009.png", "description":"An odd token"},
    "loot_010": {"name": "Dragon Scale", "category": "Loot", "price": 100, "equip_slot": None, "image_path": "images/items/loot/loot_010.png", "description":"Extremely Rare"},
    "loot_011": {"name": "Ancient Coin", "category": "Loot", "price": 18, "equip_slot": None, "image_path": "images/items/loot/loot_011.png", "description":"Old but could be valuable"},
    "loot_012": {"name": "Shiny Rock", "category": "Loot", "price": 5, "equip_slot": None, "image_path": "images/items/loot/loot_012.png", "description":"Shiny!"},
    "loot_013": {"name": "Goblin Ear", "category": "Loot", "price": 4, "equip_slot": None, "image_path": "images/items/loot/loot_013.png", "description":"Proof of a kill"},
    "loot_014": {"name": "Skeleton Bone", "category": "Loot", "price": 2, "equip_slot": None, "image_path": "images/items/loot/loot_014.png", "description":"Part of a skeleton"},
    "loot_015": {"name": "Spider Leg", "category": "Loot", "price": 6, "equip_slot": None, "image_path": "images/items/loot/loot_015.png", "description":"A leg from a giant spider"},
     "loot_016": {"name": "Vial of Slime", "category": "Loot", "price": 3, "equip_slot": None, "image_path": "images/items/loot/loot_016.png", "description":"Gooey..."},
    "loot_017": {"name": "Bat Wing", "category": "Loot", "price": 5, "equip_slot": None, "image_path": "images/items/loot/loot_017.png", "description":"From a giant bat"},
    "loot_018": {"name": "Wolf Pelt", "category": "Loot", "price": 12, "equip_slot": None, "image_path": "images/items/loot/loot_018.png", "description":"Soft Fur"},
    "loot_019": {"name": "Bear Claw", "category": "Loot", "price": 14, "equip_slot": None, "image_path": "images/items/loot/loot_019.png", "description":"Sharp and dangerous"},
    "loot_020": {"name": "Snake Skin", "category": "Loot", "price": 10, "equip_slot": None, "image_path": "images/items/loot/loot_020.png", "description":"Shedded Skin"},
    "loot_021": {"name": "Feather", "category": "Loot", "price": 1, "equip_slot": None, "image_path": "images/items/loot/loot_021.png", "description":"A colourful feather"},
    "loot_022": {"name": "Troll Hair", "category": "Loot", "price": 8, "equip_slot": None, "image_path": "images/items/loot/loot_022.png", "description":"Coarse and smelly."},
    "loot_023": {"name": "Mushroom", "category": "Loot", "price": 3, "equip_slot": None, "image_path": "images/items/loot/loot_023.png", "description":"Is it edible?"},
     "loot_024": {"name": "Crystal Shard", "category": "Loot", "price": 22, "equip_slot": None, "image_path": "images/items/loot/loot_024.png", "description":"Sparkling with energy"},
    "loot_025": {"name": "Ancient Scroll", "category": "Loot", "price": 45, "equip_slot": None, "image_path": "images/items/loot/loot_025.png", "description":"Could be a valuable find"},

}
#MONSTER CREATION
def create_monster(monster_name, roomlvl): # Added roomlvl parameter
    if monster_name in monster_data:
        data = monster_data[monster_name]

        # --- Apply Level Scaling ---
        multiplier = get_monster_stat_multiplier_by_floor(roomlvl) # Get multiplier based on roomlvl
        scaled_health = round(data["health"] * multiplier)
        scaled_defense = round(data["defense"] * multiplier)
        scaled_attack_range = [round(data["attack"][0] * multiplier), round(data["attack"][1] * multiplier)] # Scale attack range
        scaled_evasion=round(data["evasion"] * multiplier)

        if "gold_min" in data and "gold_max" in data:
            gold_value = random.randint(data["gold_min"], data["gold_max"])
        elif "gold" in data:
            gold_value = data["gold"]
        else:
            gold_value = 0
            print(f"Warning: No gold information found for monster: {monster_name}. Defaulting to 0 gold.")

        # --- Create Monster Instance ---
        monster = Monster( # <--- Monster object created here, image is loaded in Monster.__init__
            data["name"],
            data["monster_type"],
            scaled_health,
            scaled_attack_range,
            scaled_defense,
            data["accuracy"],
            scaled_evasion,
            data["experience"],
            gold_value,
            data["image_path"],
            data["abilities"]
        )
        return monster
    else:
        print(f"Monster data not found for: {monster_name}")
        return None
def load_monster_images():
    global monster_data
    for monster_name, monster_info in monster_data.items():
        image_path = monster_info.get("image_path") # Get image_path from monster data
        if image_path: # Check if image_path is defined
            try:
                # --- USE resource_path HERE! ---
                full_image_path = resource_path(image_path) # Get FULL resource path
                image = pygame.image.load(full_image_path).convert_alpha() # Load image using FULL path
                monster_data[monster_name]["image"] = image # Store loaded image back in monster_data
            except pygame.error as e:
                print(f"ERROR: Could not load image for {monster_name} from: {full_image_path}") # Error print (using FULL path in error message now)
                print(f"Pygame error: {e}") # Print specific Pygame error message
                monster_data[monster_name]["image"] = None # Set image to None if loading fails
        else:
            print(f"WARNING: No image_path defined for {monster_name}") # Warning if image_path is missing
            monster_data[monster_name]["image"] = None # Set image to None if no path
load_monster_images()
#Dungeon Room Generation
room_content_options = {  # Use this for consistency checks
    "empty": None,
    "chest": None,
    "rat": "Rat",
    "goblin": "Goblin",
    "spider": "Spider",
    "skeleton warrior": "Skeleton Warrior",  # Consistent
    "big rat": "Big Rat",  # Consistent
    "orc": "Orc",
    "mimic": "Mimic",
    "siren": "Siren",
    "giant rat": "Giant Rat",  # Consistent
    "lich": "Lich",
    "dragon": "Dragon",
    "succubus": "Succubus",
    "trap": None
}
roomtable_probabilities = {
    0: {  # Floor 0:  Starting Floor - Still a challenge, but introduces the game
        "empty": 0.30,        # Reduced empty rooms slightly
        "rat": 0.30,          # Rats are common
        "goblin": 0.15,       # Goblins less common
        "big rat": 0.10,      # Introduce Big Rats
        "spider": 0.05,
        "skeleton warrior": 0.0,
        "orc": 0.0,
        "mimic": 0.01,       # Mimics are rare, but a threat from the start
        "siren": 0.0,
        "giant rat": 0.0,
        "lich": 0.0,
        "dragon": 0.0,
        "succubus": 0.0,
        "trap": 0.04,        # Increased traps
        "staircase_down": 0.05
    },
    1: {  # Floor 1:  Early Game - Increasing Challenge
        "empty": 0.20,        # Fewer empty rooms
        "rat": 0.25,          # Rats still present
        "goblin": 0.20,       # Goblins more common
        "big rat": 0.15,     # More Big Rats
        "spider": 0.08,      # More spiders
        "skeleton warrior": 0.02,  # Introduce Skeleton Warriors (rare)
        "orc": 0.0,
        "mimic": 0.02,       # Slightly more mimics
        "siren": 0.0,
        "giant rat": 0.01,    # Introduce Giant Rats (very rare)
        "lich": 0.0,
        "dragon": 0.0,
        "succubus": 0.0,
        "trap": 0.02,        # More traps
        "staircase_down": 0.05
    },
    2: {  # Floor 2:  Mid-Early Game - Noticeable Difficulty Increase
        "empty": 0.15,        # Empty rooms less common
        "rat": 0.15,          # Rats still present, but declining
        "goblin": 0.20,       # Goblins common
        "big rat": 0.15,     # Big Rats common
        "spider": 0.10,      # Spiders more common
        "skeleton warrior": 0.08,  # More Skeleton Warriors
        "orc": 0.02,         # Introduce Orcs (rare)
        "mimic": 0.03,
        "siren": 0.01,       # Introduce Sirens (very rare)
        "giant rat": 0.05,    # Giant Rats more common
        "lich": 0.0,
        "dragon": 0.0,
        "succubus": 0.0,
        "trap": 0.03,        # More traps
        "staircase_down": 0.03
    },
    3: {  # Floor 3:  Mid Game - Solid Challenge
        "empty": 0.10,        # Empty rooms are rarer
        "rat": 0.05,          # Rats are rare
        "goblin": 0.15,       # Goblins less common
        "big rat": 0.10,     # Big Rats less common
        "spider": 0.10,      # Spiders stable
        "skeleton warrior": 0.15, # Skeleton Warriors common
        "orc": 0.10,         # Orcs more common
        "mimic": 0.04,
        "siren": 0.03,       # Sirens more common
        "giant rat": 0.10,    # Giant Rats common
        "lich": 0.01,        # Introduce Liches (very rare)
        "dragon": 0.0,
        "succubus": 0.0,
        "trap": 0.065,        # More traps
        "staircase_down": 0.05
    },
    4: {  # Floor 4:  Mid-Late Game - Getting Tough
        "empty": 0.08,        # Few empty rooms
        "rat": 0.0,          # No more Rats
        "goblin": 0.05,       # Goblins very rare
        "big rat": 0.05,    # Fewer big rats
        "spider": 0.08,     # fewer spiders
        "skeleton warrior": 0.18, # Skeleton Warriors very common
        "orc": 0.15,         # Orcs common
        "mimic": 0.05,
        "siren": 0.07,       # Sirens more common
        "giant rat": 0.12,    # Giant Rats very common
        "lich": 0.03,        # Liches more common
        "dragon": 0.0,
        "succubus": 0.01,     # Introduce Succubi (very rare)
        "trap": 0.128,       # Many traps
        "staircase_down": 0.02
    },
    5: {  # Floor 5:  Late Game - High Difficulty
        "empty": 0.05,        # Very few empty rooms
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.02,    #Fewer big rat
        "spider": 0.0,
        "skeleton warrior": 0.15, # Skeleton Warriors common
        "orc": 0.20,         # Orcs very common
        "mimic": 0.06,
        "siren": 0.10,       # Sirens common
        "giant rat": 0.10,    # Giant Rats common
        "lich": 0.08,        # Liches common
        "dragon": 0.01,      # Introduce Dragons (very rare)
        "succubus": 0.05,     # Succubi more common
        "trap": 0.179,       # Many traps
        "staircase_down": 0.0
    },
    6: {  # Floor 6:  Very Late Game - Very Hard
        "empty": 0.03,        # Almost no empty rooms
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.0,
        "spider": 0.0,
        "skeleton warrior": 0.10, # Skeleton Warriors less common
        "orc": 0.18,         # Orcs very common
        "mimic": 0.07,
        "siren": 0.12,       # Sirens very common
        "giant rat": 0.08,    # Giant Rats less
        "lich": 0.15,        # Liches very common
        "dragon": 0.03,      # Dragons more common
        "succubus": 0.08,     # Succubi common
        "trap": 0.159,       # slightly less Traps
        "staircase_down": 0.001
    },
    7: {  # Floor 7:  Near End-Game - Extremely Hard
        "empty": 0.02,
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.0,    #big rat removed
        "spider": 0.0,
        "skeleton warrior": 0.05,
        "orc": 0.10,         # Orcs less common
        "mimic": 0.08,
        "siren": 0.15,       # Sirens very common
        "giant rat": 0.05,  # giant rat less common
        "lich": 0.20,        # Liches very common
        "dragon": 0.05,      # Dragons more common
        "succubus": 0.15,     # Succubi very common
        "trap": 0.149,       # Many traps
        "staircase_down": 0.001
    },
    8: {  # Floor 8:  End-Game - Brutal
        "empty": 0.01,        # Essentially no empty rooms
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.0,
        "spider": 0.0,
        "skeleton warrior": 0.03,
        "orc": 0.05,         # Orcs rare
        "mimic": 0.09,       # Mimics very common (surprise!)
        "siren": 0.10,       # Sirens Less common
        "giant rat": 0.03,
        "lich": 0.25,        # Liches extremely common
        "dragon": 0.10,      # Dragons common
        "succubus": 0.20,     # Succubi very common
        "trap": 0.139,       # Many traps
        "staircase_down": 0.001
    },
    9: {  # Floor 9:  Penultimate Floor - Maximum Difficulty
        "empty": 0.0,         # NO empty rooms
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.0,
        "spider": 0.0,
        "skeleton warrior": 0.0,
        "orc": 0.03,         # Very few Orcs
        "mimic": 0.10,       # Mimics everywhere!
        "siren": 0.05,     # sirens less common
        "giant rat": 0.03,
        "lich": 0.30,        # Liches are the main threat
        "dragon": 0.15,      # Dragons are a major threat
        "succubus": 0.24,     # Succubi are very common
        "trap": 0.099,       # Many traps
        "staircase_down": 0.001
    },
    10: { # Floor 10: Final Floor - Boss Rush / Gauntlet
        "empty": 0.0,         # NO empty rooms
        "rat": 0.0,
        "goblin": 0.0,
        "big rat": 0.0,
        "spider": 0.0,
        "skeleton warrior": 0.0,
        "orc": 0.0,
        "mimic": 0.05,       # Mimics as a last surprise
        "siren": 0.0,
        "giant rat": 0.0,
        "lich": 0.45,       # Mostly Liches
        "dragon": 0.25,      # Many Dragons
        "succubus": 0.20,    # Many Succubi
        "trap": 0.05,      # few Traps
        "staircase_down": 0.0  # No escape
    }
}

EMPTY_ROOM_DESCRIPTIONS = [ # Add the list from above to your code, usually near the top of your game file where you define constants/data
    "It's an empty room. Dust motes dance in the faint light.",
    "You enter a silent chamber. The air is cold and still.",
    "A dimly lit room with rough-hewn stone walls. Shadows cling to the corners.",
    "This room is eerily silent. You hear only the echo of your own breath.",
    "You find yourself in a small, square room.  Nothing of interest here.",
    "The room is damp and smells of mildew.  Water drips somewhere unseen.",
    "A long, narrow passage opens into this empty space.",
    "Cracked flagstones pave the floor of this desolate chamber.",
    "Faint carvings adorn the walls, but they are too worn to decipher.",
    "You sense a lingering chill in this otherwise empty room.",
    "The silence here is heavy, almost oppressive.",
    "Patches of moss cling to the damp stone walls.",
    "Spiderwebs stretch across corners, undisturbed.",
    "You see nothing of value in this forgotten chamber.",
    "The air is stale and lifeless in this empty room.",
    "The room is unnaturally cold. Your breath is clearly visible.",
    "The room is eire and sinister. Mist clings to the floor.",
    "The room is very warm. It would be relaxing if not for the bones.",
    "The room is pitch black. You can barely see your feet.",
    "The room is cool and you feel a slight breeze.",
    "The room seems to sway. Honestly you feel slightly sick.",
    "The room smells of garlic. At Least no vampires in this version.",
    "The room seems to be made of cheese? Probably not best to eat.",
    "The room resembles a doll house. Now this is just creepy.",
    "The room coughs politely.",
    "The room is judging you.",
    "The room would never give you up.",
    "The room would never let you down.",
    "The room would never go around and hurt you.",
    "The room has a small bird trying to fly while holding a coconut struggling in the corner.",
    "The room seems to be home to a family of rats. They are quite an unusual size",
    "The room is dark. In the corner you spot two large glowing eyes glaring right at you",
    "The room seems to be in another world.A sign above you says Central Park Zoo",
    "The room is bare except for a lone flower pot in the corner.When you enter you could have sworn you heard the flower complaining.\nOh no not again",
    "The room is for copyright reasons strangely silent.",
    "The room brings all the boys to the yard.",
    "The room let the dogs out.",
    "The room comes into view.Wooden floor and swaying from side to side.",
    "The room shouts IT'S MY MONEY AND I NEED IT NOW!",
    "The room in a quiet voice asks you politely to take your shoes off.",
    "The room is filled with the sounds of smoooooth jazz.",
    "You can smell the sea from where you stand.Water splashing in from the round windows tells you that you aren't in the cave anymore.",
    "The room appears to have landed on someone.You spot some red slippers on the feet sticking out.",
    "The room seems to be a tunnel. You spot two bright lets off to the right.They are getting closer.The room starts to shake!.",
    "The room is OUCH! the room has a really short door frame!",
    "The room has padded walls. Maybe its where you belong.",
    "The room another adventurer you wave excitedly! Oh its just a mirror...",
    "The room is coded in Python!",
    "The room if it was to ever leave you.",
    "The room it wouldn't be in summer",
    "The room IS FILLED WITH RADISHES!!!",
    "The room is dark. Only a flickering fire lights the walls.",
    "The room echos a steady drip drip drip.",
    "The room is not your biggest fan.",
    "The room has a favorite flower it is a lily.",
    "The room has little time and appears to be rushing you.",
    "The room is filled with panicking people.",
    "The room appears to be a disco.",
    "The room is entirely in black and white.",
    "The room has a chair seemingly nailed to the ceiling.",
    "So many clowns.",
    "The room won't stop believing.",
    "The room is holding onto a feeling.",
    "The room was born to run.",
    "The room down rocky cliffs.",
    "The room is the next lich king.",
    "Try it for free at room.com rated T for teen.",
    "8008135",
    "('''\\(-_-)/''')",
    "ERROR FUNNY NOT FOUND",
    "is tired of writing nonsense.",
    ":D",
    ":P",
    "D:",
    ":)",
    ":("
]

def roomroll():
    global roomlvl  # Make sure to access the global roomlvl
    level_probabilities = roomtable_probabilities.get(roomlvl, roomtable_probabilities.get(max(roomtable_probabilities.keys())))
    if not level_probabilities:
        return "empty"
    content_choices = list(level_probabilities.keys())
    probabilities = list(level_probabilities.values())
    rolled_content = random.choices(content_choices, weights=probabilities, k=1)[0]
    print(f"  Rolled content: {rolled_content}")  # Debug print
    return rolled_content

def generate_monster_for_room_content(room_content, roomlvl):
    # No need for a separate monster_types dictionary!
    print(f"--- generate_monster_for_room_content called ---")
    print(f"  room_content: {room_content}")
    monster_name = room_content_options.get(room_content.lower())  # Use room_content_options directly
    print(f"  monster_name (after lookup): {monster_name}")

    if monster_name:
        monster_instance = create_monster(monster_name, roomlvl)
        return monster_instance
    else:
        print(f"  No monster found for room content: {room_content}")
        return None

    
def generate_room(room_id, name, roomlvl):
    room_content = roomroll()
    monster = None
    room_type = 0
    print(f"--- generate_room() called for {room_id} ---")
    print(f"  room content is {room_content}")
    if room_content.lower() in room_content_options and room_content_options[room_content.lower()] is not None:  # Check if it's a monster
        monster = generate_monster_for_room_content(room_content, roomlvl)
        room_type = 1
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)
    elif room_content == "chest":
        room_type = 2
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)
    elif room_content == "trap":
        room_type = 3
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS) #will fix later
    elif room_content == "staircase_down":
        room_type = 4
        content_description = "You found a staircase leading down."
    else:
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)  # Add this line

    room = {
        "id": room_id,
        "name": name,
        "content": room_content,
        "description": content_description,
        "monster": monster,
        "type": room_type
    }
    return room


def create_room_dictionary(roomlvl): # <--- Added roomlvl parameter to create_room_dictionary
    number_of_rooms = BASE_ROOMS_PER_FLOOR + (roomlvl * ROOMS_PER_LEVEL_INCREASE_FACTOR)
    rooms = {}
    for i in range(1, int(number_of_rooms) + 1): # Ensure number_of_rooms is int for range
        room_id = f"room{i}"
        room_name = f"Room {i}"
        rooms[room_id] = generate_room(room_id, room_name, roomlvl) # <--- Pass roomlvl to generate_room!
    return rooms
rooms = create_room_dictionary(roomlvl)
REST_OPTIONS = {
    "Barn Loft": {
        "name": "Barn Loft",
        "cost": 5,
        "hp_restore": 20,
        "mana_restore": 30,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.1,
        "defense_boost_percentage": 0.0,
        "duration": 5,
        "description": "Might roll on a needle." 
    },
    "Simple Room": {
        "name": "Simple Room",
        "cost": 15,
        "hp_restore": 50,
        "mana_restore": 40,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.30,
        "defense_boost_percentage": 0.1,
        "duration": 8,
        "description": "A soft bed with fresh linens."
    },
    "Private Room": {
        "name": "Private Room",
        "cost": 30,
        "hp_restore": 100,
        "mana_restore": 100,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.50,
        "defense_boost_percentage": 0.20,
        "duration": 12,
        "description": "Even comes with company..." 
    }
}
#PLAYER ACTIONS
def apply_rest_buff(player, rest_option):
    hp_restore = rest_option["hp_restore"]
    mana_restore = rest_option["mana_restore"]
    cost = rest_option["cost"]
    attack_boost_percentage = rest_option["attack_boost_percentage"]
    defense_boost_percentage = rest_option["defense_boost_percentage"]
    duration = rest_option["duration"]
    # --- 1. Apply Immediate HP Restoration --- (No change needed here)
    if hp_restore > 0:
        player.current_health += hp_restore
        player.current_health = min(player.current_health, player.stats["health"])
        print(f"{player.get_name()} restored {hp_restore} health by resting.")
    # --- 1b. Apply Immediate Mana Restoration --- (No change needed here)
    if mana_restore > 0:
        player.current_mana += mana_restore
        player.current_mana = min(player.current_mana, player.stats["mana"])
        print(f"{player.get_name()} restored {mana_restore} mana by resting.")
    # --- 2a. Apply Attack Boost Buff --- (Modified to set buff_type)
    if attack_boost_percentage > 0:
        attack_buff_data = {
            "name": f"Rest - {rest_option['name']} Attack Buff",
            "stat": "attack_buff",
            "amount": attack_boost_percentage,
            "is_percentage_buff": True,
            "duration_turns": duration,
            "buff_type": "rest" # <---- SET buff_type to "rest" - CRUCIAL!
        }
        player.apply_buff(attack_buff_data)
    # --- 2b. Apply Defense Boost Buff --- (Modified to set buff_type)
    if defense_boost_percentage > 0:
        defense_buff_data = {
            "name": f"Rest - {rest_option['name']} Defense Buff",
            "stat": "defense_buff",
            "amount": defense_boost_percentage,
            "is_percentage_buff": True,
            "duration_turns": duration,
            "buff_type": "rest" # <---- SET buff_type to "rest" - CRUCIAL!
        }
        player.apply_buff(defense_buff_data)     
def descend_staircase():
    global current_room_id, roomlvl, rooms, CURRENT_STATE, current_enemy, player_turn # <--- Include CURRENT_STATE, current_enemy, player_turn in globals
    print("You descend the staircase...")
    roomlvl += 1
    rooms = create_room_dictionary(roomlvl)
    current_room_id = "room1"
    current_room = rooms[current_room_id]
    print(f"You are now on Dungeon Level: {roomlvl}")
    print(f"Room: {rooms[current_room_id]['name']}.")
    print(f"Checking for monster in room: {current_room_id}")
    if current_room["monster"]:
        current_enemy = current_room["monster"]
        print(f"A {current_enemy.get_name()} appears!")
        CURRENT_STATE = COMBAT
        player_turn = True
def move():
    global current_room_id, CURRENT_STATE, current_enemy, roomlvl, rooms, player_turn # Keep player_turn if you use it globally
    current_room = rooms[current_room_id] # <---- Fetch current_room ONCE at the beginning
    if current_room["monster"] and current_room["monster"].is_alive():
        print("You cannot leave while a monster is alive!")
        return
    next_room_number = int(current_room_id[4:]) + 1
    next_room_id = f"room{next_room_number}"
    next_room_name = f"Room {next_room_number}"
    if next_room_id not in rooms:
        rooms[next_room_id] = generate_room(next_room_id, next_room_name, roomlvl) # <---- Pass roomlvl here in move()!
    current_room_id = next_room_id
    print(f"Room: {rooms[current_room_id]['name']}.")
    print(f"Checking for monster in room: {current_room_id}")
    current_room = rooms[current_room_id]
    if current_room["monster"]:
        print("Monster found!")
        current_enemy = current_room["monster"]
        print(f"Initial type of current_enemy.attack when combat starts in move(): {type(current_enemy.attack)}")
        print("Before setting CURRENT_STATE = COMBAT")
        CURRENT_STATE = COMBAT
        player_turn = True
        print("After setting CURRENT_STATE = COMBAT")
        print(f"A {current_enemy.get_name()} appears!")
        print(f"Current State: {CURRENT_STATE}")
        print(f"Current Enemy: {current_enemy}")
    elif current_room["type"] == 2: # Corrected to type 2 for chest, was type 3 in original prompt - assuming type 2 is treasure/chest
        print("A chest is here!")
    else:
        print("An empty room.")
def reset_game_state():
    global player, rooms, current_room_id, roomlvl, current_enemy, CURRENT_STATE, player_turn
    print("Resetting Game State...")
    # --- 2. Regenerate Dungeon ---
    roomlvl = 0  # Reset to starting dungeon level (usually 0 or 1)
    rooms = create_room_dictionary(roomlvl) 
    current_room_id = "room1" # Set player to start at the first room of the new dungeon
    print("Dungeon regenerated.")
    # --- 3. Reset Combat State ---
    current_enemy = None  
    CURRENT_STATE = MENU  
    player_turn = True   
    print("Combat state reset.")
    print("Game state reset complete. Ready for a new game run.")
# --- Text wrapping function (add this function to your code if you don't have one already) ---
def wrap_text(text, font, max_width):
    """Wraps text to fit within a given width using a given font."""
    words = text.split()
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        text_width, text_height = font.size(test_line)
        if text_width > max_width:
            wrapped_lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    wrapped_lines.append(current_line) # Add the last line
    return wrapped_lines
#Drawing
def draw_inventory_tabs():  # <--- Moved ABOVE draw_inventory()
    global current_inventory_category_index
    for i, category_name in enumerate(INVENTORY_CATEGORIES):
        tab_rect = pygame.Rect(INVENTORY_TAB_START_X + i * INVENTORY_TAB_WIDTH, INVENTORY_TAB_Y, INVENTORY_TAB_WIDTH, INVENTORY_TAB_HEIGHT)
        tab_color = TAB_COLOR  # Use the existing TAB_COLOR
        if i == current_inventory_category_index:
            tab_color = SELECTED_TAB_COLOR  # Use selected color
        pygame.draw.rect(screen, tab_color, tab_rect)
        tab_text_surface = SMALL_FONT.render(category_name, True, WHITE)
        tab_text_rect = tab_text_surface.get_rect(center=tab_rect.center)
        screen.blit(tab_text_surface, tab_text_rect)

def draw_inventory():
    global selected_inventory_item, inventory_scroll_offset, current_inventory_items
    pygame.draw.rect(screen, BROWN, INVENTORY_DISPLAY_RECT)  # Background
    pygame.draw.rect(screen, BLACK, INVENTORY_DISPLAY_RECT, 2)  # Border

    draw_inventory_tabs() # Now this call is valid

    for row in range(INVENTORY_ROWS):
        for col in range(INVENTORY_SLOTS_PER_ROW):
            index = row * INVENTORY_SLOTS_PER_ROW + col + inventory_scroll_offset
            slot_x = INVENTORY_START_X + col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_SPACING)
            slot_y = INVENTORY_START_Y + row * (INVENTORY_SLOT_HEIGHT + INVENTORY_SLOT_SPACING)
            slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_DISPLAY_WIDTH - 60, INVENTORY_SLOT_HEIGHT)

            # --- Draw Slot Background (Always) ---
            pygame.draw.rect(screen, (150, 150, 150), slot_rect)

            # --- Highlight if selected ---
            if index < len(current_inventory_items):
                item_id = current_inventory_items[index]
                if item_id == selected_inventory_item:
                    pygame.draw.rect(screen, PURPLE, slot_rect)

            pygame.draw.rect(screen, BLACK, slot_rect, 1)

            if index < len(current_inventory_items):
                item_id = current_inventory_items[index]
                item_data = shop_items_data[item_id]  # Get item data

                # --- Draw Image (Left Side) ---
                item_image = item_data.get("image")
                if item_image:
                    scaled_image = pygame.transform.scale(item_image, (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE))
                    screen.blit(scaled_image, (slot_x, slot_y))

                # --- Text Positioning (Right Side) ---
                text_x = slot_x + INVENTORY_SLOT_SIZE + 10  # Shift text to the right of the image
                text_y = slot_y + 5

                # --- Item Name ---
                item_name = item_data["name"]
                item_text_surface = SMALL_FONT.render(item_name, True, WHITE)
                screen.blit(item_text_surface, (text_x, text_y))
                text_y += 20  # Move down for the next line of text


                # --- Item Stats/Effects (Conditional) ---
                if item_data["category"] in ("Potions", "Scrolls"):
                    if item_data["effect"]["type"] == "heal":
                        effect_text = f"Heals: {item_data['effect']['amount']} HP"
                    elif item_data["effect"]["type"] == "mana":
                         effect_text = f"Restores: {item_data['effect']['amount']} MP"
                    elif item_data["effect"]["type"] == "damage":
                        effect_text = f"Damage: {item_data['effect']['amount']}"
                    else:
                        effect_text = ""
                    effect_surface = SMALL_FONT.render(effect_text, True, BLUE)  # Consistent color
                    screen.blit(effect_surface, (text_x, text_y))
                    text_y += 20 #move down

                elif item_data["category"] in ("Weapons", "Armor", "Helmets", "Rings"):
                    if "stats_bonus" in item_data:
                        for stat, bonus in item_data["stats_bonus"].items():
                            stat_text = f"{stat.capitalize()}: +{bonus}"
                            stat_surface = SMALL_FONT.render(stat_text, True, GREEN)
                            screen.blit(stat_surface, (text_x, text_y))
                            text_y += 20 #move text

    # --- Draw Scroll Buttons ---
    pygame.draw.rect(screen, LIGHT_GRAY, INVENTORY_SCROLL_UP_BUTTON_RECT)  # Up button
    pygame.draw.rect(screen, LIGHT_GRAY, INVENTORY_SCROLL_DOWN_BUTTON_RECT)  # Down button
    pygame.draw.polygon(screen, BLACK, [(INVENTORY_SCROLL_UP_BUTTON_X + 15, INVENTORY_SCROLL_UP_BUTTON_Y + 5),(INVENTORY_SCROLL_UP_BUTTON_X + 5, INVENTORY_SCROLL_UP_BUTTON_Y + 25), (INVENTORY_SCROLL_UP_BUTTON_X + 25, INVENTORY_SCROLL_UP_BUTTON_Y + 25)])
    pygame.draw.polygon(screen, BLACK, [(INVENTORY_SCROLL_DOWN_BUTTON_X + 15, INVENTORY_SCROLL_DOWN_BUTTON_Y + 25),(INVENTORY_SCROLL_DOWN_BUTTON_X + 5, INVENTORY_SCROLL_DOWN_BUTTON_Y + 5), (INVENTORY_SCROLL_DOWN_BUTTON_X + 25, INVENTORY_SCROLL_DOWN_BUTTON_Y + 5)])

def filter_inventory_by_category():
    global current_inventory_items, current_inventory_category_index
    current_inventory_items = []
    selected_category = INVENTORY_CATEGORIES[current_inventory_category_index]
    for item_id in player.inventory:
        if shop_items_data[item_id]["category"] == selected_category:
            # --- Combat Inventory Filtering ---
            if CURRENT_STATE == INVENTORY_IN_COMBAT:
                if shop_items_data[item_id]['category'] in ("Potions", "Scrolls"):
                    current_inventory_items.append(item_id)
            else:
                current_inventory_items.append(item_id) #add items

def draw_shop_menu():
    pygame.draw.rect(screen, SHOP_MENU_COLOR, SHOP_MENU_RECT) # Main shop menu box
    draw_shop_tabs() # Call function to draw tabs
    draw_item_slots() # Call function to draw item slots
    draw_shop_scroll_buttons() # Call function to draw scroll buttons
def draw_item_slots():
    global selected_shop_item, shop_scroll_offset, current_shop_items

    if not current_shop_items:
        return  # Exit early if the list is empty

    for i in range(4):  # Display up to 4 items
        slot_rect = pygame.Rect(
            ITEM_SLOTS_START_X,
            ITEM_SLOTS_START_Y + i * (ITEM_SLOT_HEIGHT + ITEM_SLOT_SPACING_Y),
            ITEM_SLOT_WIDTH,
            ITEM_SLOT_HEIGHT
        )

        index = i + shop_scroll_offset   # Calculate the CORRECT index

        # --- Highlight if selected ---
        if index < len(current_shop_items): #bounds check
            item_id = current_shop_items[index]
            if item_id == selected_shop_item:
                pygame.draw.rect(screen, PURPLE, slot_rect)  # Highlight

        pygame.draw.rect(screen, SLOT_COLOR, slot_rect)  # Draw item slot
        pygame.draw.rect(screen, BLACK, slot_rect, 1)


        if index < len(current_shop_items): #check in bounds
            item_id = current_shop_items[index]  # Access with calculated index
            item_data = shop_items_data[item_id]
            item_name = item_data["name"]

            # --- Draw Image (Left Side) ---
            item_image = item_data.get("image")
            if item_image:
                scaled_image = pygame.transform.scale(item_image, (64, 64))  # Scale to 64x64
                screen.blit(scaled_image, (slot_rect.x + 5, slot_rect.y + 5))  # Position on the left

            # --- Text Positioning (Right Side) ---
            text_x = slot_rect.x + 64 + 15  #  After the image + padding
            text_y = slot_rect.y + 5

            # --- Item Name ---
            item_text_surface = SMALL_FONT.render(item_name, True, WHITE)
            screen.blit(item_text_surface, (text_x, text_y))
            text_y += 20

            # --- Item Price ---
            price_text = f"Price: {item_data['price']} Gold"
            price_surface = SMALL_FONT.render(price_text, True, YELLOW)  # Gold color
            screen.blit(price_surface, (text_x, text_y))
            text_y += 20

            # --- Item Stats/Effects (Conditional) ---
            if item_data["category"] in ("Potions", "Scrolls"):
                if item_data["effect"]["type"] == "heal":
                    effect_text = f"Heals: {item_data['effect']['amount']} HP"
                elif item_data["effect"]["type"] == "mana":
                    effect_text = f"Restores: {item_data['effect']['amount']} MP"
                elif item_data["effect"]["type"] == "damage":
                    effect_text = f"Damage: {item_data['effect']['amount']}"
                else:
                    effect_text = ""
                effect_surface = SMALL_FONT.render(effect_text, True, BLUE)
                screen.blit(effect_surface, (text_x, text_y))
                text_y += 20
            elif item_data["category"] in ("Weapons", "Armor", "Helmets", "Rings"):
                if "stats_bonus" in item_data:
                    for stat, bonus in item_data["stats_bonus"].items():
                        stat_text = f"{stat.capitalize()}: +{bonus}"
                        stat_surface = SMALL_FONT.render(stat_text, True, GREEN)
                        screen.blit(stat_surface, (text_x, text_y))
                        text_y += 20

def draw_shop_scroll_buttons():
    """Draws the shop scroll up and down buttons."""
    # Scroll Up Button
    pygame.draw.rect(screen, BUTTON_COLOR, SHOP_SCROLL_UP_BUTTON_RECT)
    # Draw a simple up arrow (triangle)
    pygame.draw.polygon(screen, BLACK, [
        (SHOP_SCROLL_UP_BUTTON_RECT.centerx, SHOP_SCROLL_UP_BUTTON_RECT.top + 5),
        (SHOP_SCROLL_UP_BUTTON_RECT.left + 5, SHOP_SCROLL_UP_BUTTON_RECT.bottom - 5),
        (SHOP_SCROLL_UP_BUTTON_RECT.right - 5, SHOP_SCROLL_UP_BUTTON_RECT.bottom - 5)
    ])

    # Scroll Down Button
    pygame.draw.rect(screen, BUTTON_COLOR, SHOP_SCROLL_DOWN_BUTTON_RECT)
    # Draw a simple down arrow (triangle)
    pygame.draw.polygon(screen, BLACK, [
        (SHOP_SCROLL_DOWN_BUTTON_RECT.centerx, SHOP_SCROLL_DOWN_BUTTON_RECT.bottom - 5),
        (SHOP_SCROLL_DOWN_BUTTON_RECT.left + 5, SHOP_SCROLL_DOWN_BUTTON_RECT.top + 5),
        (SHOP_SCROLL_DOWN_BUTTON_RECT.right - 5, SHOP_SCROLL_DOWN_BUTTON_RECT.top + 5)
    ])
def draw_shop_menu():
    global current_shop_items, shop_scroll_offset, selected_shop_item, SHOP_CATEGORIES, current_shop_category_index

    pygame.draw.rect(screen, SHOP_MENU_COLOR, SHOP_MENU_RECT)  # Main shop menu box
    pygame.draw.rect(screen, BLACK, SHOP_MENU_RECT, 2) #add a border

    # --- Draw Tabs ---
    for i, category in enumerate(SHOP_CATEGORIES):
        tab_x = TAB_START_X + i * TAB_WIDTH  # Calculate x position
        tab_rect = pygame.Rect(tab_x, TAB_Y, TAB_WIDTH, TAB_HEIGHT)
        SHOP_TAB_RECTS[i] = tab_rect  # Store tab rect *CORRECTLY*

        # Highlight the selected tab
        if i == current_shop_category_index:
            pygame.draw.rect(screen, SELECTED_TAB_COLOR, tab_rect)  # Highlight
        else:
            pygame.draw.rect(screen, TAB_COLOR, tab_rect)
        pygame.draw.rect(screen, BLACK, tab_rect, 1)  # Border

        text_surface = SMALL_FONT.render(category, True, WHITE)
        text_rect = text_surface.get_rect(center=tab_rect.center)
        screen.blit(text_surface, text_rect)

    # --- Draw Item Slots (CORRECTED) ---
    visible_items = 4  # Number of items to display at once
    start_index = shop_scroll_offset
    end_index = shop_scroll_offset + visible_items
    items_to_display = current_shop_items[start_index:end_index] #get the items

    for index, item_id in enumerate(items_to_display): #loop the items
        item_data = shop_items_data[item_id]
        slot_y = ITEM_SLOTS_START_Y + index * (ITEM_SLOT_HEIGHT + ITEM_SLOT_SPACING_Y) #get each y
        item_slot_rect = pygame.Rect(ITEM_SLOTS_START_X, slot_y, ITEM_SLOT_WIDTH, ITEM_SLOT_HEIGHT) #get each rect
        pygame.draw.rect(screen, SLOT_COLOR, item_slot_rect) #draw
        pygame.draw.rect(screen, BLACK, item_slot_rect, 1)

        # --- Item Image ---
        item_image = item_data.get("image")
        if item_image:
          scaled_image = pygame.transform.scale(item_image,(64,64))
          screen.blit(scaled_image, (item_slot_rect.x + 5, item_slot_rect.y + 5))

        # --- Text Positioning (Right Side) ---
        text_x = item_slot_rect.x + 64 + 15  # After the image + padding
        text_y = item_slot_rect.y + 5

        # --- Item Name ---
        item_text_surface = SMALL_FONT.render(item_data["name"], True, WHITE)
        screen.blit(item_text_surface, (text_x, text_y))
        text_y += 20

        # --- Item Price ---
        price_text = f"Price: {item_data['price']} Gold"
        price_surface = SMALL_FONT.render(price_text, True, YELLOW)
        screen.blit(price_surface, (text_x, text_y))
        text_y += 20

        # --- Item Stats/Effects (Conditional) ---
        if item_data["category"] in ("Potions", "Scrolls"):
            if item_data["effect"]["type"] == "heal":
                effect_text = f"Heals: {item_data['effect']['amount']} HP"
            elif item_data["effect"]["type"] == "mana":
                effect_text = f"Restores: {item_data['effect']['amount']} MP"
            elif item_data["effect"]["type"] == "damage":
                effect_text = f"Damage: {item_data['effect']['amount']}"
            else:
                effect_text = ""
            effect_surface = SMALL_FONT.render(effect_text, True, BLUE)
            screen.blit(effect_surface, (text_x, text_y))
            text_y += 20
        elif item_data["category"] in ("Weapons", "Armor", "Helmets", "Rings"):
            if "stats_bonus" in item_data:
                for stat, bonus in item_data["stats_bonus"].items():
                    stat_text = f"{stat.capitalize()}: +{bonus}"
                    stat_surface = SMALL_FONT.render(stat_text, True, GREEN)
                    screen.blit(stat_surface, (text_x, text_y))
                    text_y += 20
         # --- Highlight Selected Item ---
        if selected_shop_item == item_id:
            pygame.draw.rect(screen, PURPLE, item_slot_rect, 3)
    draw_shop_scroll_buttons()

def load_shop_item_images():
    for item_id, item_info in shop_items_data.items():
        image_path = item_info.get("image_path")
        if image_path:
            try:
                # --- USE resource_path HERE! ---
                full_image_path = resource_path(image_path)  # Get FULL resource path
                image = pygame.image.load(full_image_path).convert_alpha()  # Load image using FULL path
                shop_items_data[item_id]["image"] = image
            except pygame.error as e:
                print(f"ERROR: Could not load shop item image for {item_id} from: {full_image_path}")  # Error print (using FULL path)
                print(f"Pygame error: {e}")  # Print specific Pygame error message
                shop_items_data[item_id]["image"] = None
            except FileNotFoundError:  # Catch FileNotFoundError explicitly
                print(f"ERROR: File not found for shop item {item_id} at path: {full_image_path}")  # More specific error for file not found
                shop_items_data[item_id]["image"] = None
        else:
            print(f"WARNING: No image_path defined for item {item_id}")
            shop_items_data[item_id]["image"] = None

load_shop_item_images()  # Make sure this is called!
def filter_shop_items():
    global shop_items_data, current_shop_items, current_shop_category_index, SHOP_CATEGORIES
    current_shop_items = []
    current_category = SHOP_CATEGORIES[current_shop_category_index]

    for item_id, item_data in shop_items_data.items():
        if item_data["category"] == current_category:
            current_shop_items.append(item_id)
def reset_shop_scroll():
    """Resets the shop scroll offset to 0."""
    global shop_scroll_offset
    shop_scroll_offset = 0  
def draw_shop_tabs():
    global current_shop_category_index # Need to access and potentially modify this
    for i, category_name in enumerate(SHOP_CATEGORIES):
        tab_rect = pygame.Rect(TAB_START_X + i * TAB_WIDTH, TAB_Y, TAB_WIDTH, TAB_HEIGHT)
        tab_color_to_use = TAB_COLOR # Default tab color
        if i == current_shop_category_index: # Check if this tab is the selected one
            tab_color_to_use = SELECTED_TAB_COLOR # Use brighter color for selected tab
        pygame.draw.rect(screen, tab_color_to_use, tab_rect) # Draw tab rectangle with color
        tab_text_surface = SMALL_FONT.render(category_name, True, WHITE) # Render category name
        tab_text_rect = tab_text_surface.get_rect(center=tab_rect.center)
        screen.blit(tab_text_surface, tab_text_rect)
def render_combat_buttons():
    if ability_menu_open:
        # --- Ability Menu Box ---
        menu_width = 400
        menu_height = 300
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, LIGHT_GRAY, menu_rect) # Background for menu box
        pygame.draw.rect(screen, BLACK, menu_rect, 2) # Border for menu box
        # --- "Exit" Button (Top Right of Ability Menu) ---
        exit_button_width = 60
        exit_button_height = 25
        exit_button_x = menu_x + menu_width - exit_button_width - 10
        exit_button_y = menu_y + 10
        exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
        pygame.draw.rect(screen, WHITE, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 1)
        exit_text = SMALL_FONT.render("Exit", True, BLACK)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)
        # --- Ability Buttons with Name, Cost, Description ---
        ability_button_y_start = menu_y + 50
        ability_button_spacing = 70 # Increased spacing to accommodate multiple lines of text
        ability_button_width = menu_width - 40 # Wider buttons inside menu
        ability_button_height = 60 # Increased button height
        player_class_name = player.class_name
        if player_class_name in CLASS_ABILITIES:
            abilities = CLASS_ABILITIES[player_class_name]
            num_abilities_to_display = 4 # Display up to 4 abilities at a time
            for i in range(num_abilities_to_display): # Display up to 4 abilities for now
                ability_index_to_display = i # For now, display abilities starting from index 0. We'll add scrolling later
                if ability_index_to_display < len(abilities): # Check if ability_index is within valid range
                    ability = abilities[ability_index_to_display]
                    ability_button_rect = pygame.Rect(menu_x + 20, ability_button_y_start + i * ability_button_spacing, ability_button_width, ability_button_height)
                    pygame.draw.rect(screen, WHITE, ability_button_rect)
                    pygame.draw.rect(screen, BLACK, ability_button_rect, 1)
                    # --- Render Ability Name ---
                    ability_name_text = BUTTON_FONT.render(ability["name"], True, BLACK) # Use BUTTON_FONT for name
                    ability_name_rect = ability_name_text.get_rect(topleft=(ability_button_rect.x + 5, ability_button_rect.y + 5)) # Position at top-left of button
                    screen.blit(ability_name_text, ability_name_rect)
                    # --- Render Mana Cost ---
                    mana_cost_text = SMALL_FONT.render(f"Cost: {ability['mana_cost']} MP", True, BLUE) # Use SMALL_FONT for cost
                    mana_cost_rect = mana_cost_text.get_rect(topleft=(ability_button_rect.x + 5, ability_button_rect.y + 25)) # Position below name
                    screen.blit(mana_cost_text, mana_cost_rect)
                    # --- Render Shortened Description ---
                    description_text = SMALL_FONT.render(ability["description"][:30] + "...", True, BLACK) # Shorten description and add "..."
                    description_rect = description_text.get_rect(topleft=(ability_button_rect.x + 5, ability_button_rect.y + 45)) # Position below cost
                    screen.blit(description_text, description_rect)
        # --- Scroll Buttons ---
        scroll_button_width = 30
        scroll_button_height = 25
        scroll_button_x = menu_x + menu_width - scroll_button_width - 10 # Right side of menu, below Exit
        scroll_up_button_y = menu_y + 50 # Position for "Up" button
        scroll_down_button_y = menu_y + menu_height - scroll_button_height - 50 # Position for "Down" button (near bottom)
        # --- "Up" Scroll Button ---
        scroll_up_button_rect = pygame.Rect(scroll_button_x, scroll_up_button_y, scroll_button_width, scroll_button_height)
        pygame.draw.rect(screen, WHITE, scroll_up_button_rect)
        pygame.draw.rect(screen, BLACK, scroll_up_button_rect, 1)
        up_arrow_text = SMALL_FONT.render("^", True, BLACK) # Simple up arrow
        up_arrow_text_rect = up_arrow_text.get_rect(center=scroll_up_button_rect.center)
        screen.blit(up_arrow_text, up_arrow_text_rect)
        # --- "Down" Scroll Button ---
        scroll_down_button_rect = pygame.Rect(scroll_button_x, scroll_down_button_y, scroll_button_width, scroll_button_height)
        pygame.draw.rect(screen, WHITE, scroll_down_button_rect)
        pygame.draw.rect(screen, BLACK, scroll_down_button_rect, 1)
        down_arrow_text = SMALL_FONT.render("v", True, BLACK) # Simple down arrow
        down_arrow_text_rect = down_arrow_text.get_rect(center=scroll_down_button_rect.center)
        screen.blit(down_arrow_text, down_arrow_text_rect)
#Handler Functions Menu Character Town dungeon Comabt
def handle_menu():
    screen.fill(GRAY)
    screen.blit(MENU_TITLE_TEXT,MENU_TITLE_RECT)
    pygame.draw.rect(screen, WHITE, NEW_GAME_BUTTON_RECT, border_radius=10)
    pygame.draw.rect(screen, WHITE, LOAD_GAME_BUTTON_RECT, border_radius=10)
    pygame.draw.rect(screen, WHITE, OPTIONS_BUTTON_RECT, border_radius=10)
    pygame.draw.rect(screen, WHITE, QUIT_BUTTON_RECT, border_radius=10)
    screen.blit(NEW_GAME_TEXT, NEW_GAME_TEXT.get_rect(center=NEW_GAME_BUTTON_RECT.center))
    screen.blit(LOAD_GAME_TEXT, LOAD_GAME_TEXT.get_rect(center=LOAD_GAME_BUTTON_RECT.center))
    screen.blit(OPTIONS_TEXT, OPTIONS_TEXT.get_rect(center=OPTIONS_BUTTON_RECT.center))
    screen.blit(QUIT_TEXT, QUIT_TEXT.get_rect(center=QUIT_BUTTON_RECT.center))
def handle_menu_events(events):
    global CURRENT_STATE
    mouse_pos = pygame.mouse.get_pos() # Get mouse position outside the event loop for general mouse pos
    for event in events: # Iterate through events - IMPORTANT for proper event handling
        if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse button press event (click)
            if event.button == 1:
                if NEW_GAME_BUTTON_RECT.collidepoint(event.pos): # Use event.pos for click position
                    CURRENT_STATE = CHARACTER_CREATION
                elif LOAD_GAME_BUTTON_RECT.collidepoint(event.pos):
                    print("Load Game Clicked")
                elif OPTIONS_BUTTON_RECT.collidepoint(event.pos):
                    print("Options Clicked")
                elif QUIT_BUTTON_RECT.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
def handle_game_over():
    screen.fill(BLACK) # Fill screen with black background
    # --- "Game Over" Text ---
    game_over_font = pygame.font.Font("freesansbold.ttf", 64)
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)) # Positioned slightly above center
    screen.blit(game_over_text, game_over_rect)
    # --- "Retry" Button ---
    pygame.draw.rect(screen, GREEN, RETRY_BUTTON_RECT) # Draw the button rectangle in green
    retry_font = pygame.font.Font("freesansbold.ttf", 32) # Smaller font for button text
    retry_text = retry_font.render("Retry", True, BLACK) # "Retry" text in black
    retry_text_rect = retry_text.get_rect(center=RETRY_BUTTON_RECT.center)
    screen.blit(retry_text, retry_text_rect)
    pygame.display.flip() 
def handle_game_over_events(events):
    global CURRENT_STATE 
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if RETRY_BUTTON_RECT.collidepoint(mouse_pos):
                reset_game_state() 
                CURRENT_STATE = MENU 
def handle_character_creation():
    global INPUT_ACTIVE, PLAYER_NAME, PLAYER_CLASS_NAME, PLAYER
    screen.fill(BLACK)
    screen.blit(CHARACTER_TITLE_TEXT, CHARACTER_TITLE_RECT)
    # Name Input
    pygame.draw.rect(screen, WHITE, NAME_INPUT_RECT, 2)
    if INPUT_ACTIVE:
        pygame.draw.rect(screen, GREEN, NAME_INPUT_RECT, 2)
    else:
        pygame.draw.rect(screen, WHITE, NAME_INPUT_RECT, 2)
    name_input_text = CHARACTER_FONT.render("Name: " + PLAYER_NAME, True, WHITE)
    screen.blit(name_input_text, (NAME_INPUT_RECT.x + 10, NAME_INPUT_RECT.y + 10))
    # Class Selection
    class_text = "Select Class" if PLAYER_CLASS_NAME is None else f"Class: {PLAYER_CLASS_NAME}"
    class_button_text = CHARACTER_FONT.render(class_text, True, WHITE)
    pygame.draw.rect(screen, WHITE, CLASS_BUTTON_RECT, 2)
    screen.blit(class_button_text, class_button_text.get_rect(center=CLASS_BUTTON_RECT.center))
    # Start Game Button
    start_game_button_text = CHARACTER_FONT.render("Start Game", True, WHITE)
    pygame.draw.rect(screen, WHITE, START_GAME_BUTTON_RECT, 2)
    screen.blit(start_game_button_text, start_game_button_text.get_rect(center=START_GAME_BUTTON_RECT.center))
def handle_character_creation_events(events):
    global INPUT_ACTIVE, PLAYER_NAME, PLAYER_CLASS_NAME, player 
    mouse_pos = pygame.mouse.get_pos() 
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if NAME_INPUT_RECT.collidepoint(mouse_pos):
                    INPUT_ACTIVE = True
                else:
                    INPUT_ACTIVE = False
                if CLASS_BUTTON_RECT.collidepoint(mouse_pos):
                    if PLAYER_CLASS_NAME is None:
                        PLAYER_CLASS_NAME = "Warrior"
                    elif PLAYER_CLASS_NAME == "Warrior":
                        PLAYER_CLASS_NAME = "Mage"
                    elif PLAYER_CLASS_NAME == "Mage":
                        PLAYER_CLASS_NAME = "Rogue"
                    elif PLAYER_CLASS_NAME == "Rogue":
                        PLAYER_CLASS_NAME = "Warrior"
                if START_GAME_BUTTON_RECT.collidepoint(mouse_pos):
                    if PLAYER_NAME and PLAYER_CLASS_NAME:
                        global player, CURRENT_STATE 
                        player = Player(PLAYER_NAME, PLAYER_CLASS_NAME)
                        CURRENT_STATE = TOWN
        elif event.type == pygame.KEYDOWN:  
            if INPUT_ACTIVE:  
                if event.key == pygame.K_RETURN:
                    INPUT_ACTIVE = False
                elif event.key == pygame.K_BACKSPACE:
                    PLAYER_NAME = PLAYER_NAME[:-1]
                else:
                    PLAYER_NAME += event.unicode
def handle_town():
    global CURRENT_STATE,screen
    screen.blit(town_bg_image,(0,0))
    render_status_bar()
def handle_town_events(events):
    global CURRENT_STATE, current_room_id
    mouse_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # --- NEW: Check for equipment button in town ---
                if EQUIPMENT_BUTTON_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = EQUIPMENT_MENU
                    global previous_state
                    previous_state = TOWN
                elif BUTTON1_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = TAVERN
                elif BUTTON2_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = SHOP
                elif BUTTON3_RECT.collidepoint(mouse_pos):
                    # ... (rest of your town event handling) ...
                    CURRENT_STATE = DUNGEON
                    global current_room_id
                    current_room_id = "room1"
                    current_room_data = rooms[current_room_id]
                    if current_room_data["monster"]:
                         global current_enemy
                         current_enemy = current_room_data["monster"]
                         CURRENT_STATE = COMBAT
                    else:
                       print(f"Entering dungeon - room {current_room_id} is clear.")
                elif BUTTON4_RECT.collidepoint(mouse_pos):
                     CURRENT_STATE = MENU
def handle_tavern():
    global CURRENT_STATE, SHOW_REST_OPTIONS_BOX, screen
    screen.blit(tavern_bg_image,(0,0)) 
    # Tavern Title Text
    tavern_font = pygame.font.Font(None, 48)
    tavern_title_text = tavern_font.render("The Cozy Tavern", True, WHITE)
    tavern_title_rect = tavern_title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(tavern_title_text, tavern_title_rect)
    render_status_bar()
    # --- Render Rest Menu (CONDITIONAL - only if SHOW_REST_OPTIONS_BOX is True) ---
    if SHOW_REST_OPTIONS_BOX: 
        render_tavern_rest_menu() 
def render_tavern_rest_menu():
    global SHOW_REST_OPTIONS_BOX, TAVERN_REST_EXIT_BUTTON_RECT 
    TAVERN_REST_EXIT_BUTTON_RECT = None  
    if SHOW_REST_OPTIONS_BOX: 
        # --- Menu Box (reusing combat menu box style) ---
        menu_width = 400
        menu_height = 300
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, LIGHT_GRAY, menu_rect)
        pygame.draw.rect(screen, BLACK, menu_rect, 2)

        # --- "Exit" Button (Top Right) ---
        exit_button_width = 60
        exit_button_height = 25
        exit_button_x = menu_x + menu_width - exit_button_width - 10
        exit_button_y = menu_y + 10
        exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)
        pygame.draw.rect(screen, WHITE, exit_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect, 1)
        exit_text = SMALL_FONT.render("Exit", True, BLACK)
        exit_text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, exit_text_rect)
        # --- Store Exit Button Rect Globally (for event handling) ---
        TAVERN_REST_EXIT_BUTTON_RECT = exit_button_rect 
        # --- Rest Option Buttons ---
        option_button_y_start = menu_y + 50 
        option_button_spacing = 70 
        option_button_width = menu_width - 40 
        option_button_height = 60
        option_index = 0 
        global REST_OPTION_BUTTON_RECTS
        REST_OPTION_BUTTON_RECTS = {} 
        for option_key, option_data in REST_OPTIONS.items(): # Iterate through REST_OPTIONS dictionary
            option_button_rect = pygame.Rect(menu_x + 20, option_button_y_start + option_index * option_button_spacing, option_button_width, option_button_height)
            pygame.draw.rect(screen, WHITE, option_button_rect)
            pygame.draw.rect(screen, BLACK, option_button_rect, 1)
            # --- Render Option Name (like Ability Name) ---
            option_name_text = BUTTON_FONT.render(option_data["name"], True, BLACK) # Use BUTTON_FONT for option name
            option_name_rect = option_name_text.get_rect(topleft=(option_button_rect.x + 5, option_button_rect.y + 5))
            screen.blit(option_name_text, option_name_rect)

            # --- Render Cost (like Mana Cost) ---
            cost_text = SMALL_FONT.render(f"Cost: {option_data['cost']} Gold", True, BLUE) # Use SMALL_FONT, different color
            cost_rect = cost_text.get_rect(topleft=(option_button_rect.x + 5, option_button_rect.y + 25))
            screen.blit(cost_text, cost_rect)

            # --- Render Short Description (like Ability Description - shortened) ---
            description_text = SMALL_FONT.render(option_data["description"][:30] + "...", True, BLACK) # Shorten desc
            description_rect = description_text.get_rect(topleft=(option_button_rect.x + 5, option_button_rect.y + 45))
            screen.blit(description_text, description_rect)

            REST_OPTION_BUTTON_RECTS[option_key] = option_button_rect # Store button rect in the dictionary
            option_index += 1 # Move to the next button position
def handle_rest_option_click(option_key):
    global player, SHOW_REST_OPTIONS_BOX  # Ensure globals are declared
    selected_option = REST_OPTIONS[option_key]
    cost = selected_option["cost"]
    if player.coins >= cost:
        player.coins -= cost
        print("--- handle_rest_option_click: Removing previous REST buffs (buff_type='rest') ---") # Updated debug print
        rest_buffs_to_remove = []
        for buff in player.buffs:
            if buff.get('buff_type') == "rest": # <--- Check for buff_type == "rest"
                print(f"  Found existing rest buff: {buff['name']}, type: {buff.get('buff_type')}") # Debug print with type
                rest_buffs_to_remove.append(buff)
        for buff_to_remove in rest_buffs_to_remove:
            player.buffs.remove(buff_to_remove)
            message_text = (f"Previous rest buff '{buff_to_remove['name']}' removed.")
            add_combat_message(message_text)
        print("--- handle_rest_option_click: Finished removing previous REST buffs (buff_type='rest') ---") # Updated debug print


        # --- Apply the rest buff using the provided apply_rest_buff function ---
        apply_rest_buff(player, selected_option) # Call the apply_rest_buff function
        message_text = (f"{player.name} rests at the {selected_option['name']} and pays {cost} coins.")
        add_combat_message(message_text)

    else:
        message_text = ("Not enough coins to rest here.")
        add_combat_message(message_text)

    SHOW_REST_OPTIONS_BOX = False

def handle_tavern_events(events):
    global CURRENT_STATE, SHOW_REST_OPTIONS_BOX, TAVERN_REST_EXIT_BUTTON_RECT
    for event in events: # <--- CORRECTED: Now iterates through the list of events
      if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse button press event (click) - no button check needed here
        mouse_pos = pygame.mouse.get_pos() # Get mouse position inside MOUSEBUTTONDOWN block
        if EQUIPMENT_BUTTON_RECT.collidepoint(mouse_pos):
            CURRENT_STATE = EQUIPMENT_MENU
            global previous_state
            previous_state = TAVERN
        elif BUTTON1_RECT.collidepoint(mouse_pos): # Check for Status Bar Button 1 (Rest Button) click
          SHOW_REST_OPTIONS_BOX = True

          # --- Handle Rest Options Menu "Exit" Button Click ---
        if SHOW_REST_OPTIONS_BOX and isinstance(TAVERN_REST_EXIT_BUTTON_RECT, pygame.Rect): # <--- ADD isinstance CHECK
          if TAVERN_REST_EXIT_BUTTON_RECT.collidepoint(mouse_pos):
            SHOW_REST_OPTIONS_BOX = False

          # --- Handle Rest Option Button Clicks (only if box is shown AND button rects exist) ---
        if SHOW_REST_OPTIONS_BOX and REST_OPTION_BUTTON_RECTS: # <--- ADD check for REST_OPTION_BUTTON_RECTS being non-empty
          for option_key, button_rect in REST_OPTION_BUTTON_RECTS.items():
            if button_rect.collidepoint(mouse_pos):
              handle_rest_option_click(option_key)
              SHOW_REST_OPTIONS_BOX = False
              break

        if BUTTON4_RECT.collidepoint(mouse_pos): # <--- NOW CHECKING for click on BUTTON4_RECT (Leave Shop Button) - you had BUTTON1_RECT in comment
          CURRENT_STATE = TOWN # Set state back to TOWN This is our current tavern

def handle_shop():
    global CURRENT_STATE, screen
    screen.fill((80, 80, 120))
    filter_shop_items() # Ensure the items are up to date
    draw_shop_menu()
    draw_inventory()
    render_status_bar()

def handle_shop_events(events):
    global CURRENT_STATE, current_shop_category_index, shop_scroll_offset, inventory_scroll_offset
    global selected_shop_item, selected_inventory_item, current_inventory_items

    mouse_pos = pygame.mouse.get_pos()
    filter_inventory_by_category()  # Ensure inventory is filtered

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click
                # --- Tab Switching (Shop) ---
                for i in range(len(SHOP_CATEGORIES)):
                    tab_rect = pygame.Rect(TAB_START_X + i * TAB_WIDTH, TAB_Y, TAB_WIDTH, TAB_HEIGHT)
                    if tab_rect.collidepoint(mouse_pos):
                        current_shop_category_index = i
                        shop_scroll_offset = 0  # Reset scroll offset
                        filter_shop_items() #filter shop items

                # --- Scroll Button Clicks (Shop) ---
                if SHOP_SCROLL_UP_BUTTON_RECT.collidepoint(mouse_pos):
                    shop_scroll_offset = max(0, shop_scroll_offset - 1)
                    

                elif SHOP_SCROLL_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                    # Calculate max_scroll_offset based on current_shop_items
                    max_scroll_offset = max(0, len(current_shop_items) - 4)
                    shop_scroll_offset = min(max_scroll_offset, shop_scroll_offset + 1)
                    


                # --- Item Slot Clicks (Shop - SELECT ONLY) ---
                for i in range(4):
                    slot_rect = pygame.Rect(
                        ITEM_SLOTS_START_X,
                        ITEM_SLOTS_START_Y + i * (ITEM_SLOT_HEIGHT + ITEM_SLOT_SPACING_Y),
                        ITEM_SLOT_WIDTH,
                        ITEM_SLOT_HEIGHT
                    )
                    if slot_rect.collidepoint(mouse_pos):
                        if i + shop_scroll_offset < len(current_shop_items):
                            selected_shop_item = current_shop_items[i + shop_scroll_offset]
                            print(f"Selected shop item: {selected_shop_item}")
                            break  # Exit after selecting

                # --- Inventory Slot Clicks (SELECT ONLY) ---
                for row in range(INVENTORY_ROWS):
                    for col in range(INVENTORY_SLOTS_PER_ROW):
                        index = row * INVENTORY_SLOTS_PER_ROW + col + inventory_scroll_offset
                        slot_x = INVENTORY_START_X + col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_SPACING)
                        slot_y = INVENTORY_START_Y + row * (INVENTORY_SLOT_HEIGHT + INVENTORY_SLOT_SPACING)
                        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_DISPLAY_WIDTH - 60, INVENTORY_SLOT_HEIGHT)

                        if slot_rect.collidepoint(mouse_pos):
                            if index < len(current_inventory_items):
                                selected_inventory_item = current_inventory_items[index]
                                print(f"Selected inventory item: {selected_inventory_item}")
                                break  # Exit the inner loop
                    else:
                        continue
                    break

                 # --- Inventory Tab Clicks ---
                handle_inventory_tab_clicks(mouse_pos)

                # --- Inventory Scroll Button Clicks (CORRECTED) ---
                if INVENTORY_SCROLL_UP_BUTTON_RECT.collidepoint(mouse_pos):
                    inventory_scroll_offset = max(0, inventory_scroll_offset - INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category()  # UPDATE DISPLAYED ITEMS
                elif INVENTORY_SCROLL_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                    max_scroll_offset = max(0, len(current_inventory_items) - (INVENTORY_ROWS * INVENTORY_SLOTS_PER_ROW))
                    inventory_scroll_offset = min(max_scroll_offset, inventory_scroll_offset + INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category()  # UPDATE DISPLAYED ITEMS

                # --- Buy Button Click (BUTTON1_RECT) ---
                if BUTTON1_RECT.collidepoint(mouse_pos):
                    if selected_shop_item:  # Only buy if an item is selected
                        item_data = shop_items_data[selected_shop_item]
                        if player.coins >= item_data["price"]:
                            if len(player.inventory) < INVENTORY_CAPACITY:
                                player.coins -= item_data["price"]
                                player.inventory.append(selected_shop_item)
                                add_combat_message(f"Bought {item_data['name']} for {item_data['price']} gold.")
                                selected_shop_item = None  # Clear selection
                                inventory_scroll_offset = 0 # Reset scroll
                                filter_inventory_by_category() #update the inventory
                            else:
                                add_combat_message("Inventory is full!")
                        else:
                            add_combat_message("Not enough gold!")

                # --- Sell Button Click (BUTTON2_RECT) ---
                if BUTTON2_RECT.collidepoint(mouse_pos):
                    if selected_inventory_item:
                        if player.sell_item(selected_inventory_item):  # Call sell_item()
                            selected_inventory_item = None  # Clear selection
                            inventory_scroll_offset = 0
                            filter_inventory_by_category() #update filtered list

                # --- Equip/Exit Button Clicks ---
                if EQUIPMENT_BUTTON_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = EQUIPMENT_MENU
                    previous_state = SHOP

                if BUTTON4_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = TOWN

def calculate_total_equipment_bonuses(player):
    """Calculates the total stat bonuses from all equipped items."""
    total_bonuses = {
        "attack": [0, 0],  # Store as [min_bonus, max_bonus] for attack range
        "defense": 0,
        "health": 0,
        "mana": 0,
        "accuracy": 0,
        "evasion": 0,
        # Add other stats as needed
    }

    for slot, item_id in player.equipment.items():
        if item_id:  # Check if an item is equipped in the slot
            item_data = shop_items_data[item_id]
            if "stats_bonus" in item_data:
                for stat, bonus in item_data["stats_bonus"].items():
                    if stat in total_bonuses:
                        if stat == "attack":
                            total_bonuses[stat][0] += bonus[0]  # Add to min attack
                            total_bonuses[stat][1] += bonus[1]  # Add to max attack
                        elif stat == "health":
                            total_bonuses[stat] += bonus
                        elif stat == "mana":
                            total_bonuses[stat] += bonus
                        else:
                            total_bonuses[stat] += bonus # Add bonuses together
                    else:
                        print(f"Warning: Unknown stat bonus '{stat}' in item {item_id}")

    return total_bonuses
def draw_equipment_menu():
    pygame.draw.rect(screen, (180, 180, 180), EQUIPMENT_MENU_RECT)  # Background
    pygame.draw.rect(screen, BLACK, EQUIPMENT_MENU_RECT, 2)  # Border

    for slot_name, slot_rect in EQUIPMENT_SLOT_RECTS.items():
        pygame.draw.rect(screen, (150, 150, 150), slot_rect)  # Slot background
        pygame.draw.rect(screen, BLACK, slot_rect, 1)  # Slot border
        equipped_item_id = player.equipment[slot_name]
        if equipped_item_id:
            # --- Draw Equipped Item Image and Name ---
            if equipped_item_id in shop_items_data:
               item_data = shop_items_data[equipped_item_id]
               item_image = item_data.get("image")
               if item_image:
                  scaled_image = pygame.transform.scale(item_image,(EQUIPMENT_SLOT_SIZE,EQUIPMENT_SLOT_SIZE ))
                  screen.blit(scaled_image, (slot_rect.x,slot_rect.y))
            else:
                print(f"ERROR: Item {equipped_item_id} not in shop.") #error checking
        else:
            # --- Draw Slot Name (if empty) ---
            slot_name_surface = SMALL_FONT.render(slot_name.replace("_", " ").title(), True, BLACK)  # Nicer formatting
            slot_name_rect = slot_name_surface.get_rect(center=slot_rect.center)
            screen.blit(slot_name_surface, slot_name_rect)

    # --- Calculate Total Bonuses ---
    total_bonuses = calculate_total_equipment_bonuses(player)

    # --- Display Total Bonuses (Organized in Rows) ---
    bonus_text_x_start = EQUIPMENT_SLOT_START_X
    bonus_text_y_start = EQUIPMENT_SLOT_RECTS["ring2"].bottom + 20  # Start below ring2
    line_spacing = 25

    # --- Background for Bonus Text (Stretching across) ---
    bonus_bg_rect = pygame.Rect(
        EQUIPMENT_MENU_X + 10,
        bonus_text_y_start - 10,
        EQUIPMENT_MENU_WIDTH - 20,
        line_spacing * 3 + 10  # Height for 3 rows + padding
    )
    pygame.draw.rect(screen, (150, 150, 150), bonus_bg_rect)
    pygame.draw.rect(screen, BLACK, bonus_bg_rect, 1)


    # Row 1: HP and Mana
    draw_outlined_text(screen, f"Bonus HP: +{total_bonuses.get('health', 0)}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start, bonus_text_y_start))
    draw_outlined_text(screen, f"Bonus Mana: +{total_bonuses.get('mana', 0)}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start + 150, bonus_text_y_start)) #x start + for next column

    # Row 2: Attack and Defense
    bonus_text_y_start += line_spacing
    attack_bonus = total_bonuses.get('attack', [0, 0])
    draw_outlined_text(screen, f"Attack: +{attack_bonus[0]}-{attack_bonus[1]}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start, bonus_text_y_start))
    draw_outlined_text(screen, f"Defense: +{total_bonuses.get('defense', 0)}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start + 150, bonus_text_y_start))#x start + for next column

    # Row 3: Accuracy and Evasion
    bonus_text_y_start += line_spacing
    draw_outlined_text(screen, f"Accuracy: +{total_bonuses.get('accuracy', 0)}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start, bonus_text_y_start))
    draw_outlined_text(screen, f"Evasion: +{total_bonuses.get('evasion', 0)}", SMALL_FONT, BLACK, WHITE, (bonus_text_x_start + 150, bonus_text_y_start))#x start + for next column
    render_status_bar()
def handle_inventory_tab_clicks(mouse_pos):
    global current_inventory_category_index, inventory_scroll_offset
    for i in range(len(INVENTORY_CATEGORIES)):
        tab_rect = pygame.Rect(INVENTORY_TAB_START_X + i * INVENTORY_TAB_WIDTH, INVENTORY_TAB_Y, INVENTORY_TAB_WIDTH, INVENTORY_TAB_HEIGHT)
        if tab_rect.collidepoint(mouse_pos):
            current_inventory_category_index = i
            inventory_scroll_offset = 0  # Reset scroll offset
            filter_inventory_by_category()
            return  # IMPORTANT: Return after handling a tab click
def handle_inventory_in_combat_events(events):
    global CURRENT_STATE, inventory_scroll_offset, current_inventory_category_index, player_turn, current_enemy, previous_state
    mouse_pos = pygame.mouse.get_pos()
    filter_inventory_by_category()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click

                # --- Inventory Slot Clicks (Use Item) ---
                for row in range(INVENTORY_ROWS):
                    for col in range(INVENTORY_SLOTS_PER_ROW):
                        index = row * INVENTORY_SLOTS_PER_ROW + col + inventory_scroll_offset
                        slot_x = INVENTORY_START_X + col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_SPACING)
                        slot_y = INVENTORY_START_Y + row * (INVENTORY_SLOT_HEIGHT + INVENTORY_SLOT_SPACING)
                        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_DISPLAY_WIDTH - 60, INVENTORY_SLOT_HEIGHT)

                        if slot_rect.collidepoint(mouse_pos):
                            if index < len(current_inventory_items):
                                item_id = current_inventory_items[index]
                                item_data = shop_items_data[item_id]

                                # --- Use the item ONLY if it's a consumable ---
                                if item_data["category"] in ("Potions", "Scrolls"):
                                    success = player.use_item(item_id, target=current_enemy)  # Pass enemy as target
                                    if success:
                                        player_turn = False #using an item ends turn
                                        if current_enemy.is_alive(): #check if alive
                                            handle_monster_turn(player,current_enemy) #monster turn
                                            player_turn = True #set up next player turn
                                        inventory_scroll_offset = 0 #reset the scroll
                                        filter_inventory_by_category() #update filtered items
                                        CURRENT_STATE = COMBAT  # Return to combat after using item


                # --- Inventory Scroll Button Clicks --- (Same as before) ---
                if INVENTORY_SCROLL_UP_BUTTON_RECT.collidepoint(mouse_pos):
                    inventory_scroll_offset = max(0, inventory_scroll_offset - INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category()
                elif INVENTORY_SCROLL_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                    max_scroll_offset = max(0, len(current_inventory_items) - (INVENTORY_ROWS * INVENTORY_SLOTS_PER_ROW))
                    inventory_scroll_offset = min(max_scroll_offset, inventory_scroll_offset + INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category()

                 # --- Inventory Tab Clicks ---
                for i in range(len(INVENTORY_CATEGORIES)):
                    tab_rect = pygame.Rect(INVENTORY_TAB_START_X + i * INVENTORY_TAB_WIDTH, INVENTORY_TAB_Y, INVENTORY_TAB_WIDTH, INVENTORY_TAB_HEIGHT)
                    if tab_rect.collidepoint(mouse_pos):
                        current_inventory_category_index = i
                        inventory_scroll_offset = 0  # Reset scroll offset
                        filter_inventory_by_category()
                # --- Exit logic using BUTTON_RECT ---
                if BUTTON3_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = previous_state
                    inventory_scroll_offset = 0
                    current_inventory_category_index = 0
# --- Event Handling Function (Placeholder - Needs Integration with Inventory) ---
def handle_equipment_events(events):
    global CURRENT_STATE, previous_state, inventory_scroll_offset, selected_slot, current_inventory_category_index
    mouse_pos = pygame.mouse.get_pos()
    filter_inventory_by_category() #filter each refresh
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left-click

                # --- Equipment Slot Clicks ---
                for slot_name, slot_rect in EQUIPMENT_SLOT_RECTS.items():
                    if slot_rect.collidepoint(mouse_pos):
                        print(f"Clicked on equipment slot: {slot_name}")
                        equipped_item_id = player.equipment[slot_name]

                        if equipped_item_id:
                            # Unequip item
                            player.remove_equipment_bonuses(equipped_item_id)  # <--- REMOVE BONUSES
                            player.equipment[slot_name] = None
                            player.inventory.append(equipped_item_id)
                            add_combat_message(f"Unequipped {shop_items_data[equipped_item_id]['name']} from {slot_name}")
                            inventory_scroll_offset = 0 # Reset scroll
                        else:
                            selected_slot = slot_name # Select the slot for equipping
                            print(f"Selected slot: {selected_slot}")

                # --- Inventory Slot Clicks (Equip to Selected Slot) ---
                #Adjusted for the new inventory layout
                for row in range(INVENTORY_ROWS):
                    for col in range(INVENTORY_SLOTS_PER_ROW):
                        index = row * INVENTORY_SLOTS_PER_ROW + col + inventory_scroll_offset
                        slot_x = INVENTORY_START_X + col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_SPACING)
                        slot_y = INVENTORY_START_Y + row * (INVENTORY_SLOT_HEIGHT+ INVENTORY_SLOT_SPACING)
                        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_DISPLAY_WIDTH - 60, INVENTORY_SLOT_HEIGHT) #use updated width

                        if slot_rect.collidepoint(mouse_pos):
                            if index < len(current_inventory_items): #use filtered items
                                item_id = current_inventory_items[index]
                                # --- Check if item can be equipped to selected_slot ---
                                if selected_slot:
                                    item_data = shop_items_data[item_id]
                                    if item_data["equip_slot"] == selected_slot:
                                        # --- Equip the item ---
                                        if player.equipment[selected_slot] is not None:  # Check for existing item
                                            player.remove_equipment_bonuses(player.equipment[selected_slot]) # Remove old bonuses
                                            player.inventory.append(player.equipment[selected_slot])  # Move old item to inventory
                                        player.equipment[selected_slot] = item_id
                                        player.apply_equipment_bonuses(item_id)  # <--- APPLY BONUSES
                                        player.inventory.remove(item_id)  # Use .remove() for item ID
                                        add_combat_message(f"Equipped {item_data['name']} to {selected_slot}")
                                        inventory_scroll_offset = 0 #reset scroll
                                        filter_inventory_by_category() #update current items
                                        selected_slot = None  # Clear selected slot after equipping
                                    else:
                                        print("wrong slot.")
                                        selected_slot = None  # Clear on incorrect slot
                                        add_combat_message("You cannot equip that item there.")

                # --- Inventory Scroll Button Clicks ---
                if INVENTORY_SCROLL_UP_BUTTON_RECT.collidepoint(mouse_pos):
                    inventory_scroll_offset = max(0, inventory_scroll_offset - INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category() #update items shown
                elif INVENTORY_SCROLL_DOWN_BUTTON_RECT.collidepoint(mouse_pos):
                    max_scroll_offset = max(0, len(current_inventory_items) - (INVENTORY_ROWS * INVENTORY_SLOTS_PER_ROW ))
                    inventory_scroll_offset = min(max_scroll_offset, inventory_scroll_offset + INVENTORY_SLOTS_PER_ROW)
                    filter_inventory_by_category() #update items shown

                 # --- Inventory Tab Clicks ---
                for i in range(len(INVENTORY_CATEGORIES)):
                    tab_rect = pygame.Rect(INVENTORY_TAB_START_X + i * INVENTORY_TAB_WIDTH, INVENTORY_TAB_Y, INVENTORY_TAB_WIDTH, INVENTORY_TAB_HEIGHT)
                    if tab_rect.collidepoint(mouse_pos):
                        current_inventory_category_index = i
                        inventory_scroll_offset = 0  # Reset scroll offset
                        filter_inventory_by_category() #update the current items

                # --- ADDED: Exit logic using BUTTON4_RECT ---
                if BUTTON4_RECT.collidepoint(mouse_pos):  # <--- COLON ADDED HERE
                    CURRENT_STATE = previous_state
                    inventory_scroll_offset = 0 #reset scroll
                    current_inventory_category_index = 0 #reset category
                    
def handle_dungeon():
    global current_room_id
    screen.fill((50, 50, 50))
    room_name = rooms[current_room_id]["name"]
    room_text = SMALL_FONT.render(f"You are in the {room_name}.", True, (255, 255, 255))
    screen.blit(room_text, (10, 10))
    room_data = rooms[current_room_id]
    if room_data["content"] == "staircase_down":
        staircase_text = SMALL_FONT.render("You have found a staircase leading deeper!", True, YELLOW)
        screen.blit(staircase_text, (10, 40))
    elif room_data["monster"]:
        monster = room_data["monster"]
        content_text = SMALL_FONT.render(f"A {monster.get_name()} is here.", True, WHITE)
        screen.blit(content_text, (10, 40))
    elif room_data["type"] == 2: #chest
        content_text = SMALL_FONT.render("A chest is here.", True, WHITE)
        screen.blit(content_text, (10, 40))
    else:
        content_text = SMALL_FONT.render("An empty room.", True, WHITE)
        screen.blit(content_text, (10, 40))
    # --- ROOM DESCRIPTION TEXT (Positioned above status bar - adjust y as needed) ---
    room_description = rooms[current_room_id]["description"]
    description_text_surface = SMALL_FONT.render(room_description, True, (200, 200, 200))
    screen.blit(description_text_surface, (10, 120)) #  <---- Adjust y-coordinate (120 is a starting point)
    render_status_bar() # Status bar rendering (assumed to be at the bottom)
def handle_dungeon_events(events):
    global current_room_id, CURRENT_STATE,roomlvl,rooms

    mouse_pos = pygame.mouse.get_pos()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # --- NEW: Check for equipment button in dungeon---
                if EQUIPMENT_BUTTON_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = EQUIPMENT_MENU
                    global previous_state
                    previous_state = DUNGEON
                elif BUTTON1_RECT.collidepoint(mouse_pos):
                    print("button1 button clicked in Dungeon")
                elif BUTTON2_RECT.collidepoint(mouse_pos):
                    print("Button2 button clicked in Dungeon")
                elif BUTTON3_RECT.collidepoint(mouse_pos):
                    print("Deeper button clicked")
                    current_room = rooms[current_room_id]
                    if current_room["content"] == "staircase_down":
                        descend_staircase()
                    else:
                        move()
                elif BUTTON4_RECT.collidepoint(mouse_pos):
                    roomlvl = 0  # Reset to starting dungeon level (usually 0 or 1)
                    rooms = create_room_dictionary(roomlvl) 
                    current_room_id = "room1" # Set player to start at the first room of the new dungeon
                    print("Dungeon regenerated.")
                    CURRENT_STATE = TOWN
def handle_combat():
    global player_turn, current_enemy, CURRENT_STATE
    screen.fill((0, 0, 0))
    if current_enemy:
        monster_image = monster_data.get(current_enemy.get_name(), {}).get("image") # Safely get image from monster_data
        if monster_image: # Check if image was loaded successfully
            image_x = SCREEN_WIDTH // 2 - monster_image.get_width() // 2
            image_y = SCREEN_HEIGHT//2-monster_image.get_height()//2
            screen.blit(monster_image, (image_x, image_y))
        render_monster_status_bar()
        render_combat_log()
        render_status_bar()
def handle_monster_turn(player, current_enemy):
    if current_enemy.is_stunned():
        message_text=(f"{current_enemy.get_name()} is stunned and cannot act.") # Keep stun message
        add_combat_message(message_text)
        current_enemy.update_buff_durations()
    else:
        current_enemy.update_buff_durations()
        chosen_ability = current_enemy.choose_ability(player)
        if chosen_ability:
            current_enemy.use_ability(chosen_ability, player)
        else:
            current_enemy.attack(player) 
    if player.current_health <= 0:
        return False
    else:
        return True
def handle_player_turn(player, current_enemy, action):
    global CURRENT_STATE, player_turn, ability_menu_open, combat_log_messages, turn_counter,rooms,current_room_id

    message_text = (f"----------------------------------- ")
    add_combat_message(message_text)
    player.start_turn() # Start player turn actions (buff updates, etc.)
    if action == "attack": # <--- HANDLE "attack" ACTION
        damage = player.attack(current_enemy) # Perform attack
        player_turn = False # End player turn
        player.end_turn() # End of player turn actions (buff expiry etc.)
        if current_enemy.is_alive():
            player_alive = handle_monster_turn(player, current_enemy) # Monster turn
            if not player_alive:
                CURRENT_STATE = GAME_OVER
        player_turn = True # Prepare for next player turn


    elif action == "abilities": # <--- HANDLE "abilities" ACTION
        ability_menu_open = not ability_menu_open # Toggle ability menu


    elif action == "run": # <--- HANDLE "run" ACTION
        if random.random() < 0.4:
            message_text=("Player successfully ran away!")
            add_combat_message(message_text)
          # --- 2. Regenerate Dungeon ---
            roomlvl = 0  # Reset to starting dungeon level (usually 0 or 1)
            rooms = create_room_dictionary(roomlvl) 
            current_room_id = "room1" # Set player to start at the first room of the new dungeon
            print("Dungeon regenerated.")
            CURRENT_STATE = TOWN # Go to town
        else:
            message_text=("Run failed! Monster attacks.")
            add_combat_message(message_text)
            player_turn = False # End player turn
            player.end_turn() # End of player turn actions
            if current_enemy.is_alive():
                player_alive = handle_monster_turn(player, current_enemy) # Monster turn
                if not player_alive:
                    CURRENT_STATE = GAME_OVER
            player_turn = True # Prepare for next player turn


    elif action == "ability_menu_click": # <--- HANDLE "ability_menu_click" ACTION (when ability is chosen from menu)
        ability_menu_open = False # Close ability menu # Assuming ability is already used in handle_combat_events in this case - adjust if needed!
        player_turn = False
        player.end_turn()
        if current_enemy.is_alive():
            player_alive = handle_monster_turn(player, current_enemy)
            if not player_alive:
                CURRENT_STATE = GAME_OVER
        player_turn = True
    return True # Default return - adjust as needed   
def handle_combat_events(events):
    global CURRENT_STATE, player_turn, current_enemy, combat_log_messages, ability_menu_open, roomlvl, player, turn_counter
    mouse_pos = pygame.mouse.get_pos()
    turn_counter = 1
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # --- Check Button Clicks ---
                if BUTTON1_RECT.collidepoint(mouse_pos):  # Attack Button
                    if player_turn and not ability_menu_open:
                        handle_player_turn(player, current_enemy, "attack")

                elif BUTTON2_RECT.collidepoint(mouse_pos):  # Abilities Button
                    if player_turn:
                        handle_player_turn(player, current_enemy, "abilities")

                elif BUTTON3_RECT.collidepoint(mouse_pos):  # Items Button (NEW)
                    if player_turn and not ability_menu_open:
                        CURRENT_STATE = INVENTORY_IN_COMBAT
                        global previous_state  # Store previous state
                        previous_state = COMBAT

                elif BUTTON4_RECT.collidepoint(mouse_pos):  # Run Button
                    if player_turn and not ability_menu_open:
                        handle_player_turn(player, current_enemy, "run")

                # --- Ability Menu Click Handling (if menu is open) ---
                if ability_menu_open:
                    # ... (existing ability menu handling code - NO CHANGES HERE) ...
                    menu_width = 400
                    menu_height = 300
                    menu_x = (SCREEN_WIDTH - menu_width) // 2
                    menu_y = (SCREEN_HEIGHT - menu_height) // 2
                    exit_button_width = 60
                    exit_button_x = menu_x + menu_width - exit_button_width - 10
                    exit_button_rect = pygame.Rect(exit_button_x, menu_y + 10, exit_button_width, 25)
                    if exit_button_rect.collidepoint(mouse_pos):
                        ability_menu_open = False
                    else:  # Ability Button Clicks
                        ability_button_y_start = menu_y + 50
                        ability_button_spacing = 70
                        ability_button_width = menu_width - 40
                        ability_button_height = 60

                        player_class_name = player.class_name
                        if player_class_name in CLASS_ABILITIES:
                            abilities = CLASS_ABILITIES[player_class_name]
                            for i in range(min(4,len(abilities))):  # Iterate through available abilities
                                ability_button_rect = pygame.Rect(menu_x+20, ability_button_y_start + i * ability_button_spacing, ability_button_width, ability_button_height)
                                if ability_button_rect.collidepoint(mouse_pos):
                                        ability = abilities[i]
                                        player.use_ability(ability, current_enemy)  # Use the ability
                                        handle_player_turn(player, current_enemy, "ability_menu_click") #handles player turn
    if current_enemy and not current_enemy.is_alive():
        player.gain_experience(current_enemy.get_experience())
        player.gain_coins(current_enemy.gold)
        message_text = (f"You gained {current_enemy.get_experience()} XP and {current_enemy.gold} coins.")
        add_combat_message(message_text)
        CURRENT_STATE = DUNGEON
        current_enemy = None
        rooms[current_room_id]['monster'] = None

STATE_HANDLERS = {
    TOWN: handle_town_events,
    DUNGEON: handle_dungeon_events,
    MENU: handle_menu_events,
    CHARACTER_CREATION: handle_character_creation_events,
    COMBAT: handle_combat_events,
    SHOP: handle_shop_events,
    TAVERN: handle_tavern_events,
    GAME_OVER:handle_game_over_events,
    EQUIPMENT_MENU: handle_equipment_events,
    INVENTORY_IN_COMBAT:handle_inventory_in_combat_events,
}
# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    events = pygame.event.get()  # Get the LIST of events (plural)
    for event in events: # Handle global events (like QUIT)
        if event.type == pygame.QUIT:
            running = False
    # --- Call State Handler with the ENTIRE 'events' LIST ---
    if CURRENT_STATE in STATE_HANDLERS:
        STATE_HANDLERS[CURRENT_STATE](events) # <---- Line 2312 (Error Point)
    # --- Game Logic and Rendering ---
    if CURRENT_STATE == MENU:
        handle_menu()
    elif CURRENT_STATE == CHARACTER_CREATION:
        handle_character_creation()
    elif CURRENT_STATE == TOWN:
        handle_town()
    elif CURRENT_STATE == DUNGEON:
        handle_dungeon()
    elif CURRENT_STATE == GAME_OVER:
        handle_game_over()
    elif CURRENT_STATE == COMBAT:
        handle_combat()
    elif CURRENT_STATE == TAVERN:
        handle_tavern()
    elif CURRENT_STATE == SHOP:
        handle_shop()
    elif CURRENT_STATE == INVENTORY_IN_COMBAT:
        draw_inventory()
    elif CURRENT_STATE == EQUIPMENT_MENU:
        draw_equipment_menu()
        draw_inventory()  # Draw the inventory!
    pygame.display.flip()
pygame.quit()