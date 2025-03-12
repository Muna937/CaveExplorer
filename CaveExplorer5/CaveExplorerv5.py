import pygame
import random
import json
import math
import os
import sys
import copy
import pytmx  # Import pytmx

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 30
VIRTUAL_WIDTH = 800 #Virtual resolution width
VIRTUAL_HEIGHT = 600 #Virtual resolution height

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
GOLD = (255, 215, 0)

# --- Game States ---
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_COMBAT = "combat"
STATE_INVENTORY = "inventory"
STATE_SHOP = "shop"  # TODO: Implement
STATE_TOWN = "town"
STATE_WORLD_MAP = "world_map"
STATE_GAME_OVER = "game_over"
STATE_TALENTS = "talents"  # TODO: Implement
STATE_QUESTS = "quests"    # TODO: Implement

# --- UI Proportions (Placeholders - adjust these!) ---
# Main Menu
MENU_TITLE_SCALE = 0.15
MENU_BUTTON_WIDTH_SCALE = 0.2
MENU_BUTTON_HEIGHT_SCALE = 0.08
MENU_BUTTON_SPACING_SCALE = 0.05
# Status Bar (In-Game)
STATUS_BAR_HEIGHT_SCALE = 0.1
STATUS_BAR_FONT_SCALE = 0.04
STATUS_BAR_PADDING_SCALE = 0.01
# Inventory/Shop
INVENTORY_WIDTH_SCALE = 0.4
INVENTORY_HEIGHT_SCALE = 0.7
INVENTORY_ITEM_SPACING_SCALE = 0.02
INVENTORY_FONT_SCALE = 0.03
SHOP_WIDTH_SCALE = 0.6  #Placeholder
SHOP_HEIGHT_SCALE = 0.8 #Placeholder
SHOP_ITEM_SPACING_SCALE = 0.025 #Placeholder
SHOP_FONT_SCALE = 0.035 #Placeholder
# Combat UI
COMBAT_LOG_WIDTH_SCALE = 0.3
COMBAT_LOG_HEIGHT_SCALE = 0.6
COMBAT_LOG_FONT_SCALE = 0.025
COMBAT_BUTTON_WIDTH_SCALE = 0.15 #Placeholder
COMBAT_BUTTON_HEIGHT_SCALE = 0.07 #Placeholder
# Font Sizes (General)
SMALL_FONT_SCALE = 0.02
MEDIUM_FONT_SCALE = 0.03
LARGE_FONT_SCALE = 0.05

# --- Directions ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Combat/Turn Order ---
TURN_PLAYER = "player"
TURN_ENEMY = "enemy"

# --- Image Paths (PLACEHOLDERS - REPLACE WITH YOUR ASSETS) ---
IMAGE_FLOOR = "assets/floor.png"
IMAGE_WALL = "assets/wall.png"
IMAGE_PLAYER = "assets/player.png"
IMAGE_MONSTER = "assets/monster.png"
IMAGE_TOWN_FLOOR = "assets/town_floor.png"  # New image for town floor
IMAGE_TOWN_WALL = "assets/town_wall.png"    # New image for town walls
IMAGE_NPC = "assets/npc.png"          # New image for NPCs
IMAGE_STAIRS_UP = "assets/stairs_up.png"  # Placeholder
IMAGE_STAIRS_DOWN = "assets/stairs_down.png"  # Placeholder
IMAGE_CHEST = "assets/chest.png" # Placeholder
IMAGE_DOOR = "assets/door.png" #Placeholder
IMAGE_GRASS = "assets/grass.png"

# --- Sound Paths (PLACEHOLDERS) ---
SOUND_FOOTSTEP = "assets/footstep.wav"  # Example
SOUND_SWORD_SWING = "assets/sword_swing.wav"  # Example
SOUND_GOLD = "assets/gold.wav"
MUSIC_TOWN = "assets/town_music.mp3"  # Example
MUSIC_DUNGEON = "assets/dungeon_music.mp3" # Example

# --- Data File Paths (PLACEHOLDERS) ---
DATA_FILE_ITEMS = "data/items.json"
DATA_FILE_MONSTERS = "data/monsters.json"
DATA_FILE_ABILITIES = "data/abilities.json"
DATA_FILE_QUESTS = "data/quests.json" #Placeholder
DATA_FILE_NPCS = "data/npcs.json"
DATA_FILE_TALENTS = "data/talents.json"
DATA_FILE_CLASSES = "data/classes.json"
DATA_FILE_WEAPONS = "data/weapons.json"
DATA_FILE_ARMOR = "data/armor.json"
DATA_FILE_DUNGEONS = "data/dungeons.json"
DATA_FILE_LEVEL_UP_STATS = "data/level_up_stats.json"
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "fullscreen": False,
    "resolution": [800, 600],
    "volume": 0.5
}

# --- Global Variables ---
combat_log = []
MAX_LOG_MESSAGES = 10
WEAPONS = {}
ARMOR = {}
ITEMS = {}
ABILITIES = {}
MONSTERS = {}
CLASSES = {}
LEVEL_UP_STATS = {}
DUNGEONS = {}
NPCS = {}
settings = {}
images = {} # Add images to prevent errors.

# --- Helper Functions ---

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  # Use current working directory if not an executable

    return os.path.join(base_path, relative_path)


def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def add_to_combat_log(message):
    global combat_log
    combat_log.append(message)
    if len(combat_log) > MAX_LOG_MESSAGES:
        combat_log.pop(0)

def render_combat_log(screen, combat_log, font):
    log_rect = pygame.Rect(
        SCREEN_WIDTH * (1- COMBAT_LOG_WIDTH_SCALE),
        0,
        SCREEN_WIDTH * COMBAT_LOG_WIDTH_SCALE,
        SCREEN_HEIGHT * COMBAT_LOG_HEIGHT_SCALE
    )
    pygame.draw.rect(screen, DARK_GREY, log_rect)

    y_offset = log_rect.top + STATUS_BAR_PADDING_SCALE * SCREEN_HEIGHT
    for i, message in enumerate(reversed(combat_log)):  # Display in reverse order (newest at the bottom)
        text_surface = font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(log_rect.left + STATUS_BAR_PADDING_SCALE * SCREEN_WIDTH, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_rect.height + STATUS_BAR_PADDING_SCALE * SCREEN_HEIGHT # Add a small vertical spacing

# --- Game Classes ---
class Entity(pygame.sprite.Sprite):  # Inherit from Sprite
    def __init__(self, name, x, y, stats, abilities, inventory=None):
        super().__init__()  # Call the Sprite's __init__ method!
        self.name = name
        self.x = x  # Grid coordinates (not pixel)
        self.y = y
        self.stats = stats  # Dictionary of base stats
        self.abilities = abilities
        self.inventory = inventory if inventory is not None else {}
        self.equipped_weapon = None  # Use None for no equipment
        self.equipped_armor = None   # Use None for no equipment
        self.buffs = []  # List of active buffs/debuffs
        self.image = None # Placeholder, will be set later.
        self.rect = None # Placeholder
        self.calculate_derived_stats() # Initial calculation



    def calculate_derived_stats(self):
        # Base stats (from self.stats)
        self.max_hp = self.stats["max_hp"]
        self.max_mana = self.stats["max_mana"]
        self.Strength = self.stats["Strength"]
        self.Agility = self.stats["Agility"]
        self.Intelligence = self.stats["Intelligence"]
        self.Wisdom = self.stats["Wisdom"]
        self.Dexterity = self.stats["Dexterity"]
        self.Luck = self.stats["Luck"]
        self.Charisma = self.stats["Charisma"]
        # Current HP and Mana (start at max)
        self.hp = self.max_hp
        self.mana = self.max_mana

        # Derived stats (calculated from base stats + equipment + buffs)
        self.attack_damage = self.Strength * 2 + (self.equipped_weapon.get("attack",0) if self.equipped_weapon else 0)
        self.defense = self.Agility * 1 + (self.equipped_armor.get("defense",0) if self.equipped_armor else 0)
        self.accuracy = self.Dexterity * 5
        self.evasion = self.Agility * 3 + self.Luck * 2
        self.crit_chance = self.Luck * 1
        self.crit_damage = 1.5 + (self.Dexterity * 0.01)
        self.initiative = self.Agility * 2 + self.Dexterity

        # Apply buffs/debuffs (after base calculations)
        for buff in self.buffs:
            if buff['stat'] == "attack_damage":
               self.attack_damage += buff['amount']
            if buff['stat'] == "defense":
                self.defense += buff["amount"]
            if buff["stat"] == "accuracy":
                self.accuracy += buff["amount"]
            if buff["stat"] == "evasion":
                self.evasion += buff['amount']
            if buff["stat"] == 'crit_chance':
                self.crit_chance += buff["amount"]
            if buff["stat"] == 'crit_damage':
                self.crit_damage += buff["amount"]

    def get_attack_damage(self):  # Example derived stat method
        return self.attack_damage

    def get_defense(self):
        return self.defense

    def get_accuracy(self):
        return self.accuracy
    def get_evasion(self):
        return self.evasion
    def get_crit_chance(self):
        return self.crit_chance
    def get_crit_damage(self):
        return self.crit_damage

    def get_initiative(self):
        return self.initiative


    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        if not self.is_alive() or not target.is_alive(): # Prevent dead attacking and attacking dead
            return

        damage = max(0, self.get_attack_damage() - target.get_defense())
        if random.randint(1, 100) <= (self.get_accuracy() - target.get_evasion()):
            if random.randint(1, 100) <= self.get_crit_chance():
                damage = int(damage * self.get_crit_damage())
                add_to_combat_log(f"{self.name} critically strikes {target.name} for {damage} damage!")
            else:
                add_to_combat_log(f"{self.name} attacks {target.name} for {damage} damage!")
            target.hp -= max(0, damage)  # Ensure damage isn't negative
        else:
            add_to_combat_log(f"{self.name} missed!")

        if target.hp < 0:
            target.hp = 0

    def use_ability(self, ability_name, target):
      if ability_name not in self.abilities:
            add_to_combat_log(f"You don't know the ability '{ability_name}'.")
            return

      ability = ABILITIES[ability_name]

      if self.mana < ability["mana_cost"]:
          add_to_combat_log(f"Not enough mana to use {ability_name}.")
          return

      self.mana -= ability["mana_cost"]

      if ability["type"] == "attack":
          if random.randint(1, 100) <= (self.get_accuracy() - target.get_evasion()):
              damage = int(self.get_attack_damage() * ability["power_multiplier"])
              if random.randint(1, 100) <= self.get_crit_chance():
                  damage = int(damage * self.get_crit_damage())
                  add_to_combat_log("Critical Hit!")
              damage = max(0, damage - target.get_defense())  # Ensure damage isn't negative
              target.hp -= damage
              add_to_combat_log(f"You use {ability_name} on {target.name} for {damage} damage!")
          else:
              add_to_combat_log(f"You use {ability_name} on {target.name}, but miss!")

      elif ability["type"] == "heal":
          target.hp = min(target.hp + ability["heal_amount"], target.max_hp)
          add_to_combat_log(f"You use {ability_name} and heal {target.name} for {ability['heal_amount']} health.")

      elif ability["type"] == "buff":
          self.buffs.append(
              {"stat": ability["stat"], "amount": ability["amount"], "duration": ability["duration"]}
          )
          add_to_combat_log(f"You use {ability_name}, increasing your {ability['stat']} by {ability['amount']} for {ability['duration']} turns.")
          # Apply the buff immediately
          self.calculate_derived_stats()

    def update_buffs(self):
        expired_buffs = []
        for buff in self.buffs:
            buff["duration"] -= 1
            if buff["duration"] <= 0:
                expired_buffs.append(buff)

        for buff in expired_buffs:
            self.buffs.remove(buff)
            add_to_combat_log(f"The buff on {buff['stat']} has expired.")
        self.calculate_derived_stats() # Recalculate

    def use_item(self, item_name, target):
      if item_name in self.inventory and self.inventory[item_name] > 0:
          item = ITEMS[item_name]
          if item["type"] == "consumable":
              if item["effect"] == "heal":
                  target.hp = min(target.hp + item["amount"], target.max_hp)
                  add_to_combat_log(f"{target.name} healed for {item['amount']} health.")
              elif item["effect"] == "restore_mana":
                  target.mana = min(target.mana + item["amount"], target.max_mana)
                  add_to_combat_log(f"{target.name} restored {item['amount']} mana.")

              self.inventory[item_name] -= 1
              if self.inventory[item_name] == 0:
                  del self.inventory[item_name]
          else:
              add_to_combat_log(f"{item_name} is not a consumable item.")
      else:
          add_to_combat_log(f"You don't have {item_name} in your inventory.")

    def equip_item(self, item_name):
        if item_name in self.inventory and self.inventory[item_name] > 0:
            item = None
            if item_name in WEAPONS:
                item = WEAPONS[item_name]
            elif item_name in ARMOR:
                item = ARMOR[item_name]

            if item:
                if item["type"] == "weapon":
                    if self.equipped_weapon:
                        self.unequip_item(self.equipped_weapon["name"])  # Unequip current
                    self.equipped_weapon = item
                    self.inventory[item_name] -= 1
                    if self.inventory[item_name] == 0:
                        del self.inventory[item_name]
                    self.calculate_derived_stats() # Recalc
                    add_to_combat_log(f"Equipped {item_name}.")
                    return  # Important: Return after equipping

                elif item["type"] == "armor":
                    if self.equipped_armor:
                        self.unequip_item(self.equipped_armor["name"])  # Unequip current
                    self.equipped_armor = item
                    self.inventory[item_name] -= 1
                    if self.inventory[item_name] == 0:
                        del self.inventory[item_name]
                    self.calculate_derived_stats() # Recalc
                    add_to_combat_log(f"Equipped {item_name}.")
                    return  # Important: Return after equipping

        add_to_combat_log(f"You don't have {item_name} in your inventory, or it's not equippable.") # Improved message
    def unequip_item(self, item_name):
        if self.equipped_weapon and self.equipped_weapon["name"] == item_name:
            # Check if the item already exists
            if item_name not in self.inventory:
                self.inventory[item_name] = 0
            self.inventory[item_name] += 1 # Add back to inventory
            self.equipped_weapon = None
            self.calculate_derived_stats()
            add_to_combat_log(f"Unequipped {item_name}.")

        elif self.equipped_armor and self.equipped_armor["name"] == item_name:
            if item_name not in self.inventory:
                self.inventory[item_name] = 0 # Create if not
            self.inventory[item_name] += 1
            self.equipped_armor = None
            self.calculate_derived_stats()
            add_to_combat_log(f"Unequipped {item_name}.")

        else:
            add_to_combat_log(f"You don't have {item_name} equipped.")

    def update(self):
        """Handles per-frame updates (for animation, AI, etc.)."""
        pass  # Replace with animation logic later (see next steps)

class Player(Entity):
    def __init__(self, name, x, y, player_class, stats, abilities, inventory=None):
        super().__init__(name, x, y, stats, abilities, inventory)
        self.player_class = player_class  # "Warrior", "Mage", etc.
        self.xp = 0
        self.level = 1
        self.talents = {}  # TODO: Implement talent system
        self.quests = []   # List of Quest objects
        self.active_quests = {} #For quest tracking.
        self.completed_quests = [] # Store completed quests.
        self.image = None # Will set after
        self.rect = None

    def level_up(self):
        while self.xp >= self.xp_needed(): # Loop for multiple level-ups
            self.xp -= self.xp_needed()
            self.level += 1
            add_to_combat_log(f"{self.name} leveled up to level {self.level}!")

            # Get stat increases from LEVEL_UP_STATS
            level_up_bonuses = LEVEL_UP_STATS.get(self.player_class, {})  # Default to {} if not found
            for stat, bonus in level_up_bonuses.items():
                self.stats[stat] = self.stats.get(stat, 0) + bonus  # Handle missing stats

            # Restore HP and MP on level up
            self.calculate_derived_stats() # Recalculate Max HP
            self.hp = self.max_hp
            self.mana = self.max_mana #Restore to max

            self.level_up()

    def xp_needed(self):
        return int(100 * (1.5 ** (self.level - 1)))  # Example formula

    def add_quest(self, quest_id, quest_data):
        # Prevent duplicate quests
        if quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests[quest_id] = quest_data.copy()  # Store a *copy*
            add_to_combat_log(f"New quest received: {quest_data['name']}")

    def check_quests(self):
        for player in self.members:
            for quest_id, quest in list(player.active_quests.items()):
                completed_all_objectives = True
                for objective in quest["objectives"]:
                    if objective["type"] == "kill":
                        if objective["current"] < objective["count"]:
                            completed_all_objectives = False
                            break  # No need to check further
                    # Add other objective types here (e.g., "collect", "talk", "location")

                if completed_all_objectives:
                    print(f"Quest '{quest['name']}' completed!")

                    # --- Give Rewards ---
                    player.xp += quest["rewards"]["xp"]
                    player.level_up()
                    self.add_to_inventory("Gold",quest['rewards']['gold']) # Party inventory
                    for item_name, quantity in quest["rewards"]["items"].items():
                         self.add_to_inventory(item_name, quantity)

                    # --- Move Quest to Completed List ---
                    player.completed_quests.append(quest_id)
                    del player.active_quests[quest_id]

    def learn_ability(self, ability_name):
        # TODO: Implement ability learning (e.g., from trainers, level up)
        pass

    def display_talents(self):
        # TODO: UI for spending talent points
        pass

    def use_talent(self, talent):
        # TODO: Logic for applying talent effects
        pass

class Monster(Entity):
    def __init__(self, name, x, y, stats, abilities, inventory, xp_reward, gold_reward, drops, width=1, height=1):
        super().__init__(name, x, y, stats, abilities, inventory)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.drops = drops  # List of (item_name, drop_chance) tuples
        self.width = width  # NEW: Monster width in tiles
        self.height = height # NEW: Monster height in tiles
        self.image = None #Set image later.
        self.rect = None

    # Add a method to get all occupied tile coordinates
    def occupied_tiles(self):
        tiles = []
        for row in range(self.y, self.y + self.height):
            for col in range(self.x, self.x + self.width):
                tiles.append((col,row))
        return tiles

    def choose_action(self, target): # Choose a course of action
        self.attack(target)
class Tile(pygame.sprite.Sprite):  # Base class for all tile types
    def __init__(self, tile_type, walkable, image=None, x=None, y=None):
        super().__init__() # Sprite init
        self.tile_type = tile_type  # e.g., "floor", "wall", "door"
        self.walkable = walkable  # True/False
        self.image = image  # pygame.Surface
        self.rect = None
        self.x = x # Tile Grid
        self.y = y
        self.explored = False  # Add explored here

    def is_walkable(self):
        return self.walkable

class DungeonTile(Tile):
    def __init__(self, tile_type, walkable, image=None, x=None, y=None):
        super().__init__(tile_type, walkable, image, x, y)
        self.enemies = []  # List to hold enemies on the tile
        self.explored = False
        self.visible = False  # For fog of war (optional)
        self.objects = []  # Added for chest and doors
        self._is_cleared = False


    def is_cleared(self):
        return self._is_cleared

    def set_cleared(self, cleared):
        self._is_cleared = cleared


    def interact(self, party, game_state):
       #Stairs Logic
        if self.tile_type == "stairs_up":
            if game_state.current_floor > 1:
                game_state.current_floor -= 1
                game_state.generate_floor()
                party.x, party.y = game_state.current_map.down_stair_location # Move party
                add_to_combat_log("You ascend the stairs.")
            else:
                add_to_combat_log("There is no way to go but down...") # Changed message.
        elif self.tile_type == "stairs_down":
            game_state.current_floor += 1
            game_state.generate_floor()
            party.x, party.y = game_state.current_map.up_stair_location # Move party
            add_to_combat_log("You descend the stairs.")
        #Chest Logic
        elif self.tile_type == "chest":
            add_to_combat_log("You open the chest!")
            for item_name, quantity in self.objects[0]["contents"].items():
                party.add_to_inventory(item_name, quantity)
                add_to_combat_log(f"You found {quantity} {item_name}(s)!")
            self.image = None # Change image
            self.walkable = True # Can now walk on the space.
            self.objects = [] # Empty
        #Door Logic
        elif self.tile_type == "door":
            add_to_combat_log("You open the door.")
            self.tile_type = "floor" # Change the tile
            self.image = images["floor"] # Change the image to floor.
            self.walkable = True # Can now walk here.

class TownTile(Tile):  # New TownTile class
    def __init__(self, tile_type, walkable, image=None, x= None, y=None):
        super().__init__(tile_type, walkable, image, x, y)
        self.npc = None  # Store an NPC object if one is present
        # Add any town-specific attributes here (e.g., shop type, etc.)

class WorldMapTile(Tile):
    def __init__(self, tile_type, walkable, image = None, x = None, y = None):
        super().__init__(tile_type, walkable, image, x, y)
        self.connected_dungeon = None # Add dungeons at this location.
        self.rect = None


    def add_connected_dungeon(self, dungeon_type):
      self.connected_dungeon = dungeon_type

class Dungeon:
    def __init__(self, width, height, tile_size=32):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.rooms = []  # List to store rooms (as Rect objects)
        self.tiles = self.generate_tiles()  # 2D list of Tile objects
        self.up_stair_location = None  # (x, y) tuple
        self.down_stair_location = None  # (x, y) tuple
        self.start_x = None #Starting position in dungeon
        self.start_y = None
        self.highest_floor=1

    def generate_tiles(self):
        # Initialize all tiles as walls
        tiles = [[DungeonTile("wall", False) for _ in range(self.width)] for _ in range(self.height)]

        # Create rooms
        self.rooms = []
        self.create_rooms(tiles)

        # Create corridors between rooms
        self.create_corridors(tiles)

        # Place stairs
        self.place_stairs(tiles)

        # Place objects (chests, etc.) - after rooms and corridors
        self.place_objects(tiles)


        return tiles

    def create_rooms(self, tiles):
        num_rooms = random.randint(5, 10)  # Adjust as desired
        for _ in range(num_rooms):
            w = random.randint(5, 10)  # Adjust room size range
            h = random.randint(5, 10)
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)
            new_room = pygame.Rect(x, y, w, h)

            # Check for overlap with existing rooms
            if not any(new_room.colliderect(other_room) for other_room in self.rooms):
                self.rooms.append(new_room)
                # Carve out the room
                for i in range(x, x + w):
                    for j in range(y, y + h):
                        tiles[j][i] = DungeonTile("floor", True)

    def create_corridors(self, tiles):
            #Connect all rooms with corridors.
        for i in range(len(self.rooms) - 1):
            room1 = self.rooms[i]
            room2 = self.rooms[i + 1]
            x1, y1 = room1.center
            x2, y2 = room2.center
            #Create L shaped corridors
            if random.randint(0, 1) == 0:
                # Horizontal first, then vertical
                self.create_h_corridor(tiles, x1, x2, y1)
                self.create_v_corridor(tiles, y1, y2, x2)
            else:
                # Vertical first, then horizontal
                self.create_v_corridor(tiles, y1, y2, x1)
                self.create_h_corridor(tiles, x1, x2, y2)

    def create_h_corridor(self, tiles, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles[y][x] = DungeonTile("floor", True)
            #Check for walls above or below
            if y > 0 and tiles[y-1][x].tile_type == "wall":
                tiles[y-1][x] = DungeonTile("door", False) # Add door
            if y < len(tiles) - 1 and tiles[y+1][x].tile_type == "wall":
                tiles[y+1][x] = DungeonTile("door", False) #Add door

    def create_v_corridor(self, tiles, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles[y][x] = DungeonTile("floor", True)
            # Check for walls on either side.
            if x > 0 and tiles[y][x-1].tile_type == "wall":
                tiles[y][x-1] = DungeonTile("door", False) # Add door.
            if x < len(tiles[0]) - 1 and tiles[y][x+1].tile_type == "wall":
                tiles[y][x+1] = DungeonTile("door", False) # Add door

    def place_stairs(self, tiles):
        # Place stairs up in the first room
        room1 = self.rooms[0]
        x1, y1 = room1.center
        tiles[y1][x1] = DungeonTile("stairs_up", True, x=x1, y=y1)  # Use the correct string for tile_type
        self.up_stair_location = (x1,y1)
        self.start_x = x1  # Set start_x to the stairs up location
        self.start_y = y1

    def place_objects(self, tiles):
        #Place object like chests and doors
        for room in self.rooms[1:]:
            if random.random() < 0.2:  # 20% chance of a chest
                x = random.randint(room.x + 1, room.x + room.width - 2)
                y = random.randint(room.y + 1, room.y + room.height - 2)
                if tiles[y][x].tile_type == 'floor': # Place chest on floor.
                    tiles[y][x] = DungeonTile("chest", False, x=x, y=y)  # Chests are not initially walkable
                    tiles[y][x].objects = [{"type": "chest", "contents": {"Gold": 10, "Health Potion": 1}}]  # Example contents

    def place_monsters(self, num_monsters):
        placed_monsters = 0
        while placed_monsters < num_monsters:
            room = random.choice(self.rooms[1:]) # Get random room

            # --- Choose a random size (example) ---
            monster_width = 1
            monster_height = 1
            if random.random() < 0.2:  # 20% chance of a larger monster
                monster_width = random.choice([2, 3])
                monster_height = random.choice([2, 3])

            # --- Find a valid placement spot ---
            start_x = random.randint(room.left + 1, room.right - monster_width - 1)
            start_y = random.randint(room.top + 1, room.bottom - monster_height - 1)

            valid_spot = True
            for y in range(start_y, start_y + monster_height):
                for x in range(start_x, start_x + monster_width):
                    if not self.tiles[y][x].is_walkable():
                        valid_spot = False # Invalid spot.
                        break # Inner loop
                if not valid_spot:
                    break # Outer loop

            if valid_spot:
                # Create the monster (using data from your MONSTERS dictionary)
                monster_data = random.choice(list(MONSTERS.values()))  # Choose a random monster type
                monster = Monster(
                    monster_data["name"],
                    start_x,
                    start_y,
                    {k: v for k, v in monster_data.items() if k not in ["name", "abilities", "drops", "inventory"]},  # Stats
                    monster_data["abilities"],
                    monster_data["inventory"],
                    monster_data["xp_reward"],
                    monster_data["gold_reward"],
                    monster_data["drops"],
                    monster_width,  # Pass width
                    monster_height  # Pass height
                )

                # --- Add the monster to *every* tile it occupies ---
                for y in range(start_y, start_y + monster_height):
                    for x in range(start_x, start_x + monster_width):
                        self.tiles[y][x].enemies.append(monster) # Add monster to tile.

                placed_monsters += 1

    def is_walkable(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        tile = self.tiles[y][x]
        if not tile.walkable:
            return False

        # Check if tile is blocked by an enemy
        if any(not enemy.is_alive() == False for enemy in tile.enemies): # Check to see if enemy is not alive.
            return False # Is blocked

        return True
    def interact_with_tile(self, x, y, party, game_state):
        tile = self.tiles[y][x]
        if isinstance(tile, DungeonTile): # Make sure its dungeon tile
            if tile.enemies:
                # Find living enemies.
                living_enemies = [enemy for enemy in tile.enemies if enemy.is_alive()]
                if living_enemies:
                    game_state.current_state = STATE_COMBAT # Enter combat
                    game_state.battle_map = BattleMap(10,8)
                    combat(party, living_enemies, game_state)  # Pass game_state for state changes
            else:
                tile.interact(party, game_state) # Chests, doors, stairs

class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.generate_tiles()
        self.start_x = 0  # Added starting x
        self.start_y = 0  # Added starting y
        self.npcs = [] # List to store npcs.


    def generate_tiles(self):
        # Simplest map: all grass
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if random.random() < 0.7:  # 70% chance of grass
                    tile = WorldMapTile("grass", True, x=x, y=y)  # Pass x and y
                    row.append(tile)
                elif random.random() < 0.2:  # 20% chance of trees
                    tile = WorldMapTile("trees", False, x=x, y=y)  # Not walkable
                    row.append(tile)
                else:  # 10% chance of mountains
                    tile = WorldMapTile("mountain", False, x=x, y=y)  # Not walkable
                    row.append(tile)
            tiles.append(row)
        return tiles


    def is_walkable(self, x, y):
        # Simple bounds check and walkability of the tile
        return 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x].is_walkable()

    def interact_with_tile(self, x, y, party, game_state):
        tile = self.tiles[y][x]
        if tile.tile_type.startswith("dungeon_entrance_"):
            dungeon_type = tile.tile_type.split("_")[-1]  # Extract "forest", "ice", etc.
            game_state.enter_dungeon(dungeon_type)
        elif tile.tile_type == "town":
            game_state.enter_town("Starter Town") # Example town name.

    def add_town(self, x, y, town_name):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = WorldMapTile("town", True, x=x, y=y)  # Pass x and y
            print(f"Added town '{town_name}' at ({x}, {y})")
        else:
            print(f"Invalid coordinates for town: ({x}, {y})")

    def add_dungeon_entrance(self, x, y, dungeon_type):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = WorldMapTile(f"dungeon_entrance_{dungeon_type}", True, x=x, y=y)
            self.tiles[y][x].add_connected_dungeon(dungeon_type)
            print(f"Added dungeon entrance of type '{dungeon_type}' at ({x}, {y})")
        else:
            print(f"Invalid coordinates for dungeon entrance: ({x}, {y})")

class Town:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.tiles = self.generate_tiles()
        self.npcs = self.place_npcs()  # List of NPCs
        self.entrance_location = (width // 2, height - 2) # Example
        self.start_x = width // 2 # Start x
        self.start_y = height - 2 # Start y


    def generate_tiles(self):
        # Simple town layout: floor with a border of walls.
        tiles = [[TownTile("town_floor", True, x=x, y=y) for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            tiles[0][x] = TownTile("town_wall", False, x=x, y=0)
            tiles[self.height - 1][x] = TownTile("town_wall", False, x=x, y=self.height - 1)
        for y in range(self.height):
            tiles[y][0] = TownTile("town_wall", False, x=0, y=y)
            tiles[y][self.width - 1] = TownTile("town_wall", False, x=self.width-1, y=y)
        return tiles

    def place_npcs(self):
        npcs = []
        # Example NPC placement (using data from DATA_FILE_NPCS):
        for npc_data in NPCS.values():
            npc = NPC(
                npc_data["name"],
                npc_data["x"],
                npc_data["y"],
                npc_data["dialogue"],
                {
                    quest_id: Quest(  # Create Quest objects
                        quest_data["name"],
                        quest_data["description"],
                        quest_data["objectives"],
                        quest_data["rewards"],
                    )
                    for quest_id, quest_data in npc_data.get("quests", {}).items()
                },
            )
            npcs.append(npc)
            # Add NPC to the tile
            self.tiles[npc.y][npc.x].npc = npc # Add npc
        return npcs

    def is_walkable(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x].is_walkable()

    def interact_with_tile(self, x, y, party, game_state):
        tile = self.tiles[y][x]
        if tile.npc:
            tile.npc.talk(party)  # Pass the party to the NPC's talk method

class NPC:
    def __init__(self, name, x, y, dialogue, quests=None):
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = dialogue
        self.quests = quests if quests is not None else {}  # Dictionary of quest_id: Quest object
        self.image = None  # Load in game loop
        self.rect = None

    def talk(self, party):
        print(f"{self.name}: {self.dialogue}")  # Simple dialogue for now
        # Check if the NPC has quests to offer, and offer them *one at a time*:
        for quest_id, quest in self.quests.items():
            if quest_id not in [q.name for q in party.members[0].quests] and not quest.completed:
                party.members[0].add_quest(quest_id, quest) # Pass id and data
                break  # Only give one quest at a time

class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of objective dictionaries
        self.rewards = rewards  # Dictionary of rewards (xp, gold, items)
        self.completed = False

    def check_completion(self, player):
        if self.completed:  # Already complete
            return

        all_objectives_complete = True
        for objective in self.objectives:
            if objective["type"] == "kill":
                if objective["current"] < objective["count"]:
                    all_objectives_complete = False
                    break  # No need to check further
            # Add other objective types here (e.g., "collect", "talk", "location")

        if all_objectives_complete:
            self.completed = True
            add_to_combat_log(f"Quest completed: {self.name}!")
            # Grant rewards
            player.xp += self.rewards.get("xp", 0)
            player.level_up()
            # Add gold to the player
            if "gold" in self.rewards:
                if "Gold" in player.inventory:
                    player.inventory['Gold'] += self.rewards["gold"]
                else:
                    player.inventory['Gold'] = self.rewards['gold']

            for item_name, quantity in self.rewards.get("items", {}).items():
                if item_name in player.inventory:
                    player.inventory[item_name] += quantity
                else:
                    player.inventory[item_name] = quantity
                add_to_combat_log(f"Received {quantity} x {item_name}")

class BattleMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.generate_tiles()

    def generate_tiles(self):
        # Simple battle map: all floor
        return [[Tile("floor", True) for _ in range(self.width)] for _ in range(self.height)]

    def is_walkable(self, x, y):
        # Simple bounds check
        return 0 <= x < self.width and 0 <= y < self.height

    def place_entity(self, entity, x, y):
        entity.x = x
        entity.y = y
        entity.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

    def get_tile(self, x, y):
        if 0<= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

class Party:
    def __init__(self, members, x, y):
        self.members = members
        self.x = x
        self.y = y
        self.inventory = {"Gold": 0}  # Shared inventory

    def add_to_inventory(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        add_to_combat_log(f"Added {quantity} x {item_name} to party inventory.")


    def remove_from_inventory(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name] # Delete
            add_to_combat_log(f"Removed {quantity} x {item_name} from the party inventory")

    def is_alive(self):
        return any(member.is_alive() for member in self.members)

    def move(self, dx, dy, dungeon, game_state):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < dungeon.width and 0 <= new_y < dungeon.height:
            if dungeon.is_walkable(new_x, new_y):
                self.x = new_x
                self.y = new_y
                # --- RANDOM ENCOUNTER CHECK (AFTER successful move) ---
                if isinstance(dungeon, Dungeon):  # Only in dungeons
                    if random.random() < 0.1:  # 10% chance of encounter per step
                        add_to_combat_log("A monster appears!")
                        self.start_random_encounter(game_state, dungeon)
                        return # Important, exit out of the function after starting.
                # --- END RANDOM ENCOUNTER CHECK ---
                # Check for interaction *after* moving
                if isinstance(dungeon, WorldMap):  # Check if it's the world map
                    dungeon.interact_with_tile(new_x, new_y, self, game_state)
                elif isinstance(dungeon, Dungeon): # Check if its a dungeon
                    dungeon.interact_with_tile(new_x, new_y, self, game_state)
                elif isinstance(dungeon, Town): # Check if town
                    dungeon.interact_with_tile(new_x, new_y, self, game_state)
                return True  # Movement successful
            else:
                add_to_combat_log("You can't move there.")
                return False
        else:
            add_to_combat_log("You can't go that way.")
            return False
    
    def update_all_buffs(self): # Update all party members buffs
        for member in self.members:
            member.update_buffs()
    def check_quests(self):
        for member in self.members:
            for quest_id, quest in list(member.active_quests.items()):
                completed_all_objectives = True
                for objective in quest["objectives"]:
                    if objective["type"] == "kill":
                        if objective["current"] < objective["count"]:
                            completed_all_objectives = False
                            break  # No need to check further
                    # Add other objective types here (e.g., "collect", "talk", "location")

                if completed_all_objectives:
                    print(f"Quest '{quest['name']}' completed!")

                    # --- Give Rewards ---
                    member.xp += quest["rewards"]["xp"]
                    member.level_up()
                    self.add_to_inventory("Gold",quest['rewards']['gold']) # Party inventory
                    for item_name, quantity in quest["rewards"]["items"].items():
                         self.add_to_inventory(item_name, quantity)
                         # --- Move Quest to Completed List ---
                    member.completed_quests.append(quest_id)
                    del member.active_quests[quest_id]
class Shop:  # TODO: Implement Shop class
    def __init__(self, name, inventory):
        # TODO
        pass
    # Add methods for buying/selling, displaying inventory, etc.

class GameState:
    def __init__(self):
        self.party = None # The player's party
        self.current_map = None # WorldMap, Dungeon, or Town
        self.current_floor = 1 # Current dungeon floor.
        self.current_state = STATE_MENU  # Start at the main menu
        self.battle_map = None  # For combat
        self.world_map = None # Ensure world map is created.


    def _load_json_data(self, filepath, data_dict):
        """Helper function to load JSON data and print debug info."""
        print(f"Loading data from: {resource_path(filepath)}")
        try:
            with open(resource_path(filepath), "r") as f:
                data_dict.update(json.load(f))  # Use update to merge
            print(f"Data: {data_dict}")  # Debug print
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {filepath}: {e}")
            sys.exit(1)

    def initialize_game(self):
        """Loads game data, creates the player, and sets up the initial game state."""
        global WEAPONS, ARMOR, ITEMS, MONSTERS, ABILITIES, CLASSES, LEVEL_UP_STATS, NPCS, DUNGEONS

        # --- Load JSON data ---
        self._load_json_data(DATA_FILE_WEAPONS, WEAPONS)
        self._load_json_data(DATA_FILE_ARMOR, ARMOR)
        self._load_json_data(DATA_FILE_ITEMS, ITEMS)
        self._load_json_data(DATA_FILE_ABILITIES, ABILITIES)
        self._load_json_data(DATA_FILE_MONSTERS, MONSTERS)
        self._load_json_data(DATA_FILE_CLASSES, CLASSES)
        self._load_json_data(DATA_FILE_LEVEL_UP_STATS, LEVEL_UP_STATS)
        self._load_json_data(DATA_FILE_NPCS, NPCS)
        self._load_json_data(DATA_FILE_DUNGEONS, DUNGEONS)

        # --- World, Dungeon, and Town Creation ---
        #Start on the world map.
        self.current_map = load_tiled_map("data/maps/world_map.tmx", self)
        self.current_state = STATE_GAME

        # --- Player and Party Creation ---
        player1 = Player("Warrior", 0, 0, "Warrior", CLASSES["Warrior"]["stats"], CLASSES["Warrior"]["abilities"], CLASSES["Warrior"]["inventory"])
        player2 = Player("Mage", 0, 0, "Mage", CLASSES["Mage"]["stats"], CLASSES["Mage"]["abilities"], CLASSES["Mage"]["inventory"])
        self.party = Party([player1, player2],x=self.current_map.start_x, y=self.current_map.start_y) # Create and place

        # --- Placeholder for save/load system ---
        self.save_file = "savegame.json"

    def generate_floor(self):
        # Select the dungeon to load from
        dungeon_type = "forest" # Add to the dungeon types
        difficulty = "easy"  # TODO: Implement difficulty selection
        floor_num = self.current_floor

        possible_maps = DUNGEONS.get(dungeon_type, {}).get(difficulty, [])
        #If we cannot find maps exit the function.
        if not possible_maps:
            print(f"Error: No maps found for dungeon type '{dungeon_type}', difficulty '{difficulty}'")
            return

        #Select map file, and map path.
        map_file = random.choice(possible_maps)
        map_path = os.path.join("data", "maps", "dungeons", map_file)

        if map_file == "world_map.tmx": # If the map file is the world map.
                map_path = os.path.join("data","maps", map_file) # Set correct path
                self.current_map = load_tiled_map(map_path, self)  # Load the Tiled map!
                self.current_state = STATE_GAME
                # Find town and set to be outside.
                for y, row in enumerate(self.current_map.tiles):
                    for x, tile in enumerate(row):
                        if tile.tile_type == "town":
                            self.party.x = x
                            self.party.y = y
                            break  # Only need to find one town (for now)
                    else:
                        continue  # Only executed if the inner loop did NOT break
                    break  # Only executed if the inner loop DID break
                add_to_combat_log("You have returned to the overworld")
                self.current_floor = 1 # Reset
        else:
            self.current_map = load_tiled_map(map_path, self)
            #Going down a floor logic.
            if floor_num > self.current_map.highest_floor:
                self.party.x, self.party.y = self.current_map.up_stair_location
                self.current_map.highest_floor = floor_num
            #Going up a floor
            else:
                 self.party.x, self.party.y = self.current_map.down_stair_location # Move party
            add_to_combat_log(f"Entering floor {self.current_floor} of {dungeon_type} dungeon.")

    def enter_dungeon(self, dungeon_type):
        # Choose a random map file based on type, difficulty (easy for now), and floor.
        difficulty = "easy"  # TODO: Implement difficulty selection
        floor_num = self.current_floor
        possible_maps = DUNGEONS.get(dungeon_type, {}).get(difficulty, [])

        if not possible_maps:
            print(f"Error: No maps found for dungeon type '{dungeon_type}', difficulty '{difficulty}'")
            return  # Or raise an exception, or generate a default map

        map_file = random.choice(possible_maps)
        map_path = os.path.join("data", "maps", "dungeons", map_file) #Added map path
        print(f"Loading dungeon map: {map_path}")  # Debug print
        self.current_map = load_tiled_map(map_path, self)  # Load the Tiled map!
        self.current_state = STATE_GAME

        # Place the player at the entrance of the dungeon (stairs up)
        self.party.x = self.current_map.up_stair_location[0]
        self.party.y = self.current_map.up_stair_location[1]
        print(f"Entering dungeon: {dungeon_type}, floor {floor_num}, map: {map_file}")


    def next_floor(self):
        # Go to next floor (or previous, for stairs up).
        # This is a simplified example; you'll need to handle going back to the
        # world map, etc.
        self.current_floor += 1
        dungeon_type = "forest"  # Replace with actual dungeon type
        difficulty = "easy"  # Replace with actual difficulty
        map_files = DUNGEONS.get(dungeon_type, {}).get(difficulty, [])

        if not map_files:
            print("No more floors!")
            return

        map_file = random.choice(map_files)
        map_path = os.path.join("data","maps", "dungeons", map_file)
        self.current_map = load_tiled_map(map_path, self)
        self.party.x, self.party.y = self.current_map.up_stair_location
        add_to_combat_log(f"Entering floor {self.current_floor} of {dungeon_type} dungeon.")
    def enter_town(self, town_name):
        map_path = os.path.join("data","maps", "town_map.tmx") # Load town
        self.current_map = load_tiled_map(map_path, self)
        self.current_state = STATE_TOWN # Change state
        self.party.x, self.party.y = self.current_map.entrance_location # Move to entrance

    def generate_town(self, town_name):
       # Town loaded from tiled.
       pass
    def save_game(self, filename="savegame.json"):
        """Saves the current game state to a JSON file."""
        data = {
            "current_state": self.current_state,
            "current_map_type": None,  # We'll determine this below
            "world_map": {  # Save world map data
                "width": self.world_map.width,
                "height": self.world_map.height,
                "tiles": [[tile.tile_type for tile in row] for row in self.world_map.tiles]
            },
            "current_floor": self.current_floor,
            "party": {
                "members": [
                    {
                        "name": member.name,
                        "x": member.x,
                        "y": member.y,
                        "player_class": member.player_class,
                        "stats": member.stats,
                        "abilities": member.abilities,
                        "inventory": member.inventory,  # Save inventory
                        "equipped_weapon": member.equipped_weapon,  # Save equipment
                        "equipped_armor": member.equipped_armor,  # Save equipment
                        "level": member.level, #Save Level
                        "xp": member.xp, # Save exp
                        "buffs": member.buffs, # Save buffs
                        "active_quests": member.active_quests,
                        "completed_quests": member.completed_quests
                    }
                    for member in self.party.members
                ],
                "x": self.party.x,
                "y": self.party.y,
                "inventory": self.party.inventory, #Save party inventory
            },

        }
        # Handle the current map differently depending on type
        if isinstance(self.current_map, Dungeon):
            data["current_map_type"] = "dungeon"
            data["dungeon"] = {
                "width": self.current_map.width,
                "height": self.current_map.height,
                "tiles": [[(tile.tile_type, tile.is_walkable()) for tile in row] for row in self.current_map.tiles],
                 "enemies": [  # Save enemy data
                    [
                        {
                            "name": enemy.name,
                            "x": enemy.x,
                            "y": enemy.y,
                            "stats": enemy.stats,
                            "abilities" : enemy.abilities,
                            "inventory": enemy.inventory,
                            "drops": enemy.drops,
                            "xp_reward": enemy.xp_reward,
                            "gold_reward": enemy.gold_reward,
                            "width": enemy.width,
                            "height": enemy.height,
                            "current_hp": enemy.hp, # Save status
                            "current_mana": enemy.mana

                        }
                        for enemy in tile.enemies
                    ] if hasattr(tile, "enemies") else []  # Handle empty enemy lists
                    for row in self.current_map.tiles for tile in row],
                "start_x": self.current_map.start_x,
                "start_y": self.current_map.start_y,
                "up_stair_location": self.current_map.up_stair_location,
                "down_stair_location": self.current_map.down_stair_location,
                "rooms": [
                    {
                        "x" : room.x,
                        "y" : room.y,
                        "width" : room.width,
                        "height" : room.height
                    }
                    for room in self.current_map.rooms
                ]

            }
        elif isinstance(self.current_map, WorldMap):
            data["current_map_type"] = "world"
            data["world_map"] = { # Save world map data
                "width": self.world_map.width,
                "height": self.world_map.height,
                "tiles": [[(tile.tile_type, tile.is_walkable())  for tile in row] for row in self.world_map.tiles]
            }

        elif isinstance(self.current_map, Town):
            data["current_map_type"] = "town"
            data["town"] = {
                "width": self.current_map.width,
                "height": self.current_map.height,
                "name" : self.current_map.name,
                "tiles": [[(tile.tile_type, tile.is_walkable()) for tile in row] for row in self.current_map.tiles],
                "npcs" : [
                    {
                        "name" : npc.name,
                        "x" : npc.x,
                        "y" : npc.y,
                        "dialogue" : npc.dialogue,
                        "quests" : npc.quests
                    }
                    for npc in self.current_map.npcs
                ],
                "start_x": self.current_map.start_x,  # Save start position
                "start_y": self.current_map.start_y,  # Save start position
                "entrance_location" : self.current_map.entrance_location
            }

        try:
            with open(resource_path(self.save_file), "w") as f:
                json.dump(data, f, indent=4)  # Use indent for readability
            print(f"Game saved to {self.save_file}")
        except Exception as e:
            print(f"Error saving game: {e}")
            add_to_combat_log(f"Error saving game.")

    def load_game(self, filename="savegame.json"):
        """Loads the game state from a JSON file."""
        global CLASSES, WEAPONS, ARMOR, ITEMS, ABILITIES, MONSTERS, NPCS, DUNGEONS
        try:
            with open(resource_path(filename), "r") as f:
                data = json.load(f)

            # --- Load party ---
            members_data = data["party"]["members"]
            members = []
            for member_data in members_data:
                # Recreate Player objects, handling potential missing keys gracefully
                player = Player(
                    member_data.get("name", "Unnamed"),  # Provide defaults
                    member_data.get("x", 0),
                    member_data.get("y", 0),
                    member_data.get("player_class", "Warrior"),  # Default to Warrior
                    member_data.get("stats", {}),  # Default to empty dict
                    member_data.get("abilities", []),  # Default to empty list
                    member_data.get("inventory", {}),  # Default to empty dict
                )
                player.hp = member_data.get("current_hp", player.stats.get('max_hp',100))
                player.mana = member_data.get("current_mana",player.stats.get('max_mana',20))
                player.level = member_data.get("level", 1)
                player.xp = member_data.get("xp",0)
                player.equipped_weapon = member_data.get("equipped_weapon")
                player.equipped_armor = member_data.get("equipped_armor")
                player.buffs = member_data.get("buffs")
                # --- Load Quests ---
                player.active_quests = member_data.get("active_quests", {})
                player.completed_quests = member_data.get("completed_quests",[])

                members.append(player)

            self.party = Party(members, data["party"]["x"], data["party"]["y"])
            self.party.inventory = data["party"]["inventory"]


            # --- Load Map ---
            map_type = data["current_map_type"]
            if map_type == "dungeon":
                self.current_map = load_tiled_map(data['current_map'], self) # Load map
                self.current_floor = data["current_floor"]

            elif map_type == "world":
                self.current_map = load_tiled_map(data['current_map'], self)

            elif map_type == "town":
                self.current_map = load_tiled_map(data["current_map"], self)


            # --- Load Overall Game State ---
            self.current_state = data["current_state"]

            print("Game loaded successfully.")

        except FileNotFoundError:
            print(f"No save file found: {self.save_file}")
        except Exception as e:
            print(f"Error loading game: {e}")

# --- UI Functions ---
def create_button_rect(screen, scale_width, scale_height, x_pos_scale, y_pos_scale):
    """Creates a centered button rectangle based on screen size and scaling factors."""
    button_width = screen.get_width() * scale_width
    button_height = screen.get_height() * scale_height
    x_pos = screen.get_width() * x_pos_scale - button_width / 2
    y_pos = screen.get_height() * y_pos_scale - button_height / 2
    return pygame.Rect(x_pos, y_pos, button_width, button_height)

def draw_menu(screen, title, button_texts, button_rects, title_font, button_font, selected_button_index):
    """Draws a generic menu on the screen."""

    # Fill background
    screen.fill(BLACK)

    # Render and display title
    title_surface = title_font.render(title, True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * MENU_TITLE_SCALE))
    screen.blit(title_surface, title_rect)

    # Render and display buttons
    for i, (text, rect) in enumerate(zip(button_texts, button_rects)):
        color = WHITE
        if i == selected_button_index:
            color = YELLOW  # Highlight selected button

        pygame.draw.rect(screen, color, rect, 2)  # Draw button border
        text_surface = button_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

def handle_menu_input(event, current_index, num_buttons):
    """Handles keyboard input for menu navigation."""
    new_index = current_index
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            new_index = (current_index - 1) % num_buttons
        elif event.key == pygame.K_DOWN:
            new_index = (current_index + 1) % num_buttons
        elif event.key == pygame.K_RETURN:
            return "select", new_index  # Signal that a button was selected
    return None, new_index  # No selection made

def draw_status_bar(screen, party, font):
    """Draws the status bar at the top of the screen."""
    bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, STATUS_BAR_HEIGHT_SCALE * SCREEN_HEIGHT)
    pygame.draw.rect(screen, DARK_GREY, bar_rect)

    x_offset = STATUS_BAR_PADDING_SCALE * SCREEN_WIDTH
    for i, member in enumerate(party.members):
        # Name
        name_surface = font.render(member.name, True, WHITE)
        name_rect = name_surface.get_rect(topleft=(x_offset, STATUS_BAR_PADDING_SCALE * SCREEN_HEIGHT))
        screen.blit(name_surface, name_rect)

        # HP
        hp_text = f"HP: {member.hp}/{member.max_hp}"
        hp_surface = font.render(hp_text, True, RED)  # Red for HP
        hp_rect = hp_surface.get_rect(topleft=(x_offset, name_rect.bottom + STATUS_BAR_PADDING_SCALE * SCREEN_HEIGHT))
        screen.blit(hp_surface, hp_rect)

        # Mana
        mana_text = f"Mana: {member.mana}/{member.max_mana}"
        mana_surface = font.render(mana_text, True, BLUE)  # Blue for Mana
        mana_rect = mana_surface.get_rect(topleft=(x_offset, hp_rect.bottom + STATUS_BAR_PADDING_SCALE * SCREEN_HEIGHT))
        screen.blit(mana_surface, mana_rect)

        x_offset += SCREEN_WIDTH / 4  # Adjust spacing between party members

def draw_inventory(screen, party, font):
    """Draws the inventory screen."""
    inventory_rect = pygame.Rect(
        SCREEN_WIDTH * (1 - INVENTORY_WIDTH_SCALE),  # Adjusted for right side
        SCREEN_HEIGHT * (1- INVENTORY_HEIGHT_SCALE),
        SCREEN_WIDTH * INVENTORY_WIDTH_SCALE,
        SCREEN_HEIGHT * INVENTORY_HEIGHT_SCALE
    )
    pygame.draw.rect(screen, DARK_GREY, inventory_rect)

    title_surface = font.render("Inventory", True, WHITE)
    title_rect = title_surface.get_rect(topleft=(inventory_rect.left + INVENTORY_ITEM_SPACING_SCALE*SCREEN_WIDTH, inventory_rect.top + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT))
    screen.blit(title_surface, title_rect)

    y_offset = title_rect.bottom + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT # Add Spacing

    for item_name, quantity in party.inventory.items():
        item_text = f"{item_name}: {quantity}"
        item_surface = font.render(item_text, True, WHITE)
        item_rect = item_surface.get_rect(topleft=(inventory_rect.left + INVENTORY_ITEM_SPACING_SCALE * SCREEN_WIDTH, y_offset))
        screen.blit(item_surface, item_rect)
        y_offset += item_rect.height + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT  # Add a small vertical spacing

def draw_player(screen, x, y):
    """Draws the player character (simplified)."""
    player_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)  # Use a color for now

# --- Combat Functions ---

def combat(party, enemies, game_state):
    """Handles the combat sequence."""
    global combat_log
    combat_log = []  # Clear the combat log at the start of each battle

    all_participants = party.members + enemies
    all_participants.sort(key=lambda entity: entity.get_initiative(), reverse=True)

    current_turn_index = 0
    current_turn = TURN_PLAYER if isinstance(all_participants[current_turn_index], Player) else TURN_ENEMY

    add_to_combat_log("Combat started!")

    battle_over = False

    while not battle_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Example: Press 'Esc' to attempt to flee
                if event.key == pygame.K_ESCAPE:
                    # Implement your escape/flee logic here.  For now, let's
                    # just go back to the game.  You'd want a check for success/failure.
                    add_to_combat_log("Attempted to flee...")
                    game_state.current_state = STATE_GAME # Back to exploration.
                    return  # Exit the combat loop

        # --- 1. Determine Turn Order (already done at the start) ---

        # --- 2. Current Entity's Turn ---
        current_entity = all_participants[current_turn_index]

        if current_turn == TURN_PLAYER:
            # Player Turn:  This is where your combat UI will go.
            # For this basic version, we'll just auto-attack the first enemy.
            if isinstance(current_entity, Player): # Double check.
                target = next((enemy for enemy in enemies if enemy.is_alive()), None)  # Find first alive enemy
                if target:
                     current_entity.attack(target) # Auto Attack
                else: # No enemies left
                    battle_over = True

        elif current_turn == TURN_ENEMY:
            # Enemy Turn (Simplified AI)
            if isinstance(current_entity, Monster):  # Double-check type
                target = next((member for member in party.members if member.is_alive()), None) # Find first alive.
                if target: # Check for targets
                    current_entity.choose_action(target) # Choose action.
                else: # If no players are left
                    battle_over = True # End battle

        # --- 3. Check for End of Combat ---
        if not any(enemy.is_alive() for enemy in enemies): # Check if all dead.
            add_to_combat_log("All enemies defeated!")
            # --- Rewards ---
            total_xp = sum(enemy.xp_reward for enemy in enemies)
            total_gold = sum(enemy.gold_reward for enemy in enemies)
            add_to_combat_log(f"Gained {total_xp} XP and {total_gold} gold.")
            for player in party.members:
                player.xp += total_xp
                player.level_up() # Check if player levels up
            # Add gold to the party's inventory (assuming a shared inventory)
            if 'Gold' in party.inventory:
                party.inventory['Gold'] += total_gold
            else:
                party.inventory['Gold'] = total_gold

            # --- Item Drops ---
            for enemy in enemies:  # Iterate through *all* enemies (even dead ones)
                for item_name, drop_chance in enemy.drops:
                    if random.random() <= drop_chance:
                        party.add_to_inventory(item_name, 1)  # Add to inventory
                        add_to_combat_log(f"Dropped {item_name}!")

            battle_over = True  # Combat ends
            game_state.current_state = STATE_GAME # Back to the game
            # --- Check for Quests ---
            party.check_quests() # Check Quests

        elif not any(member.is_alive() for member in party.members): # Check party
            add_to_combat_log("Party defeated!")
            battle_over = True
            game_state.current_state = STATE_GAME_OVER # To game over state

        # --- 4. Advance Turn ---
        if not battle_over: # Check again
            party.update_all_buffs() # Update buffs between turns
            current_turn_index = (current_turn_index + 1) % len(all_participants)
            current_turn = TURN_PLAYER if isinstance(all_participants[current_turn_index], Player) else TURN_ENEMY

def load_tiled_map(filename, game_state):
    """Loads a Tiled map (.tmx) file and creates the appropriate Map object."""
    tmx_data = pytmx.util_pygame.load_pygame(resource_path(filename), pixelalpha=True)
    map_width = tmx_data.width
    map_height = tmx_data.height

    # Determine the map type based on the filename or some other property
    if "world_map" in filename:
        tile_class = WorldMapTile
        new_map = WorldMap(map_width, map_height)  # Pass width and height
    elif "town" in filename:
        tile_class = TownTile
        new_map = Town(map_width, map_height, "town")  # Pass width and height, and a name
    else:
        tile_class = DungeonTile
        new_map = Dungeon(map_width, map_height)  # Pass width and height

    # --- Iterate through layers and tiles ---
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                if tile_properties:
                    # --- Tile Type and Walkability ---
                    tile_type = tile_properties.get('type', 'floor')  # Default to 'floor'
                    walkable = tile_properties.get('walkable', True)  # Default to walkable

                    # --- Create the correct Tile subclass ---
                    #Pass the map type to correctly determine which tile.
                    if isinstance(new_map, Dungeon):
                        tile = DungeonTile(tile_type, walkable, x=x, y=y) # Pass x and y
                        #Stair interaction:
                        if tile_type == "stairs_up":
                            new_map.up_stair_location = (x,y)
                        if tile_type == 'stairs_down':
                            new_map.down_stair_location = (x,y)
                    elif isinstance(new_map, WorldMap):
                        tile = WorldMapTile(tile_type, walkable, x=x, y=y) #Pass x and y
                    elif isinstance(new_map, Town):
                        tile = TownTile(tile_type, walkable, x=x, y=y) # Pass x and y

                    # --- Image --- Get image here.
                    image = tmx_data.get_tile_image_by_gid(gid)
                    if image:
                        tile.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                    tile.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    # --- Add to the map's tiles ---
                    # Ensure that the tiles list is large enough. This handles maps that are
                    # not rectangular, or have empty sections at the beginning
                    while y >= len(new_map.tiles):
                        new_map.tiles.append([])
                    while x >= len(new_map.tiles[y]):
                        new_map.tiles[y].append(None)  # Fill with None if needed

                    new_map.tiles[y][x] = tile

    # --- Object Layer (for start position, NPCs, etc.) ---
    for obj in tmx_data.objects:
        if obj.type == "start_position":  # Example object type
            if isinstance(new_map, WorldMap):
                new_map.start_x = int(obj.x // TILE_SIZE)
                new_map.start_y = int(obj.y // TILE_SIZE)

        elif obj.type == "npc":
            # Create and place an NPC.  You'll need to adapt this.
            if isinstance(new_map, Town):  # Only place NPCs in towns, for now
                npc_data = NPCS.get(obj.name)
                if npc_data:
                    npc = NPC(obj.name, int(obj.x // TILE_SIZE), int(obj.y // TILE_SIZE), npc_data["dialogue"],
                              {quest_id: Quest(
                                    quest_data["name"],
                                    quest_data["description"],
                                    quest_data["objectives"],
                                    quest_data["rewards"],
                                )
                                for quest_id, quest_data in npc_data.get("quests", {}).items()}) #Get dialogue and quests
                    npc.image = images["npc"] # Get image
                    npc.rect = npc.image.get_rect() # Create rect
                    npc.rect.topleft = (int(obj.x), int(obj.y))  # Use pixel coordinates
                    new_map.npcs.append(npc) # Append
                    new_map.tiles[int(obj.y // TILE_SIZE)][int(obj.x // TILE_SIZE)].npc = npc # Set npc value.
                else:
                    print(f"Error: NPC '{obj.name}' not found in NPCS data.")

        elif obj.type == "dungeon_entrance":
            if isinstance(new_map, WorldMap):
                new_map.tiles[int(obj.y // TILE_SIZE)][int(obj.x // TILE_SIZE)] = WorldMapTile(f"dungeon_entrance_{obj.dungeon_type}", True, x = int(obj.x//TILE_SIZE), y = int(obj.y//TILE_SIZE))
                new_map.tiles[int(obj.y // TILE_SIZE)][int(obj.x // TILE_SIZE)].add_connected_dungeon(obj.dungeon_type)
        elif obj.type == "stairs_up":
            if isinstance(new_map, Dungeon):
                new_map.up_stair_location = (int(obj.x // TILE_SIZE), int(obj.y // TILE_SIZE))
                new_map.tiles[int(obj.y//TILE_SIZE)][int(obj.x // TILE_SIZE)] = DungeonTile("stairs_up", True, x = int(obj.x//TILE_SIZE), y = int(obj.y//TILE_SIZE))
        elif obj.type == "stairs_down":
            if isinstance(new_map, Dungeon):
                new_map.down_stair_location = (int(obj.x // TILE_SIZE), int(obj.y // TILE_SIZE))
                new_map.tiles[int(obj.y//TILE_SIZE)][int(obj.x // TILE_SIZE)] = DungeonTile("stairs_down", True,  x = int(obj.x//TILE_SIZE), y = int(obj.y//TILE_SIZE))
        elif obj.type == "chest":
            if isinstance(new_map, Dungeon):
                new_map.tiles[int(obj.y//TILE_SIZE)][int(obj.x // TILE_SIZE)] = DungeonTile("chest", False,  x = int(obj.x//TILE_SIZE), y = int(obj.y//TILE_SIZE))
                new_map.tiles[int(obj.y//TILE_SIZE)][int(obj.x // TILE_SIZE)].objects = [{"type": "chest", "contents": {"Gold": 10, "Health Potion": 1}}]  # Example contents
        elif obj.type == "door":
            if isinstance(new_map, Dungeon):
                new_map.tiles[int(obj.y//TILE_SIZE)][int(obj.x // TILE_SIZE)] = DungeonTile("door", False,  x = int(obj.x//TILE_SIZE), y = int(obj.y//TILE_SIZE))


    return new_map

def load_images():
    """Loads images used in the game."""
    global images
    images = {
        "floor": pygame.image.load(resource_path(IMAGE_FLOOR)).convert_alpha(),
        "wall": pygame.image.load(resource_path(IMAGE_WALL)).convert_alpha(),
        "player": pygame.image.load(resource_path(IMAGE_PLAYER)).convert_alpha(),
        "monster": pygame.image.load(resource_path(IMAGE_MONSTER)).convert_alpha(),
        "town_floor": pygame.image.load(resource_path(IMAGE_TOWN_FLOOR)).convert_alpha(),  # Town floor
        "town_wall": pygame.image.load(resource_path(IMAGE_TOWN_WALL)).convert_alpha(),    # Town wall
        "npc": pygame.image.load(resource_path(IMAGE_NPC)).convert_alpha(),             # NPC image
        "stairs_up": pygame.image.load(resource_path(IMAGE_STAIRS_UP)).convert_alpha(),
        "stairs_down": pygame.image.load(resource_path(IMAGE_STAIRS_DOWN)).convert_alpha(),
        "chest" : pygame.image.load(resource_path(IMAGE_CHEST)).convert_alpha(),
        "door" : pygame.image.load(resource_path(IMAGE_DOOR)).convert_alpha(),
        "grass" : pygame.image.load(resource_path(IMAGE_GRASS)).convert_alpha()

        # Load more images here as needed (items, abilities, etc.)
    }

    # --- Scale images to the tile size ---
    for key, image in images.items():
        images[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

def load_settings():
    """Loads the game settings or uses defaults if file not present."""
    global settings
    try:
        with open(resource_path(SETTINGS_FILE), "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        print("Settings file not found, using default settings.")
        settings = DEFAULT_SETTINGS  # Use the constants

    # --- Validate loaded settings (important!) ---
    if not isinstance(settings, dict):
        print("Error: Invalid settings file format. Using defaults.")
        settings = DEFAULT_SETTINGS
        return

    # Check each setting individually, use default if invalid or missing
    if not isinstance(settings.get("fullscreen"), bool):
        print("Warning: Invalid 'fullscreen' setting, using default.")
        settings["fullscreen"] = DEFAULT_SETTINGS["fullscreen"]

    if not isinstance(settings.get("resolution"), list) or len(settings["resolution"]) != 2 or \
            not all(isinstance(x, int) for x in settings["resolution"]):
        print("Warning: Invalid 'resolution' setting, using default.")
        settings["resolution"] = DEFAULT_SETTINGS["resolution"]

    if not isinstance(settings.get("volume"), (int, float)) or not (0 <= settings["volume"] <= 1):
        print("Warning: Invalid 'volume' setting, using default.")
        settings["volume"] = DEFAULT_SETTINGS["volume"]
def save_settings():
    """Saves the current game settings."""
    global settings
    try:
        with open(resource_path(SETTINGS_FILE), "w") as f:
            json.dump(settings, f, indent=4) # Save
        print("Game settings saved.")
    except Exception as e:
        print(f"Error saving settings: {e}")

def render_map(screen, game_map, party):
    """Renders the current map to the screen, handling visibility."""

    # --- 1.  Handle Fog of War (Dungeon-specific) ---
    if isinstance(game_map, Dungeon):
        # Reset visibility (everything starts as not visible)
        for y in range(game_map.height):
            for x in range(game_map.width):
                game_map.tiles[y][x].visible = False

        # Set tiles around the player to visible, and explored.
        for y in range(party.y - 2, party.y + 3):
            for x in range(party.x - 2, party.x + 3):
                if 0 <= x < game_map.width and 0 <= y < game_map.height:
                    game_map.tiles[y][x].visible = True
                    game_map.tiles[y][x].explored = True # Mark explored

    # --- 2. Draw the Map ---
    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.tiles[y][x]

            # --- 3.  Handle drawing for different map types ---
            if isinstance(game_map, Dungeon):
                if tile.explored: # Check if explored
                    if tile.visible:
                        # Draw the tile and any objects on it
                        if tile.image:
                            if isinstance(tile.image, tuple): # Check image
                                print(f"Error: Tile image at ({x},{y}) is a tuple!")
                                tile.image = images.get("floor") # Set default
                            screen.blit(tile.image, (x * TILE_SIZE, y * TILE_SIZE))
                        # Draw monsters
                        for enemy in tile.enemies:
                            if enemy.is_alive():
                                if not enemy.image:
                                     enemy.image = images["monster"]
                                     enemy.rect = enemy.image.get_rect()
                                screen.blit(enemy.image, (enemy.x * TILE_SIZE, enemy.y * TILE_SIZE))


                    else:  # Explored, but not currently visible (darker)
                        if tile.image:
                            # Apply a darkening effect (simplest way)
                            darkened_image = tile.image.copy()
                            darkened_image.fill((100, 100, 100, 255), None, pygame.BLEND_RGBA_MULT)
                            screen.blit(darkened_image, (x * TILE_SIZE, y * TILE_SIZE))

            elif isinstance(game_map, Town):
                if tile.image: #Towns are all visible
                    if isinstance(tile.image, tuple): # Check image
                        print(f"Error: Town Tile image at ({x},{y}) is a tuple!")
                        tile.image = images.get("town_floor") # Set default
                    screen.blit(tile.image, (x*TILE_SIZE, y*TILE_SIZE)) # Blit
                if tile.npc and tile.npc.image is None: # Check and set images
                    tile.npc.image = images["npc"]
                    tile.npc.rect = tile.npc.image.get_rect()
                if tile.npc: # Blit npcs
                    screen.blit(tile.npc.image, (tile.npc.x*TILE_SIZE, tile.npc.y*TILE_SIZE))
            elif isinstance(game_map, WorldMap): # World is visisble
                if tile.image:
                    if isinstance(tile.image, tuple): # Check Image
                        print(f"Error: WorldMap Tile image at ({x},{y}) is a tuple!")
                        tile.image = images.get("grass") # Set Default
                    screen.blit(tile.image, (x * TILE_SIZE, y* TILE_SIZE))
                    
# --- Main Game Function ---

def main():
    """Main game function."""
    global settings
    pygame.init()

    load_settings()  # Load settings at the start

    if settings["fullscreen"]:
        screen = pygame.display.set_mode(settings["resolution"], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(settings["resolution"])


    pygame.display.set_caption("Roguelike RPG")

    clock = pygame.time.Clock()

    # --- Load Assets ---
    load_images()
    # Load sounds and music here (using pygame.mixer)

    # --- Game Initialization ---
    game_state = GameState()
    game_state.initialize_game()
    # Create a font object (you only need to do this once)
    font_size = int(MEDIUM_FONT_SCALE * SCREEN_HEIGHT)  # Example: 5% of screen height
    font = pygame.font.Font(None, font_size)

    # --- Main Menu Setup ---
    menu_title_font = pygame.font.Font(None, int(SCREEN_HEIGHT * MENU_TITLE_SCALE))
    menu_button_font = pygame.font.Font(None, int(SCREEN_HEIGHT * MENU_BUTTON_HEIGHT_SCALE))
    menu_button_texts = ["New Game", "Load Game", "Settings", "Quit"]
    menu_button_rects = [
        create_button_rect(screen, MENU_BUTTON_WIDTH_SCALE, MENU_BUTTON_HEIGHT_SCALE, 0.5, 0.4 + i * MENU_BUTTON_SPACING_SCALE)
        for i in range(len(menu_button_texts))
    ]
    selected_menu_button = 0  # Start with "New Game" selected.
    # --- Main Game Loop ---
    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- Input based on Game State ---
            if game_state.current_state == STATE_MENU:
                action, selected_menu_button = handle_menu_input(event, selected_menu_button, len(menu_button_texts))
                if action == "select":
                    if selected_menu_button == 0:  # New Game
                        # Reset game state for a new game (important!)
                        game_state = GameState()
                        game_state.initialize_game()
                        game_state.current_state = STATE_GAME
                    elif selected_menu_button == 1:  # Load Game
                        game_state.load_game()
                    elif selected_menu_button == 2: #Options
                        pass #TODO Add options menu
                    elif selected_menu_button == 3:  # Quit
                        running = False

            elif game_state.current_state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dx, dy = UP
                    elif event.key == pygame.K_DOWN:
                        dx, dy = DOWN
                    elif event.key == pygame.K_LEFT:
                        dx, dy = LEFT
                    elif event.key == pygame.K_RIGHT:
                        dx, dy = RIGHT
                    elif event.key == pygame.K_i: # Inventory
                        game_state.current_state = STATE_INVENTORY
                    elif event.key == pygame.K_ESCAPE: # Back to menu
                        game_state.current_state = STATE_MENU # Go to menu

                    game_state.party.move(dx, dy, game_state.current_map, game_state)
                    # Play footstep sound (if moved)
                    # pygame.mixer.Sound.play(sounds[SOUND_FOOTSTEP])

            elif game_state.current_state == STATE_INVENTORY: # Inventory state
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        game_state.current_state = STATE_GAME

            elif game_state.current_state == STATE_GAME_OVER: #Game over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        game_state.current_state = STATE_MENU  # Reset to menu

        # --- Game Logic Updates ---

        # --- Drawing/Rendering ---
        screen.fill(BLACK)  # Clear the screen

        if game_state.current_state == STATE_MENU:
            draw_menu(screen, "Main Menu", menu_button_texts, menu_button_rects, menu_title_font, menu_button_font, selected_menu_button)

        elif game_state.current_state == STATE_GAME or game_state.current_state == STATE_COMBAT or game_state.current_state == STATE_TOWN: # Render Map
            render_map(screen, game_state.current_map, game_state.party)

            # Draw the player (after drawing the map, so it's on top)
            if game_state.party:
                # Set the player image and rect (do this once, when created)
                if game_state.party.members:
                    if game_state.party.members[0].image is None: # Check
                        game_state.party.members[0].image = images["player"] # Set image
                        game_state.party.members[0].rect = game_state.party.members[0].image.get_rect()

                    screen.blit(game_state.party.members[0].image,
                            (game_state.party.x * TILE_SIZE, game_state.party.y * TILE_SIZE))
            draw_status_bar(screen, game_state.party, font) # Draw Status
            render_combat_log(screen, combat_log, font) # Combat log


        elif game_state.current_state == STATE_INVENTORY:
            draw_inventory(screen, game_state.party, font) #Draw inventory
            draw_status_bar(screen, game_state.party, font) # Status Bar
            render_combat_log(screen, combat_log, font) # Combat Log

        elif game_state.current_state == STATE_GAME_OVER:
            screen.fill(BLACK)
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("Game Over", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, game_over_rect)

        pygame.display.flip()  # Update the full display
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()