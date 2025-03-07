import pygame
import random
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
# --- Screen Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
town_bg_image=pygame.image.load("PythonGaming V3/PYTHON Gaming/Images/town.png").convert()
tavern_bg_image=pygame.image.load("PythonGaming V3/PYTHON Gaming/Images/tavern.png").convert()
# --- Fonts ---
TITLE_FONT = pygame.font.Font("freesansbold.ttf", 64)
BUTTON_FONT = pygame.font.Font("freesansbold.ttf", 20)
CHARACTER_FONT = pygame.font.Font("freesansbold.ttf", 20)
STATUS_FONT = pygame.font.Font(None, 24)
SMALL_FONT = pygame.font.Font(None, 20)
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
player_room_count=0
roomlvl = 0  # Starting room level (level 0 is the first floor)
rooms_explored_this_floor = 0 # Counter for rooms explored on the current floor
rooms={}
# --- Combat State Variables ---
player_turn = True
current_enemy = None
combat_log_messages = []
ability_menu_open = False
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
#Shop UI
SHOP_MENU_COLOR = (100, 90, 130)
TAB_COLOR = (120, 110, 150)
SLOT_COLOR = (80, 70, 100)
BUTTON_COLOR = (120, 120, 120)
SHOP_MENU_RECT = pygame.Rect(50, 50, 350, 400)
TAB_WIDTH = 75
TAB_HEIGHT = 25
TAB_START_X = SHOP_MENU_RECT.x + 20
TAB_Y = SHOP_MENU_RECT.y - TAB_HEIGHT
ITEM_SLOT_WIDTH = SHOP_MENU_RECT.width - 60 # <--- Wider: almost full width of shop menu, with some padding
ITEM_SLOT_HEIGHT = 80 # <--- Adjust vertical height as needed (smaller than before maybe)
ITEM_SLOTS_START_X = SHOP_MENU_RECT.x + 30 # <--- Start from left edge of shop menu, with some padding
ITEM_SLOTS_START_Y = SHOP_MENU_RECT.y + 20 # <--- Starting Y inside shop menu
ITEM_SLOT_SPACING_Y = 10 # <--- VERTICAL spacing between item slots (rename from X to Y)
SCROLL_BUTTON_WIDTH = 80
SCROLL_BUTTON_HEIGHT = 30
SCROLL_UP_BUTTON_RECT = pygame.Rect(SHOP_MENU_RECT.centerx - SCROLL_BUTTON_WIDTH - 10, SHOP_MENU_RECT.bottom - SCROLL_BUTTON_HEIGHT + 40, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
SCROLL_DOWN_BUTTON_RECT = pygame.Rect(SHOP_MENU_RECT.centerx + 10, SHOP_MENU_RECT.bottom - SCROLL_BUTTON_HEIGHT + 40, SCROLL_BUTTON_WIDTH, SCROLL_BUTTON_HEIGHT)
#Shop data
SHOP_CATEGORIES = ["Armor", "Weapons", "Potions", "Scrolls", "Misc."] # Global SHOP_CATEGORIES
current_shop_category_index = 0
SELECTED_TAB_COLOR = (150, 140, 180) 
current_shop_items = []
#--- Inventory UI
INVENTORY_BOX_COLOR = (90, 80, 110) # Example inventory box color
INVENTORY_BOX_WIDTH = 375 # Example width of inventory box
INVENTORY_BOX_HEIGHT = SHOP_MENU_RECT.height # Let's make it the same height as the shop menu
INVENTORY_BOX_X = SHOP_MENU_RECT.right + 10 # Position it to the right of the shop menu, with a 20 pixel gap
INVENTORY_BOX_Y = SHOP_MENU_RECT.y # Align it vertically with the top of the shop menu
INVENTORY_BOX_RECT = pygame.Rect(INVENTORY_BOX_X, INVENTORY_BOX_Y, INVENTORY_BOX_WIDTH, INVENTORY_BOX_HEIGHT) # Define the Rect
SELECTED_INVENTORY_TAB_COLOR=(150,140,100)
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
TOWN_BUTTON_TEXTS = ["Tavern", "Shop", "Dungeon", "Menu"]
DUNGEON_BUTTON_TEXTS = ["Attack", "Abilities", "Deeper", "Town"]
COMBAT_BUTTON_TEXTS = ["Attack","Abilities","Items","Run"]
SHOP_BUTTON_TEXTS = ["Buy","Sell","Examine","Leave"]
INVENTORY_IN_COMBAT_TEXTS = ["Use","Examine","Drop","Close",]
TAVERN_BUTTON_TEXTS = ["Rest","Quest","Gamble","Leave"]
BUTTON_TEXTS = {
    TOWN: TOWN_BUTTON_TEXTS,
    DUNGEON: DUNGEON_BUTTON_TEXTS,
    COMBAT: COMBAT_BUTTON_TEXTS,
    SHOP: SHOP_BUTTON_TEXTS,
    TAVERN: TAVERN_BUTTON_TEXTS
}
#Tavern Rest UI
SHOW_REST_OPTIONS_BOX = False
REST_OPTION_BUTTON_RECTS = {
    "rough_couch": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 40), # Example positions, adjust
    "cozy_bed": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 300, 40),
    "luxurious_suite": pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 70, 300, 40),
}
TAVERN_REST_EXIT_BUTTON_RECT = None 
# --- Player Class ---
class Player:
    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name
        self.stats = CLASS_STATS[class_name].copy() # Use .copy() to avoid modifying the original CLASS_STATS
        self.stats["attack"] = list(CLASS_STATS[class_name]["attack"])
        self.current_health = self.stats['health']
        self.current_mana = self.stats['mana']
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.buffs = [] # List to hold buffs
        self.coins = 0
        self.max_experience = self._calculate_max_experience()
    def get_attack_damage(self): # Renamed to get_attack_damage for clarity
        """Calculates attack damage (including buffs)."""
        base_attack_range = self.stats['attack'] # Get attack range (list/tuple)
        min_damage = base_attack_range[0] # Minimum damage from range
        max_damage = base_attack_range[1] # Maximum damage from range
        buffed_attack = 0 # Initialize flat buffed_attack (sum of flat buffs)
        percentage_buff_multiplier = 1.0 # Initialize percentage buff multiplier
        for buff in self.buffs: # Iterate through self.buffs (correct list name)
            if buff['stat'] == 'attack_buff': # Check for 'attack_buff' stat (correct key and stat name)
                if buff.get('is_percentage_buff'): # Check for percentage buff (existing logic)
                    percentage_buff_multiplier += buff['amount'] # Apply percentage buffs
                else: # Flat buff (existing logic)
                    buffed_attack += buff['amount'] # Sum flat attack buffs
        min_damage = round(min_damage * percentage_buff_multiplier)
        max_damage = round(max_damage * percentage_buff_multiplier)
        random_damage = random.randint(min_damage, max_damage) 
        return round(random_damage + buffed_attack) 
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
    def take_damage(self, damage):
        actual_damage = max(0, damage)
        if actual_damage > 0: 
            self.current_health -= actual_damage
            combat_log_messages.append(f"{self.name} takes {actual_damage} damage!") 
            return actual_damage
        else:
            combat_log_messages.append(f"{self.name} took no damage!") 
            return 0
    def attack(self, enemy):
        attacker_accuracy = self.get_accuracy()
        enemy_evasion = enemy.get_evasion()
        hit_chance_percentage = max(5, min(95, self.get_accuracy() - enemy.get_evasion())) # DIRECT PERCENTAGE SUBTRACTION, calling get_accuracy and get_evasion which now return percentages
        is_hit = random.random() < (hit_chance_percentage / 100.0)
        # --- DEBUG PRINTS ---
        print(f"--- Attack Debug ---")
        print(f"Attacker: {self.name}, Accuracy: {attacker_accuracy}")
        print(f"Enemy: {enemy.get_name()}, Evasion: {enemy_evasion}")
        print(f"Hit Chance Percentage: {hit_chance_percentage:.2f}%") # Format to 2 decimal places
        print(f"Is Hit Roll (Random < {hit_chance_percentage/100.0:.2f}): {'HIT' if is_hit else 'MISS'}")
        print(f"--- End Attack Debug ---")
        if is_hit:
            damage = self.get_attack_damage()
            damage_dealt = enemy.take_damage(damage)
            combat_log_messages.append(f"{self.name} attacks {enemy.get_name()} for {damage_dealt} damage!")
            return damage_dealt
        else:
            combat_log_messages.append(f"{self.name} attacks {enemy.get_name()} and misses!")
            return 0
    def get_evasion(self):
        """Calculates player evasion, returning WHOLE NUMBER PERCENTAGE (0-100)."""
        base_evasion_percentage = self.stats['evasion'] # Get base evasion as whole number percentage
        buffed_evasion_percentage = base_evasion_percentage # Start with base percentage
        for buff in self.buffs:
            if buff['stat'] == 'evasion_buff':
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['amount']
                    buffed_evasion_percentage += percentage_increase
                else:
                    buffed_evasion_percentage += buff['amount']
        return buffed_evasion_percentage # <--- Return WHOLE NUMBER PERCENTAGE (0-100)
    def get_accuracy(self):
        """Calculates player accuracy, returning WHOLE NUMBER PERCENTAGE (0-100)."""
        accuracy_percentage_whole_number = self.stats['accuracy'] # Get accuracy as whole number percentage from stats
        return accuracy_percentage_whole_number # <--- Return WHOLE NUMBER PERCENTAGE directly
    def is_alive(self):
        """Checks if the player's health is above 0."""
        return self.current_health > 0
    def gain_experience(self, xp):
        """Awards experience points and handles level ups."""
        self.experience += xp
        if self.experience >= self.max_experience: # Use self.max_experience here
            self.level_up()
    def _calculate_max_experience(self): # Private method to calculate max_experience
        """Calculates the experience needed for the next level."""
        return (self.level ** 2) * 100
    def level_up(self):
        """Handles player level up, increasing stats based on class."""
        if self.experience >= self.max_experience:
            self.level += 1
            self.experience -= self.max_experience
            self.max_experience = int(self.max_experience * 1.5) # Increase XP needed for next level
            level_up_stats = CLASS_LEVEL_UP_STATS[self.class_name]
            self.stats["health"] += level_up_stats["health"]
            self.stats["mana"] += level_up_stats["mana"]
            # --- Handle Attack Range Level Up ---
            attack_increase = level_up_stats["attack"] # Get the *increase* value from level up stats
            current_attack_range = self.stats["attack"] # Get current attack range (list)
            current_attack_range[0] += attack_increase # Increase the minimum of the range
            current_attack_range[1] += attack_increase # Increase the maximum of the range
            self.stats["defense"] += level_up_stats["defense"]
            self.stats["accuracy"] += level_up_stats["accuracy"]
            self.stats["evasion"] += level_up_stats["evasion"]
            self.current_health = self.stats["health"] # Full heal on level up
            self.current_mana = self.stats["mana"]     # Full mana on level up
            combat_log_messages.append(f"{self.name} leveled up to Level {self.level}!")
            combat_log_messages.append("Stats increased!")
    def gain_coins(self, gold):
        """Adds gold to the player's inventory (for now just tracks gold)."""
        self.coins += gold
        combat_log_messages.append(f"{self.name} gained {gold} gold.") # Log gold gain
    def use_mana(self, amount):
        """Reduces player's mana by the given amount, returns True if successful, False if not enough mana."""
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        else:
            combat_log_messages.append("Not enough mana!")
            return False
    def apply_buff(self, buff_data):
        buff_name = buff_data['name']
        buff_stat = buff_data['stat']
        buff_duration = buff_data['duration_turns'] if 'duration_turns' in buff_data else 3
        buff_type = buff_data.get('buff_type')
        print(f"Applying buff: Name='{buff_name}', Stat='{buff_stat}', Type='{buff_type}'") # <--- DEBUG PRINT
        if buff_type == "rest":
            print("  Buff type is 'rest'. Checking for existing *different rest option* buffs...") # <--- DEBUG PRINT - Refined message
            rest_buffs_to_remove = []
            current_rest_option_name = buff_name.split(" - ")[1].split(" ")[0] # Extract "Rough Couch", "Cozy Bed", etc.
            for buff in self.buffs:
                if buff.get('buff_type') == "rest":
                    existing_rest_buff_option_name = buff['name'].split(" - ")[1].split(" ")[0] # Extract existing buff's option name
                    if existing_rest_buff_option_name != current_rest_option_name: # <--- REFINED CHECK: DIFFERENT REST OPTION NAME
                        print(f"    Found existing *different rest option* buff: Name='{buff['name']}', Stat='{buff['stat']}'") # <--- DEBUG PRINT
                        rest_buffs_to_remove.append(buff)
            for buff_to_remove in rest_buffs_to_remove:
                print(f"    Removing existing *different rest option* buff: Name='{buff_to_remove['name']}', Stat='{buff_to_remove['stat']}'") # <--- DEBUG PRINT
                self.buffs.remove(buff_to_remove)
                combat_log_messages.append(f"Previous rest buff '{buff_to_remove['name']}' removed.")
        existing_buff_index = -1
        for index, buff in enumerate(self.buffs):
            if buff['name'] == buff_name and buff['stat'] == buff_stat:
                existing_buff_index = index
                break
        if existing_buff_index != -1:
            self.buffs[existing_buff_index]['duration_turns'] = buff_duration
            combat_log_messages.append(f"{buff_name} duration refreshed on {self.name}.")
        else:
            buff = buff_data.copy()
            buff['duration_turns'] = buff_duration
            self.buffs.append(buff)
            combat_log_messages.append(f"{self.name} is buffed with {buff_name}!")
    def update_buff_durations(self):
        buffs_to_remove = []
        for buff in self.buffs:
            buff['duration_turns'] -= 1
            if buff['duration_turns'] <= 0:
                buffs_to_remove.append(buff)
                combat_log_messages.append(f"{buff['name']} buff expired from {self.name}.")
        for buff in buffs_to_remove:
            self.buffs.remove(buff)
    def start_turn(self):
        self.update_buff_durations() # Update buff durations at start of turn
    def end_turn(self):
        """Actions to perform at the end of the player's turn."""
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
        print(f"You added {item_name} to your inventory.")
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
        "health": 15,  # Warriors gain more health per level
        "mana": 3,     # Less mana gain
        "attack": 3,   # Good attack gain
        "defense": 2,  # Moderate defense gain
        "accuracy": 1,
        "evasion": 1
    },
    "Mage": {
        "health": 10,
        "mana": 7,     # Mages gain more mana per level
        "attack": 1,   # Lower attack gain
        "defense": 1,  # Lower defense gain
        "accuracy": 2, # Mages might gain more accuracy
        "evasion": 1
    },
    "Rogue": {
        "health": 12,
        "mana": 5,
        "attack": 2,
        "defense": 1,
        "accuracy": 2, # Rogues could gain more accuracy
        "evasion": 2   # Rogues could gain more evasion
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
def render_status_bar():
    global player
    pygame.draw.rect(screen, GRAY, STATUS_BAR_RECT)
    # --- Health and Mana Bars ---
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 50
    health_bar_y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 10
    health_ratio = player.current_health / player.stats["health"]
    current_health_width = int(health_bar_width * health_ratio)
    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height))
    health_text = SMALL_FONT.render(f"HP: {player.current_health}/{player.stats['health']}", True, WHITE)
    health_text_rect = health_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y + health_bar_height // 2))
    screen.blit(health_text, health_text_rect)
    mana_bar_width = 200
    mana_bar_height = 20
    mana_bar_x = 50
    mana_bar_y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 40
    mana_ratio = player.current_mana / player.stats["mana"]
    current_mana_width = int(mana_bar_width * mana_ratio)
    pygame.draw.rect(screen, BLACK, (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height))
    pygame.draw.rect(screen, BLUE, (mana_bar_x, mana_bar_y, current_mana_width, mana_bar_height))
    mana_text = SMALL_FONT.render(f"MP: {player.current_mana}/{player.stats['mana']}", True, WHITE)
    mana_text_rect = mana_text.get_rect(center=(mana_bar_x + mana_bar_width // 2, mana_bar_y + mana_bar_height // 2))
    screen.blit(mana_text, mana_text_rect)
    # --- Coins ---
    coin_text = SMALL_FONT.render(f"Coins: {player.coins}", True, WHITE)
    screen.blit(coin_text, (50, SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 70))
    # --- Character Stats ---
    stats_x = 260
    stats_y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 10
    stat_font = pygame.font.Font(None, 20)
    line_spacing = 20  # Define line spacing for stats
    name_text = stat_font.render(f"Name: {player.name}", True, WHITE)
    screen.blit(name_text, (stats_x, stats_y))
    class_text = stat_font.render(f"Class: {player.class_name}", True, WHITE)
    screen.blit(class_text, (stats_x, stats_y + line_spacing))
    level_text = stat_font.render(f"Level: {player.level}", True, WHITE)
    screen.blit(level_text, (stats_x, stats_y + 2 * line_spacing))
    # --- Attack and Defense Section ---
    attack_defense_stats_x = 360
    attack_defense_stats_y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT + 10
    attack_range = player.stats['attack'] # Get the base attack range from player.stats
    min_attack_value = attack_range[0] # Get the minimum base attack value
    max_attack_value = attack_range[1] # Get the maximum base attack value
    buffed_min_attack = min_attack_value # Initialize with base values
    buffed_max_attack = max_attack_value # Initialize with base values
    percentage_attack_buff_multiplier = 1.0 # For percentage-based buffs
    for buff in player.buffs: # Iterate through buffs to apply attack boosts
        if buff['stat'] == 'attack_buff': # Check for attack buffs
            if buff.get('is_percentage_buff'):
                percentage_attack_buff_multiplier += buff['amount'] # Apply percentage buffs
            else: # Flat buff (though we are mainly using percentage buffs from rest)
                buffed_min_attack += buff['amount']
                buffed_max_attack += buff['amount'] # Apply flat buff to BOTH min and max

    # Apply percentage multiplier to BOTH min and max attack values
    buffed_min_attack = int(buffed_min_attack * percentage_attack_buff_multiplier)
    buffed_max_attack = int(buffed_max_attack * percentage_attack_buff_multiplier)

    attack_range_string = f"Attack: {buffed_min_attack}-{buffed_max_attack}" # <--- FORMAT RANGE STRING "Min-Max" with BUFFED values
    attack_stat_text = stat_font.render(attack_range_string, True, WHITE) # Render the range string
    screen.blit(attack_stat_text, (attack_defense_stats_x, attack_defense_stats_y))
    attack_defense_stats_y += line_spacing
    defense_value = player.get_defense()
    defense_text = stat_font.render(f"Defense: {defense_value}", True, WHITE)
    screen.blit(defense_text, (attack_defense_stats_x, attack_defense_stats_y))
    attack_defense_stats_y += line_spacing
    # --- DODGE CHANCE ---
    dodge_chance = player.get_evasion()  # Get evasion value
    dodge_text = stat_font.render(f"Dodge: {dodge_chance}%", True, WHITE) # Render Dodge Chance Text
    screen.blit(dodge_text, (attack_defense_stats_x, attack_defense_stats_y)) # Position after Defense
    attack_defense_stats_y += line_spacing # Increment again if you plan to add more stats below Dodge

    # --- Buffs Display Section ---
    buff_display_x = 540  # Starting X position for buffs (adjust as needed)
    buff_display_y = SCREEN_HEIGHT - STATUS_BAR_HEIGHT - 100 # Start Y position (same as other stats)
    buff_title_text = stat_font.render("Buffs:", True, BLACK) # Title for the buff section
    screen.blit(buff_title_text, (buff_display_x, buff_display_y)) # Blit the title
    buff_display_y += line_spacing # Move Y position down for the first buff

    for buff in player.buffs: # Iterate through the player's active buffs
        buff_text = stat_font.render(f"- {buff['name']} ({buff['duration_turns']} turns)", True, WHITE) # Format buff text
        screen.blit(buff_text, (buff_display_x, buff_display_y)) # Blit the buff text
        buff_display_y += line_spacing # Move Y position down for the next buff
    # --- XP Bar ---  <--- XP BAR SECTION - *NOW INCLUDED!*
    exp_bar_width = 200
    exp_bar_height = 10
    exp_bar_x = stats_x
    exp_bar_y = stats_y + 60
    exp_ratio = player.experience / player.max_experience
    current_exp_width = int(exp_bar_width * exp_ratio)
    pygame.draw.rect(screen, BLACK, (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height))
    pygame.draw.rect(screen, PURPLE, (exp_bar_x, exp_bar_y, current_exp_width, exp_bar_height))
    exp_text = SMALL_FONT.render(f"XP: {player.experience}/{player.max_experience}", True, WHITE)
    exp_text_rect = exp_text.get_rect(center=(exp_bar_x + exp_bar_width // 2, exp_bar_y + exp_bar_height // 2))
    screen.blit(exp_text, exp_text_rect)    


    # --- Buttons ---
    pygame.draw.rect(screen, WHITE, BUTTON1_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON2_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON3_RECT)
    pygame.draw.rect(screen, WHITE, BUTTON4_RECT)
    if CURRENT_STATE in BUTTON_TEXTS:
        button_texts = BUTTON_TEXTS[CURRENT_STATE]
        button1_text = BUTTON_FONT.render(button_texts[0], True, BLACK)
        button2_text = BUTTON_FONT.render(button_texts[1], True, BLACK)
        button3_text = BUTTON_FONT.render(button_texts[2], True, BLACK)
        button4_text = BUTTON_FONT.render(button_texts[3], True, BLACK)

        screen.blit(button1_text, button1_text.get_rect(center=BUTTON1_RECT.center))
        screen.blit(button2_text, button2_text.get_rect(center=BUTTON2_RECT.center))
        screen.blit(button3_text, button3_text.get_rect(center=BUTTON3_RECT.center))
        screen.blit(button4_text, button4_text.get_rect(center=BUTTON4_RECT.center))

    render_combat_buttons()
def render_monster_status_bar(): # <---- Function to render MONSTER status bar at TOP in combat
    global current_enemy # <--- Access current_enemy (should be set in combat)

    if current_enemy: # <--- Only render if there is a current enemy
        status_bar_x = 0# Top-left X position for status bar
        status_bar_y = 0 # Top-left Y position for status bar  <--- Position at the TOP
        status_bar_width = 800 # Adjust width as needed
        status_bar_height = 100 # Adjust height to fit all info
        STATUS_BAR_RECT = pygame.Rect(status_bar_x, status_bar_y, status_bar_width, status_bar_height) # Define STATUS_BAR_RECT for top position

        pygame.draw.rect(screen, GRAY, STATUS_BAR_RECT) # Background for status bar

        # --- Health Bar (for Enemy) ---  <---- Modified for ENEMY
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = status_bar_x + 50 # Offset within status bar
        health_bar_y = status_bar_y + 10 # Y position at the top of status bar
        health_ratio = current_enemy.current_health / current_enemy.stats["health"] if current_enemy.stats["health"] > 0 else 0 # Enemy health ratio
        current_health_width = int(health_bar_width * health_ratio)
        pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height)) # Health bar background
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height)) # Health bar fill
        health_text = SMALL_FONT.render(f"HP: {current_enemy.current_health}/{current_enemy.stats['health']}", True, BLACK) # Enemy health text
        health_text_rect = health_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y + health_bar_height // 2))
        screen.blit(health_text, health_text_rect) # Blit health text

        # --- Mana Bar (N/A for Monsters - Render Empty) --- <---- Mana Bar - RENDERED EMPTY
        #mana_bar_width = 200
        #mana_bar_height = 20
        #mana_bar_x = status_bar_x + 50
        #mana_bar_y = status_bar_y + 40 # Position below health bar
        #pygame.draw.rect(screen, BLACK, (mana_bar_x, mana_bar_y, mana_bar_width, mana_bar_height)) # Just draw the background, no fill
        #mana_text = SMALL_FONT.render(f"MP: N/A", True, BLACK) # "MP: N/A" text
        #mana_text_rect = mana_text.get_rect(center=(mana_bar_x + mana_bar_width // 2, mana_bar_y + mana_bar_height // 2))
        #screen.blit(mana_text, mana_text_rect) # Blit "MP: N/A"

        # --- Coins (N/A for Monsters - Render Empty) --- <---- Coins - RENDERED EMPTY
        #coin_text = SMALL_FONT.render(f"Coins: N/A", True, WHITE) # "Coins: N/A" text
        #screen.blit(coin_text, (status_bar_x + 50, status_bar_y + 70)) # Position below mana bar

        # --- Character Stats (Monster Stats) ---  <---- Modified for MONSTER STATS
        stats_x = status_bar_x + 260 # X position for stats (adjust as needed)
        stats_y = status_bar_y + 10 # Y position for stats
        stat_font = pygame.font.Font(None, 20)
        line_spacing = 20 # Line spacing for stats
        name_text = stat_font.render(f"Name: {current_enemy.get_name()}", True, WHITE) # Monster name
        screen.blit(name_text, (stats_x, stats_y))
        class_text = stat_font.render(f"Type: {current_enemy.monster_type}", True, WHITE) # Monster class
        screen.blit(class_text, (stats_x, stats_y + line_spacing))
        level_text = stat_font.render(f"Level: --", True, WHITE) # Level - Null value as requested
        screen.blit(level_text, (stats_x, stats_y + 2 * line_spacing))

        # --- Attack and Defense Section (Monster Stats) --- <---- Modified for MONSTER ATTACK/DEFENSE
        attack_defense_stats_x = status_bar_x + 400 # X position for attack/defense stats
        attack_defense_stats_y = status_bar_y + 10 # Y position
        attack_range = current_enemy.stats['attack'] # Get monster attack range
        min_attack_value = attack_range[0]
        max_attack_value = attack_range[1]
        buffed_min_attack = min_attack_value # Initialize buffed attack
        buffed_max_attack = max_attack_value # Initialize buffed max attack
        percentage_attack_buff_multiplier = 1.0 # For percentage attack buffs
        for buff in current_enemy.buffs: # Iterate through monster statuses (buffs/debuffs)
            if buff['stat'] == 'attack_buff': # Check for attack buffs
                if buff.get('is_percentage_buff'):
                    percentage_attack_buff_multiplier += buff['amount']
                else:
                    buffed_min_attack += buff['amount']
                    buffed_max_attack += buff['amount']

        buffed_min_attack = int(buffed_min_attack * percentage_attack_buff_multiplier) # Apply percentage buffs
        buffed_max_attack = int(buffed_max_attack * percentage_attack_buff_multiplier)

        attack_range_string = f"Attack: {buffed_min_attack}-{buffed_max_attack}" # Format attack range string
        attack_stat_text = stat_font.render(attack_range_string, True, WHITE) # Render attack text
        screen.blit(attack_stat_text, (attack_defense_stats_x, attack_defense_stats_y))
        attack_defense_stats_y += line_spacing # Move Y down for next stat
        defense_value = current_enemy.get_defense() # Get monster defense
        defense_text = stat_font.render(f"Defense: {defense_value}", True, WHITE) # Render defense text
        screen.blit(defense_text, (attack_defense_stats_x, attack_defense_stats_y))
        attack_defense_stats_y += line_spacing

        dodge_chance = current_enemy.get_evasion() # Get monster evasion
        dodge_text = stat_font.render(f"Dodge: {dodge_chance}%", True, WHITE) # Render dodge text
        screen.blit(dodge_text, (attack_defense_stats_x, attack_defense_stats_y)) # Position dodge text
        attack_defense_stats_y += line_spacing

        # --- Buffs Display Section (Monster Buffs) --- <---- Modified for MONSTER BUFFS
        buff_display_x = status_bar_x + 540 # X position for buffs display
        buff_display_y = status_bar_y + 10 # Y position for buffs display
        buff_title_text = stat_font.render("Buffs:", True, BLACK) # "Buffs:" title
        screen.blit(buff_title_text, (buff_display_x, buff_display_y)) # Blit title
        buff_display_y += line_spacing # Move Y down for first buff

        for buff in current_enemy.buffs: # Iterate through monster's active statuses (buffs/debuffs)
            buff_text = stat_font.render(f"- {buff['name']} ({buff['duration_turns']} turns)", True, WHITE) # Format buff text - CORRECTED KEY
            screen.blit(buff_text, (buff_display_x, buff_display_y)) # Blit buff text
            buff_display_y += line_spacing # Move Y down for next buff
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
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.buffs = []  # <--- Use buffs instead of statuses, initialize as empty list
        self.abilities = abilities

    def choose_ability(self, target):
        """Monster chooses an ability to use, or defaults to normal attack."""
        if not self.abilities:
            return None

        ability_chance = 0.3
        if random.random() < ability_chance:
            ability_set_name = self.abilities[0]
            ability_choices = MONSTER_ABILITIES.get(ability_set_name)
            if ability_choices:
                chosen_ability = random.choice(ability_choices)
                print(f"{self.name} chooses to use ability: {chosen_ability['name']}")
                return chosen_ability
        return None

    def use_ability(self, ability, target):
        """Executes a monster ability against a target."""
        if ability['type'] == 'attack':
            damage_multiplier = ability.get('damage_multiplier', 1.0)
            base_damage = self.get_attack_damage()
            damage = max(0, int(base_damage * damage_multiplier) - target.get_defense())
            damage_dealt = target.take_damage(damage)
            print(f"{self.name} uses **{ability['name']}** and hits you for {damage_dealt} damage!")

        elif ability['type'] == 'buff':
            buff_stat = ability['stat']
            buff_amount = ability['buff_amount']
            duration_turns = ability['duration_turns']
            buff_name = ability['name']
            buff_dict = {
                'name': buff_name,
                'stat': buff_stat,
                'amount': buff_amount,
                'duration_turns': duration_turns,
                'is_percentage_buff': True if buff_stat.endswith('_buff') else False
            }
            self.apply_buff(buff_dict)
            print(f"{self.name} uses **{ability['name']}** and buffs its {buff_stat} by {buff_amount*100}% for {duration_turns} turns!")

        elif ability['type'] == 'debuff':
            debuff_stat = ability['stat']
            debuff_amount = ability['buff_amount']
            duration_turns = ability['duration_turns']
            debuff_name = ability['name']
            debuff_dict = {
                'name': debuff_name,
                'stat': debuff_stat,
                'amount': debuff_amount,
                'duration': duration_turns,
                'is_percentage_buff': True if debuff_stat.endswith('_buff') else False
            }
            target.apply_buff(debuff_dict)
            print(f"{self.name} uses **{ability['name']}** and debuffs your {debuff_stat} by {abs(debuff_amount)*100}% for {duration_turns} turns!")
        else:
            print(f"{self.name} tried to use unknown ability type: {ability['type']}")

    def apply_buff(self, buff_data):
        """Applies a buff to the monster, handling duration and refresh."""
        buff_name = buff_data['name']
        buff_stat = buff_data['stat']
        buff_duration = buff_data['duration_turns'] if 'duration_turns' in buff_data else 3
        buff_type = buff_data.get('buff_type')

        print(f"{self.name} applying buff: Name='{buff_name}', Stat='{buff_stat}', Type='{buff_type}'")

        existing_buff_index = -1
        for index, buff in enumerate(self.buffs):
            if buff['name'] == buff_name and buff['stat'] == buff_stat:
                existing_buff_index = index
                break

        if existing_buff_index != -1:
            self.buffs[existing_buff_index]['duration_turns'] = buff_duration
            print(f"  Buff '{buff_name}' duration refreshed on {self.name}.")
        else:
            buff = buff_data.copy()
            buff['duration_turns'] = buff_duration
            self.buffs.append(buff)
            print(f"  {self.name} buffed with '{buff_name}'!")

    def get_name(self):
        return self.name

    def get_health(self):
        return self.current_health

    def take_damage(self, damage):
        damage_taken = max(0, damage)
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
        for buff in self.buffs: # <--- Check buffs list, not statuses
            if buff["name"] == "stun" and buff["duration_turns"] > 0: # Check 'duration_turns'
                return True
        return False

    def get_accuracy(self):
        """Retrieves monster accuracy, including buffs, returning WHOLE NUMBER PERCENTAGE (0-100)."""
        base_accuracy_percentage = self.stats['accuracy']
        buffed_accuracy_percentage = base_accuracy_percentage
        for buff in self.buffs: # <--- Iterate through buffs, not statuses
            if buff.get('stat') == 'accuracy_buff':
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['amount']
                    buffed_accuracy_percentage += percentage_increase
                else:
                    buffed_accuracy_percentage += buff['amount']
        return buffed_accuracy_percentage

    def get_evasion(self):
        """Retrieves monster evasion, including buffs, returning WHOLE NUMBER PERCENTAGE (0-100)."""
        base_evasion_percentage = self.stats['evasion']
        buffed_evasion_percentage = base_evasion_percentage
        for buff in self.buffs: # <--- Iterate through buffs, not statuses
            if buff.get('stat') == 'evasion_buff':
                if buff.get('is_percentage_buff'):
                    percentage_increase = buff['amount']
                    buffed_evasion_percentage += percentage_increase
                else:
                    buffed_evasion_percentage += buff['amount']
        return buffed_evasion_percentage

    def update_buff_durations(self):
        """Updates buff durations for the monster, removing expired buffs."""
        buffs_to_remove = []
        for buff in self.buffs: # <--- Iterate through buffs, not statuses
            buff['duration_turns'] -= 1 # Use 'duration_turns'
            if buff['duration_turns'] <= 0:
                buffs_to_remove.append(buff)
                print(f"Buff '{buff['name']}' expired from {self.name}.")
        for buff in buffs_to_remove:
            self.buffs.remove(buff)

    def attack(self, target):
        """Monster attacks a target (player)."""
        if self.is_stunned():
            print(f"{self.get_name()} is stunned and cannot attack!")
            return 0

        # --- 1. Accuracy Check ---
        accuracy_roll = random.random()
        monster_accuracy_percentage = self.get_accuracy() # Get as whole percentage
        monster_accuracy_decimal = monster_accuracy_percentage / 100.0 # Convert to decimal

        print(f"Debug (Accuracy Check): Monster: {self.get_name()}, Accuracy Roll: {accuracy_roll:.2f}, Monster Accuracy: {int(monster_accuracy_percentage)}%")

        if accuracy_roll < monster_accuracy_decimal:
            print(f"Debug (Accuracy Check): Accuracy check passed for {self.get_name()}.")

            # --- 2. Evasion Check ---
            evasion_roll = random.random()
            player_evasion_percentage = target.get_evasion() # Player evasion as whole percentage
            player_evasion_decimal = player_evasion_percentage / 100.0 # Convert to decimal

            print(f"Debug (Evasion Check): Monster: {self.get_name()}, Player: {target.get_name()}, Evasion Roll: {evasion_roll:.2f}, Player Evasion: {int(player_evasion_percentage)}%")

            if evasion_roll < player_evasion_decimal:
                print(f"{target.get_name()} **DODGED** the attack from {self.get_name()}!")
                return 0

            else: # Hit and Damage
                print(f"Debug (Evasion Check): Evasion check failed - proceeding with hit.")
                attack_range = self.stats['attack']
                base_damage = random.randint(attack_range[0], attack_range[1])
                damage = max(0, base_damage - target.get_defense())
                print(f"Debug: {self.get_name()} attacks {target.get_name()}, Damage: {damage}")
                damage_dealt = target.take_damage(damage)
                if damage_dealt > 0:
                    print(f"{self.get_name()} attacks you and **HIT** for {damage_dealt} damage!")
                else:
                    print(f"{self.get_name()} attacks you but deals no damage!")
                return damage_dealt
        else: # Miss due to inaccuracy
            print(f"Debug (Accuracy Check): Accuracy check failed - **MISSED** due to inaccuracy.")
            print(f"{self.get_name()} **MISSED** you!")
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/Goblin.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/rat.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/bigrat.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/spider.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/skeleton_warrior.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/giant_rat.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/siren.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/mimic.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/orc.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/succubus.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/lich.png",
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
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/dragon.png",
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
            "description": "A quick dodge, increasing evasion for 2 turns.", # Corrected description
            "type": "buff",
            "stat": "evasion_buff",  # <--- CORRECTED to "evasion_buff"
            "buff_amount": 15,      # <--- CORRECTED to whole number percentage (15%)
            "duration_turns": 2,
            "is_percentage_buff": True # <--- ADDED to specify percentage buff
        },
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
    "healing_potion_1": { # Unique item ID (you can use names or generate IDs)
        "name": "Minor Healing Potion",
        "description": "Restores a small amount of health.",
        "price": 25,
        "category": "Potions",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/potion_small.png", # Path to a small potion icon
        "effect": {"type": "heal", "amount": 20} # Example effect: heals 20 HP
    },
    "basic_sword_1": {
        "name": "Iron Sword",
        "description": "A simple but reliable iron sword.",
        "price": 100,
        "category": "Weapons",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/sword_iron.png", # Path to an iron sword icon
        "stats_bonus": {"attack": 5} # Example stat bonus: +5 Attack
    },
    "leather_armor_1": {
        "name": "Leather Armor",
        "description": "Light and flexible leather armor.",
        "price": 80,
        "category": "Armor",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/armor_leather.png", # Path to a leather armor icon
        "stats_bonus": {"defense": 3} # Example stat bonus: +3 Defense
    },
    "scroll_ Minor Damage": {
        "name": "Scroll of Minor Damage",
        "description": "A scroll that unleashes a small burst of magical damage.",
        "price": 50,
        "category": "Scrolls",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/scroll_damage.png", # Path to a scroll icon
        "effect": {"type": "damage", "amount": 10, "target": "enemy"} # Example effect: deals 10 damage to enemy
    },
    "torch_1": {
        "name": "Torch",
        "description": "Provides light in dark places. Mostly useful in dungeons.",
        "price": 10,
        "category": "Misc.",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/torch.png", # Path to a torch icon
        "effect": {"type": "utility", "use": "light"} # Example utility effect
    },
     "medium_healing_potion_1": { # Unique item ID (you can use names or generate IDs)
        "name": "Medium Healing Potion",
        "description": "Restores a medium amount of health.",
        "price": 50,
        "category": "Potions",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/potion_medium.png", # Path to a medium potion icon
        "effect": {"type": "heal", "amount": 40} # Example effect: heals 40 HP
    },
    "steel_sword_1": {
        "name": "Steel Sword",
        "description": "A sturdy steel sword, better than iron.",
        "price": 200,
        "category": "Weapons",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/sword_steel.png", # Path to a steel sword icon
        "stats_bonus": {"attack": 10} # Example stat bonus: +10 Attack
    },
    "chainmail_armor_1": {
        "name": "Chainmail Armor",
        "description": "Provides good protection.",
        "price": 150,
        "category": "Armor",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/armor_chainmail.png", # Path to a chainmail armor icon
        "stats_bonus": {"defense": 6} # Example stat bonus: +6 Defense
    },
    "scroll_ Medium Damage": {
        "name": "Scroll of Medium Damage",
        "description": "A scroll that unleashes a moderate burst of magical damage.",
        "price": 100,
        "category": "Scrolls",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/scroll_medium_damage.png", # Path to a scroll icon
        "effect": {"type": "damage", "amount": 20, "target": "enemy"} # Example effect: deals 20 damage to enemy
    },
    "rope_1": {
        "name": "Rope",
        "description": "A sturdy rope. Useful for climbing and other things.",
        "price": 20,
        "category": "Misc.",
        "image_path": "PythonGaming V3/PYTHON Gaming/Images/rope.png", # Path to a rope icon
        "effect": {"type": "utility", "use": "climbing"} # Example utility effect
    },
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
        monster = Monster(
            data["name"],
            data["monster_type"], # Assuming "monster_type" in data is meant to be description - adjust if needed
            scaled_health, # Use scaled health
            scaled_attack_range, # Use scaled attack range
            scaled_defense, # Use scaled defense
            data["accuracy"],
            scaled_evasion,
            data["experience"],
            gold_value,
            data["image_path"],
            data["abilities"] # Assuming you have "abilities" defined in your monster_data
        )
        try:
            monster_image = pygame.image.load(data["image_path"]).convert_alpha()
            monster.image = monster_image
        except pygame.error as e:
            monster.image = None
            print(f"Error loading image for {monster_name} from path: {data['image_path']}. Error: {e}")
        return monster
    else:
        print(f"Monster data not found for: {monster_name}")
        return None
    
def load_monster_images():
    for monster_name, monster_info in monster_data.items():
        image_path = monster_info.get("image_path") # Get image_path from monster data
        if image_path: # Check if image_path is defined
            try:
                image = pygame.image.load(image_path).convert_alpha() # Load image, convert_alpha for transparency
                monster_data[monster_name]["image"] = image # Store loaded image back in monster_data
            except pygame.error as e:
                print(f"ERROR: Could not load image for {monster_name} from: {image_path}") # Error print
                print(f"Pygame error: {e}") # Print specific Pygame error message
                monster_data[monster_name]["image"] = None # Set image to None if loading fails
        else:
            print(f"WARNING: No image_path defined for {monster_name}") # Warning if image_path is missing
            monster_data[monster_name]["image"] = None # Set image to None if no path
load_monster_images()
#Dungeon Room Generation
room_content_options = {
    "empty": None,
    "chest": None,
    "rat": "Rat",
    "goblin": "Goblin",
    "spider": "Spider",
    "skeletonw": "Skeleton",
    "BigRat":"Big Rat",
    "orc": "Orc",
    "mimic": "Mimic",
    "sirien": "Sirien",
    "giantrat": "Giantrat",
    "lich": "Lich",
    "dragon": "Dragon",
    "succubus": "Succubus",
    "trap": None
}
roomtable_probabilities = {
    0: {  # Floor 0: Very Easy Start (Tutorial/Early Game)
        "empty": 0.3,      # Higher chance of empty rooms
        "rat": 0.3,        # Common basic enemy
        "goblin": 0.2,     # Slightly less common basic enemy
        "Big Rat": 0.05,   # Minor challenge increase
        "spider": 0.03,    # Slightly rarer, minor challenge
        "Skeleton Warrior": 0.0, # Not present on level 0
        "orc": 0.0,          # Not present on level 0
        "mimic": 0.01,     # Rare, surprise element
        "Siren": 0.0,        # Not present on level 0
        "Giant Rat": 0.0,    # Not present on level 0
        "Lich": 0.0,         # Not present on level 0
        "Dragon": 0.0,       # Not present on level 0
        "Succubus": 0.0,     # Not present on level 0
        "trap": 0.01,      # Very low chance of trap, just to introduce mechanic
        "staircase_down": 0.1 # Encourage exploration on first floor
    },
    1: {  # Floor 1: Easy (Level 1-3 Challenge)
        "empty": 0.25,
        "rat": 0.25,
        "goblin": 0.2,
        "Big Rat": 0.1,
        "spider": 0.05,
        "Skeleton Warrior": 0.05, # Introduce Skeleton Warriors
        "orc": 0.0,
        "mimic": 0.02,
        "Siren": 0.0,
        "Giant Rat": 0.0,
        "Lich": 0.0,
        "Dragon": 0.0,
        "Succubus": 0.0,
        "trap": 0.02,
        "staircase_down": 0.05 # Slightly higher chance of staircase
    },
    2: {  # Floor 2: Medium-Easy (Level 2-4 Challenge)
        "empty": 0.25,
        "rat": 0.15,
        "goblin": 0.15,
        "Big Rat": 0.1,
        "spider": 0.1,
        "Skeleton Warrior": 0.1,
        "orc": 0.05,         # Introduce Orcs
        "mimic": 0.03,
        "Siren": 0.0,
        "Giant Rat": 0.02,    # Introduce Giant Rats
        "Lich": 0.01,
        "Dragon": 0.01,
        "Succubus": 0.02,
        "trap": 0.04,
        "staircase_down": 0.05
    },
    3: {  # Floor 3: Medium (Level 3-5 Challenge)
        "empty": 0.2,
        "rat": 0.05,        # Rats becoming less common
        "goblin": 0.1,      # Goblins slightly less common
        "Big Rat": 0.05,
        "spider": 0.05,
        "Skeleton Warrior": 0.15,
        "orc": 0.15,
        "mimic": 0.05,
        "Siren": 0.05,       # Introduce Sirens
        "Giant Rat": 0.1,
        "Lich": 0.0,
        "Dragon": 0.0,
        "Succubus": 0.0,
        "trap": 0.08,
        "staircase_down": 0.02
    },
    4: {  # Floor 4: Medium-Hard (Level 5-7 Challenge)
        "empty": 0.15,
        "rat": 0.0,         # No more Rats
        "goblin": 0.0,      # No more Goblins (mostly)
        "Big Rat": 0.0,
        "spider": 0.02,     # Spiders very rare now
        "Skeleton Warrior": 0.1,
        "orc": 0.2,
        "mimic": 0.08,
        "Siren": 0.1,
        "Giant Rat": 0.15,
        "Lich": 0.05,        # Introduce Liches (rare, mini-boss type)
        "Dragon": 0.0,
        "Succubus": 0.03,     # Introduce Succubi (rare, dangerous)
        "trap": 0.1,
        "staircase_down": 0.02
    },
    5: {  # Floor 5: Hard (Level 6-8 Challenge)
        "empty": 0.1,
        "goblin": 0.0,
        "Skeleton Warrior": 0.05, # Skeletons less common
        "orc": 0.15,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.05,
        "Siren": 0.15,
        "Giant Rat": 0.1,
        "Lich": 0.2,         # Liches more common
        "Dragon": 0.02,       # Introduce Dragons (very rare, special encounter)
        "Succubus": 0.08,     # Succubi still rare but more frequent
        "trap": 0.15,
        "staircase_down": 0.03
    },
    6: {  # Floor 6: Harder (Level 7-9 Challenge)
        "empty": 0.08,
        "goblin": 0.0,
        "Skeleton Warrior": 0.02,
        "orc": 0.1,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.03,
        "Siren": 0.1,
        "Giant Rat": 0.05,
        "Lich": 0.3,         # High Lich chance
        "Dragon": 0.05,       # Dragons still rare but a threat
        "Succubus": 0.12,     # Succubi more common
        "trap": 0.17,
        "staircase_down": 0.05
    },
    7: {  # Floor 7: Very Hard (Level 8-10 Challenge)
        "empty": 0.05,
        "goblin": 0.0,
        "Skeleton Warrior": 0.0,
        "orc": 0.05,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.02,
        "Siren": 0.05,
        "Giant Rat": 0.0,
        "Lich": 0.4,         # Very High Lich Chance
        "Dragon": 0.1,        # Dragons more frequent
        "Succubus": 0.2,      # Succubi becoming significant threat
        "trap": 0.2,
        "staircase_down": 0.05
    },
    8: {  # Floor 8: Extremely Hard (Level 9-12 Challenge)
        "empty": 0.03,
        "goblin": 0.0,
        "Skeleton Warrior": 0.0,
        "orc": 0.01,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.01,
        "Siren": 0.02,
        "Giant Rat": 0.0,
        "Lich": 0.5,         # Extremely High Lich Chance
        "Dragon": 0.15,       # Dragons are a definite threat now
        "Succubus": 0.25,     # High Succubus chance
        "trap": 0.28,
        "staircase_down": 0.05
    },
    9: {  # Floor 9: Near Maximum Difficulty (Level 11-14 Challenge)
        "empty": 0.01,
        "goblin": 0.0,
        "Skeleton Warrior": 0.0,
        "orc": 0.0,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.005,
        "Siren": 0.01,
        "Giant Rat": 0.0,
        "Lich": 0.6,         # Dominant Lich presence
        "Dragon": 0.2,        # Dragons are common and dangerous
        "Succubus": 0.3,      # Succubi very common, major threat
        "trap": 0.375,
        "staircase_down": 0.05
    },
    10: { # Floor 10: Maximum Difficulty (Level 12-15 Challenge - End Game?)
        "empty": 0.0,        # No empty rooms at max depth - constant threat
        "goblin": 0.0,
        "Skeleton Warrior": 0.0,
        "orc": 0.0,
        "spider": 0.0,
        "rat": 0.0,
        "Big Rat": 0.0,
        "mimic": 0.0,
        "Siren": 0.0,
        "Giant Rat": 0.0,
        "Lich": 0.7,         # Overwhelming Lich presence
        "Dragon": 0.3,        # Dragons very common, expect them in most rooms
        "Succubus": 0.0,      # Succubi removed on final level? Or could keep them and make even more deadly
        "trap": 0.0,         # No traps? Or could add deadly traps
        "staircase_down": 0.0 # No stairs down from max level - final level
    },
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
    level_probabilities = roomtable_probabilities.get(roomlvl, roomtable_probabilities.get(max(roomtable_probabilities.keys())))
    if not level_probabilities:
        return "empty"
    content_choices = list(level_probabilities.keys())
    probabilities = list(level_probabilities.values())
    return random.choices(content_choices, weights=probabilities, k=1)[0]
def generate_monster_for_room_content(room_content, roomlvl): # <--- Added roomlvl parameter
    monster_types = {
        "rat": "Rat", "goblin": "Goblin", "spider": "Spider", "skeletonw": "Skeleton Warrior", # Corrected "Skeleton" to "Skeleton Warrior" to match monster_data key
        "orc": "Orc", "mimic": "Mimic", "siren": "Siren", "giantrat": "Giant Rat", # Corrected "Sirien" to "Siren" and "Giantrat" to "Giant Rat" to match monster_data keys
        "lich": "Lich", "dragon": "Dragon", "succubus": "Succubus"
    }
    monster_name = monster_types.get(room_content.lower()) # <-- Case-insensitive lookup
    if monster_name:
        monster_instance = create_monster(monster_name, roomlvl) # <--- Pass roomlvl to create_monster
        return monster_instance
    else:
        return None
def generate_room(room_id, name, roomlvl): # <---- Added roomlvl parameter here!
    room_content = roomroll()
    monster = None
    room_type = 0 # 0: Empty, 1: Monster, 2: Treasure, 3: Trap, 4:Staircase
    if room_content.lower() in [monster_type.lower() for monster_type in ["rat", "goblin", "skeleton", "big_rat","spider","skeletonw","orc","mimic","sirien","giantrat","lich","dragon","succubus"]]: #Monster room
        monster = generate_monster_for_room_content(room_content, roomlvl) # <---- Pass roomlvl here!
        room_type = 1
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)
    elif room_content == "chest": #treasure room
        room_type = 2
        content_description = "You found a chest."
    elif room_content == "trap": #trap room - not yet implemented
        room_type = 3
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)
    elif room_content == "staircase_down": #staircase room
        room_type = 4
        content_description = "You found a staircase leading down."
    else: #empty room
        content_description = random.choice(EMPTY_ROOM_DESCRIPTIONS)
    room = {
        "id": room_id,
        "name": name,
        "content": room_content,
        "description": content_description,
        "monster": monster,
        "type": room_type #0=empty, 1=monster, 2=treasure room/chest, 3=trap, 4=Staircase
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
    "rough_couch": {
        "name": "Rough Couch",
        "cost": 5,
        "hp_restore": 20,
        "mana_restore": 30,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.05,
        "defense_boost_percentage": 0.0,
        "duration": 5,
        "description": "A worn, lumpy couch. Better than the floor." 
    },
    "cozy_bed": {
        "name": "Cozy Bed",
        "cost": 15,
        "hp_restore": 50,
        "mana_restore": 40,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.10,
        "defense_boost_percentage": 0.05,
        "duration": 8,
        "description": "A soft bed with fresh linens. Quite comfortable."
    },
    "luxurious_suite": {
        "name": "Luxurious Suite",
        "cost": 30,
        "hp_restore": 100,
        "mana_restore": 100,       # <--- ADD MANA RESTORE VALUE
        "attack_boost_percentage": 0.20,
        "defense_boost_percentage": 0.10,
        "duration": 12,
        "description": "The finest room in the tavern. Pure luxury." 
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
def use_ability(ability, caster, target):
    """Handles ability use, applying effects based on ability type."""
    if caster.use_mana(ability["mana_cost"]):
        ability_name = ability["name"]
        combat_log_messages.append(f"{caster.name} uses {ability_name}!")
        ability_type = ability["type"]
        if ability_type == "attack" or ability_type == "magic_attack": # Handle both attack types similarly for now
            damage_multiplier = ability.get("damage_multiplier", 1.0) # Default multiplier to 1.0 if not specified
            damage = int(caster.get_attack_damage() * damage_multiplier)
            if ability_type == "magic_attack":
                damage = int(damage * 3) # Example: Magic attacks do 20% more base damage for now - balance later
            damage_dealt = target.take_damage(damage)
            combat_log_messages.append(f"{ability_name} hits {target.get_name()} for {damage_dealt} damage!")
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
                caster.apply_buff(buff_data)
            elif buff_stat == "magic_shield": # Mage Magic Shield (flat buff) - corrected stat name
                buff_data = {
                    "name": buff_name,
                    "stat": "defense_buff", #  Using defense_buff for magic shield too - adjust logic if needed later
                    "amount": buff_amount, # buff_amount is flat amount (e.g., 50 flat defense)
                    "duration_turns": buff_duration
                }
                caster.apply_buff(buff_data)

            elif buff_stat == "evasion": # Rogue Evasion
                buff_data = {
                "name": ability_name,
                "stat": "evasion_buff",
                "amount": buff_amount,
                "duration_turns": buff_duration,
                "is_percentage_buff": True
                }
                caster.apply_buff(buff_data)
        elif ability_type == "heal": # Heal ability
            heal_amount = ability["heal_amount"]
            caster.current_health = min(caster.stats['health'], caster.current_health + heal_amount) # Heal, but not over max HP
            combat_log_messages.append(f"{ability_name} heals {caster.name} for {heal_amount} HP!")

        elif ability_type == "multi_attack": # For abilities with multiple attacks (like Rogue's Double Attack - not used yet but prepared)
            number_of_attacks = ability.get("number_of_attacks", 1) # Default to 1 attack if not specified
            damage_multiplier = ability.get("damage_multiplier", 1.0)
            for _ in range(number_of_attacks): # Loop for each attack
                damage = int(caster.get_attack_damage() * damage_multiplier)
                damage_dealt = target.take_damage(damage)
                combat_log_messages.append(f"{ability_name} hits {target.get_name()} for {damage_dealt} damage!")
        # After ability use, end player's turn
        global player_turn
        player_turn = False
    else:
        combat_log_messages.append(f"{caster.name} does not have enough mana to use {ability['name']}!")
def descend_staircase():
    global current_room_id, roomlvl, rooms, player_room_count, CURRENT_STATE, current_enemy, player_turn # <--- Include CURRENT_STATE, current_enemy, player_turn in globals
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
    global current_room_id, CURRENT_STATE, current_enemy, player_room_count, roomlvl, rooms, player_turn # Keep player_turn if you use it globally
    current_room = rooms[current_room_id] # <---- Fetch current_room ONCE at the beginning
    if current_room["monster"] and current_room["monster"].is_alive():
        print("You cannot leave while a monster is alive!")
        return
    next_room_number = int(current_room_id[4:]) + 1
    next_room_id = f"room{next_room_number}"
    next_room_name = f"Room {next_room_number}"
    player_room_count += 1
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
    global player, rooms, current_room_id, roomlvl, player_room_count, current_enemy, CURRENT_STATE, player_turn
    print("Resetting Game State...")
    # --- 2. Regenerate Dungeon ---
    roomlvl = 0  # Reset to starting dungeon level (usually 0 or 1)
    player_room_count = 0 # Reset room exploration count
    rooms = create_room_dictionary(roomlvl) # **Crucially, regenerate the dungeon rooms!**
    current_room_id = "room1" # Set player to start at the first room of the new dungeon
    print("Dungeon regenerated.")
    # --- 3. Reset Combat State ---
    current_enemy = None  # Clear any current enemy
    CURRENT_STATE = MENU  # **Set game state back to DUNGEON (or TOWN, if you start in town)**
    player_turn = True      # Reset player turn for combat (if applicable)
    print("Combat state reset.")
    print("Game state reset complete. Ready for a new game run.")
def draw_rest_options_box():
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 300) # Example box size/position
    pygame.draw.rect(screen, (200, 200, 200), box_rect) # Light gray box background
    pygame.draw.rect(screen, BLACK, box_rect, 2) # Black border
    title_font = pygame.font.Font(None, 40)
    title_text = title_font.render("Rest Options", True, BLACK)
    title_rect = title_text.get_rect(center=(box_rect.centerx, box_rect.top + 20))
    screen.blit(title_text, title_rect)
    y_offset = 0
    for option_key, option_data in REST_OPTIONS.items():
        button_rect = REST_OPTION_BUTTON_RECTS[option_key]
        pygame.draw.rect(screen, (150, 150, 150), button_rect) # Button background
        pygame.draw.rect(screen, BLACK, button_rect, 1) # Button border
        option_font = pygame.font.Font(None, 30)
        option_text = option_font.render(f"{option_data['name']} ({option_data['cost']} Gold)", True, BLACK)
        option_rect = option_text.get_rect(center=button_rect.center)
        screen.blit(option_text, option_rect)
        # --- Display Option Description ---
        description_font = pygame.font.Font(None, 24) # Smaller font for description
        # --- Wrap text to fit within the box width ---
        wrapped_description_lines = wrap_text(option_data['description'], description_font, box_rect.width - 40) # box_rect.width - 40 for padding

        description_y_start = button_rect.bottom + 5 # Start description below button
        for line in wrapped_description_lines:
            description_text_surface = description_font.render(line, True, BLACK)
            description_rect = description_text_surface.get_rect(topleft=(button_rect.left + 10, description_y_start)) # Add some left padding
            screen.blit(description_text_surface, description_rect)
            description_y_start += description_font.get_linesize() # Move to next line for multi-line descriptions
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
def draw_inventory_box():
    pygame.draw.rect(screen, INVENTORY_BOX_COLOR, INVENTORY_BOX_RECT)
def draw_shop_menu():
    pygame.draw.rect(screen, SHOP_MENU_COLOR, SHOP_MENU_RECT) # Main shop menu box
    draw_shop_tabs() # Call function to draw tabs
    draw_item_slots() # Call function to draw item slots
    draw_scroll_buttons() # Call function to draw scroll buttons
def draw_item_slots():
    for i in range(4): # Still 4 item slots for now
        slot_rect = pygame.Rect(
            ITEM_SLOTS_START_X,
            ITEM_SLOTS_START_Y + i * (ITEM_SLOT_HEIGHT + ITEM_SLOT_SPACING_Y),
            ITEM_SLOT_WIDTH,
            ITEM_SLOT_HEIGHT
        )
        pygame.draw.rect(screen, SLOT_COLOR, slot_rect) # Draw item slot rectangles

        if i < len(current_shop_items): # Check if there's an item for this slot index
            item_id = current_shop_items[i] # Get item ID from current_shop_items list
            item_data = shop_items_data[item_id] # Get item data from shop_items_data
            item_name = item_data["name"] # Get item name

            item_text_surface = SMALL_FONT.render(item_name, True, WHITE) # Render item name text
            item_text_rect = item_text_surface.get_rect(center=slot_rect.center) # Center text in slot
            screen.blit(item_text_surface, item_text_rect) # Blit item name text
def draw_scroll_buttons():
    pygame.draw.rect(screen, BUTTON_COLOR, SCROLL_UP_BUTTON_RECT) # "Scroll Up" button
    pygame.draw.rect(screen, BUTTON_COLOR, SCROLL_DOWN_BUTTON_RECT) # "Scroll Down" button
    up_text_surface = SMALL_FONT.render("Up", True, WHITE) # "Up" text
    up_rect = up_text_surface.get_rect(center=SCROLL_UP_BUTTON_RECT.center)
    screen.blit(up_text_surface, up_rect)
    down_text_surface = SMALL_FONT.render("Down", True, WHITE) # "Down" text
    down_rect = down_text_surface.get_rect(center=SCROLL_DOWN_BUTTON_RECT.center)
    screen.blit(down_text_surface, down_rect)
def load_shop_item_images():
    for item_id, item_info in shop_items_data.items():
        image_path = item_info.get("image_path")
        if image_path:
            try:
                image = pygame.image.load(image_path).convert_alpha()
                shop_items_data[item_id]["image"] = image
            except pygame.error as e:
                shop_items_data[item_id]["image"] = None
        else:
            print(f"WARNING: No image_path defined for item {item_id}")
            shop_items_data[item_id]["image"] = None
load_shop_item_images()
def populate_shop_items():
    global current_shop_items, current_shop_category_index
    current_shop_items = [] # Clear the current items list
    selected_category = SHOP_CATEGORIES[current_shop_category_index] # Get selected category name
    items_added = 0 # Counter to limit to 4 items per category for now
    for item_id, item_data in shop_items_data.items():
        if item_data["category"] == selected_category: # Check if item belongs to selected category
            current_shop_items.append(item_id) # Add item ID to the current items list
            items_added += 1
            if items_added >= 4: # Limit to 4 items for now (for 4 slots)
                break # Stop after adding 4 items
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
                    CURRENT_STATE = GAME_OVER
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
    retry_text_rect = retry_text.get_rect(center=RETRY_BUTTON_RECT.center) # Center text in button
    screen.blit(retry_text, retry_text_rect)
    pygame.display.flip() # Update the display to show the button
def handle_game_over_events(events):
    global CURRENT_STATE 
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if RETRY_BUTTON_RECT.collidepoint(mouse_pos): # Check for Retry button click
                print("Retry Button Clicked from handle_game_over_events!")
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
def handle_character_creation_events(events):  # <--- Parameter is now 'events' (plural - list of events)
    global INPUT_ACTIVE, PLAYER_NAME, PLAYER_CLASS_NAME, player # Corrected global declaration - use 'player' (lowercase)
    mouse_pos = pygame.mouse.get_pos()  # Mouse position is needed, get it outside the loop once
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
                        global player, CURRENT_STATE # Global declaration - ensure 'player' is global
                        player_class_stats = CLASS_STATS[PLAYER_CLASS_NAME] # Get base class stats (use a different variable name for clarity)
                        # --- NEW DEBUG PRINT BEFORE PLAYER CREATION ---
                        print("Debug - Before Player Creation: CLASS_STATS['Warrior']['attack']:") 
                        print(CLASS_STATS['Warrior']['attack'])
                        print("Debug - Before Player Creation: CLASS_STATS['Mage']['attack']:") 
                        print(CLASS_STATS['Mage']['attack'])
                        print("Debug - Before Player Creation: CLASS_STATS['Rogue']['attack']:") 
                        print(CLASS_STATS['Rogue']['attack'])
                        player = Player(PLAYER_NAME, PLAYER_CLASS_NAME)
                        print("Debug - Character Creation: Player Attack Stats after creation:")
                        print(f"Player Class: {player.class_name}")
                        print(f"Player Attack: {player.stats['attack']}")
                        CURRENT_STATE = TOWN
                        print(f"Character Created: Name={player.name}, Class={player.class_name}")
        elif event.type == pygame.KEYDOWN:  # Check for KEYDOWN events within the loop
            if INPUT_ACTIVE:  # Only process key presses if input is active
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
    mouse_pos = pygame.mouse.get_pos() # Mouse position is needed, so get it outside the loop once
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if BUTTON1_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = TAVERN
                elif BUTTON2_RECT.collidepoint(mouse_pos):
                    CURRENT_STATE = SHOP
                elif BUTTON3_RECT.collidepoint(mouse_pos):
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
    global player, SHOW_REST_OPTIONS_BOX  # Ensure 'player' and 'SHOW_REST_OPTIONS_BOX' are declared as global

    selected_option = REST_OPTIONS[option_key]  # Get the data for the selected rest option from REST_OPTIONS
    cost = selected_option["cost"]  # Extract the gold cost from the selected option data

    if player.coins >= cost:  # Check if the player has enough coins to afford the rest option
        player.coins -= cost  # Deduct the cost from the player's coin balance
        apply_rest_buff(player, selected_option)  
        print(f"Player chose {selected_option['name']}. Cost: {cost} Gold. Buff applied.") 
    else:
        print("Not enough gold to rest here!")  # Print "not enough gold" message to the console

    SHOW_REST_OPTIONS_BOX = False  # Regardless of success or failure, close the rest options box after the click
def handle_tavern_events(events):
    global CURRENT_STATE, SHOW_REST_OPTIONS_BOX, TAVERN_REST_EXIT_BUTTON_RECT
    for current_event in events:
        if current_event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse button press event (click) - no button check needed here
            mouse_pos = pygame.mouse.get_pos() # Get mouse position inside MOUSEBUTTONDOWN block
            if BUTTON1_RECT.collidepoint(mouse_pos): # Check for Status Bar Button 1 (Rest Button) click
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
    pygame.display.flip()
    global CURRENT_STATE, screen
    screen.fill((80, 80, 120))
    populate_shop_items() # <--- CALL populate_shop_items() at start of handle_shop()
    draw_shop_menu()
    draw_inventory_box()
    render_status_bar()
def handle_shop_events(events): # <--- Parameter is now 'events' (plural - list of events)
    global CURRENT_STATE, current_shop_category_index

    mouse_pos = pygame.mouse.get_pos() # Get mouse position outside the loop
    if event.type == pygame.MOUSEBUTTONDOWN: # Check for MOUSEBUTTONDOWN event within the loop
        if event.button == 1:
            for i in range(len(SHOP_CATEGORIES)):
                tab_rect = pygame.Rect(TAB_START_X + i * TAB_WIDTH, TAB_Y, TAB_WIDTH, TAB_HEIGHT)
                if tab_rect.collidepoint(mouse_pos):
                    print(f"Clicked on Tab: {SHOP_CATEGORIES[i]}")
                    current_shop_category_index = i
                    populate_shop_items()
            if BUTTON4_RECT.collidepoint(mouse_pos): 
                CURRENT_STATE = TOWN 
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
    pygame.draw.rect(screen, (100, 100, 100), BUTTON3_RECT)
    button_texts = BUTTON_TEXTS[DUNGEON]
    deeper_button_text = button_texts[2]
    deeper_text_surface = SMALL_FONT.render(deeper_button_text, True, WHITE)
    deeper_rect = deeper_text_surface.get_rect(center=BUTTON3_RECT.center)
    screen.blit(deeper_text_surface, deeper_rect)
    render_status_bar() # Status bar rendering (assumed to be at the bottom)
def handle_dungeon_events(events): # <--- Parameter is now 'events' (plural - list of events)
    global current_room_id, CURRENT_STATE,roomlvl

    mouse_pos = pygame.mouse.get_pos() # Get mouse position outside the loop

    for event in events: # <--- Add a loop to iterate through the list of events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if BUTTON1_RECT.collidepoint(mouse_pos):
                    print("Attack button clicked in Dungeon") # This will not be attack in future
                elif BUTTON2_RECT.collidepoint(mouse_pos):
                    print("Abilities button clicked in Dungeon") # This will not be abilities in future
                elif BUTTON3_RECT.collidepoint(mouse_pos):
                    print("Deeper button clicked")
                    current_room = rooms[current_room_id]
                    if current_room["content"] == "staircase_down":
                        descend_staircase()
                    else:
                        print("No staircase in this room.")
                        move()
                elif BUTTON4_RECT.collidepoint(mouse_pos):
                    roomlvl=0
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
        render_status_bar()
def handle_combat_events(events): # <--- Parameter is now 'events' (plural - list of events)
    global CURRENT_STATE, player_turn, current_enemy, combat_log_messages, ability_menu_open, roomlvl, player # <--- Make sure 'player' is global if needed in monster_turn

    mouse_pos = pygame.mouse.get_pos() # Get mouse position outside the loop
    for event in events: # <--- Add a loop to iterate through the list of events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button1_rect = BUTTON1_RECT
                button2_rect = BUTTON2_RECT
                button4_rect = BUTTON4_RECT
                # --- Check Button Clicks ---
                if button1_rect.collidepoint(mouse_pos): # Attack Button
                    if event.button == 1:
                        if player_turn and not ability_menu_open:
                            player.start_turn()
                            damage = player.attack(current_enemy)
                            if damage > 0:
                                combat_log_messages.append(f"You attack {current_enemy.get_name()} for {damage} damage!") # Log attack
                            else:
                                combat_log_messages.append("You missed!") # Log miss
                            player_turn = False
                            player.end_turn()
                            if current_enemy.is_alive():
                                # --- Monster Turn with Abilities --- START ---
                                if current_enemy.is_stunned():
                                    combat_log_messages.append(f"{current_enemy.get_name()} is stunned and cannot act.")
                                    current_enemy.update_buff_durations()
                                else:
                                    current_enemy.update_buff_durations()
                                    chosen_ability = current_enemy.choose_ability(player) # Monster chooses ability
                                    if chosen_ability:
                                        current_enemy.use_ability(chosen_ability, player) # Use ability (game_logic is None here for now)
                                        combat_log_messages.append("") # Add empty line for spacing in combat log
                                    else:
                                        damage = current_enemy.attack(player) # Normal attack if no ability chosen
                                        if damage > 0:
                                            combat_log_messages.append(f"{current_enemy.get_name()} attacks you for {damage} damage!") # Log enemy attack
                                        else:
                                            combat_log_messages.append(f"{current_enemy.get_name()} missed!") # Log enemy miss
                                # --- Monster Turn with Abilities --- END ---
                                player_turn = True # Give turn back to player (even if monster stunned or missed)
                            if player.current_health <= 0:
                                combat_log_messages.append("Player defeated!") # Log player defeat
                                CURRENT_STATE = GAME_OVER

                elif button2_rect.collidepoint(mouse_pos): # Abilities Button
                    if event.button == 1:
                        if player_turn:
                            player.start_turn() # <---- CALL PLAYER.START_TURN() AT THE BEGINNING OF PLAYER TURN!
                            ability_menu_open = not ability_menu_open
                            combat_log_messages.append(f"Ability Menu Toggled: {'Open' if ability_menu_open else 'Closed'}") # Log menu toggle

                elif BUTTON3_RECT.collidepoint(mouse_pos): # Items Button
                    if event.button == 1:
                        combat_log_messages.append("Items are not implemented yet!") # Log item attempt

                elif button4_rect.collidepoint(mouse_pos): # Run Button
                    if event.button == 1:
                        if player_turn and not ability_menu_open:
                            player.start_turn()
                            if random.random() < 0.4:
                                combat_log_messages.append("Player successfully ran away!") # Log run success
                                current_enemy = None
                                roomlvl=0 # Reset roomlvl on run success to test town transition
                                CURRENT_STATE = TOWN # Go to town on run success
                            else:
                                combat_log_messages.append("Run failed! Monster attacks.") # Log run failure
                                player_turn = False
                                player.end_turn()
                                if current_enemy.is_alive():
                                    # --- Monster Turn with Abilities --- START --- (same as in Attack button)
                                    if current_enemy.is_stunned():
                                        combat_log_messages.append(f"{current_enemy.get_name()} is stunned and cannot act.")
                                        current_enemy.update_buff_durations()
                                    else:
                                        current_enemy.update_buff_durations()
                                        chosen_ability = current_enemy.choose_ability(player) # Monster chooses ability
                                        if chosen_ability:
                                            current_enemy.use_ability(chosen_ability, player) # Use ability (game_logic is None here for now)
                                            combat_log_messages.append("") # Add empty line for spacing
                                        else:
                                            damage = current_enemy.attack(player) # Normal attack if no ability chosen
                                            if damage > 0:
                                                combat_log_messages.append(f"{current_enemy.get_name()} attacks you for {damage} damage!") # Log enemy attack
                                            else:
                                                combat_log_messages.append(f"{current_enemy.get_name()} missed!") # Log enemy miss
                                    # --- Monster Turn with Abilities --- END ---
                                    player_turn = True # Give turn back to player
                            if player.current_health <= 0:
                                combat_log_messages.append("Player defeated!") # Log player defeat
                                CURRENT_STATE = GAME_OVER

                # --- Ability Menu Click Handling (if menu is open) ---
                if ability_menu_open:
                    player.start_turn() # <---- CALL PLAYER.START_TURN() AT THE BEGINNING OF PLAYER TURN!
                    # --- Exit Button Click ---
                    menu_width = 400
                    menu_height=300
                    menu_x = (SCREEN_WIDTH - menu_width) // 2
                    menu_y=(SCREEN_HEIGHT-menu_height)//2
                    exit_button_width = 60
                    exit_button_x = menu_x + menu_width - exit_button_width - 10
                    exit_button_rect = pygame.Rect(exit_button_x, menu_y + 10, exit_button_width, 25)
                    if exit_button_rect.collidepoint(mouse_pos):
                        ability_menu_open = False
                        combat_log_messages.append("Ability Menu Closed via Exit Button") # Log menu close
                    else: # Check for clicks on ability buttons if not Exit button
                        ability_button_y_start = menu_y + 50
                        ability_button_spacing = 70
                        ability_button_width = menu_width - 40
                        ability_button_height = 60
                        player_class_name = player.class_name
                        if player_class_name in CLASS_ABILITIES:
                            abilities = CLASS_ABILITIES[player_class_name]
                            for i in range(min(4, len(abilities))): # Check up to 4 ability buttons
                                ability_button_rect = pygame.Rect(menu_x + 20, ability_button_y_start + i * ability_button_spacing, ability_button_width, ability_button_height)
                                if ability_button_rect.collidepoint(mouse_pos):
                                    ability = abilities[i]
                                    ability_name = ability["name"]
                                    use_ability(ability, player, current_enemy) # Player use ability function (already defined)
                                    combat_log_messages.append(f"You use {ability_name}!") # Log player ability use
                                    ability_menu_open = False
                                    player.end_turn()
                                    if current_enemy.is_alive():
                                        # --- Monster Turn with Abilities --- START --- (same as in Attack and Run button)
                                        if current_enemy.is_stunned():
                                            combat_log_messages.append(f"{current_enemy.get_name()} is stunned and cannot act.")
                                            current_enemy.update_buff_durations()
                                        else:
                                            current_enemy.update_buff_durations()
                                            chosen_ability = current_enemy.choose_ability(player) # Monster chooses ability
                                            if chosen_ability:
                                                current_enemy.use_ability(chosen_ability, player) # Use ability (game_logic is None here for now)
                                                combat_log_messages.append("") # Add empty line for spacing
                                            else:
                                                damage = current_enemy.attack(player) # Normal attack if no ability chosen
                                                if damage > 0:
                                                    combat_log_messages.append(f"{current_enemy.get_name()} attacks you for {damage} damage!") # Log enemy attack
                                                else:
                                                    combat_log_messages.append(f"{current_enemy.get_name()} missed!") # Log enemy miss
                                        # --- Monster Turn with Abilities --- END ---
                                        player_turn = True
                                    if player.current_health <= 0:
                                        combat_log_messages.append("Player defeated!") # Log player defeat
                                        CURRENT_STATE = GAME_OVER

        if current_enemy and not current_enemy.is_alive(): # Check for monster death AFTER player and monster turns
            player.gain_experience(current_enemy.get_experience())
            player.gain_coins(current_enemy.gold)
            combat_log_messages.append(f"You gained {current_enemy.get_experience()} XP and {current_enemy.gold} coins.") # Log rewards
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
    GAME_OVER:handle_game_over_events
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
    pygame.display.flip()
pygame.quit()