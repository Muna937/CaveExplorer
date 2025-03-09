import pygame
import random
import json  # For saving/loading
import math  # For potential future use
import sys
import os
# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 30  # Limit frame rate for smoother movement

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
STATE_SHOP = "shop"  # Placeholder for shop state
STATE_GAME_OVER = "game_over"
STATE_WORLD_MAP = "world_map"  # Placeholder for world map
STATE_TALENTS = "talents"  # Placeholder for talent screen
STATE_QUESTS = "quests"    # Placeholder for quest log


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
SHOP_WIDTH_SCALE = 0.6
SHOP_HEIGHT_SCALE = 0.8
SHOP_ITEM_SPACING_SCALE = 0.025
SHOP_FONT_SCALE = 0.035
# Combat UI
COMBAT_LOG_WIDTH_SCALE = 0.3
COMBAT_LOG_HEIGHT_SCALE = 0.6
COMBAT_LOG_FONT_SCALE = 0.025
COMBAT_BUTTON_WIDTH_SCALE = 0.15
COMBAT_BUTTON_HEIGHT_SCALE = 0.07
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
IMAGE_STAIRS_UP = "assets/stairs_up.png"  # Placeholder
IMAGE_STAIRS_DOWN = "assets/stairs_down.png"  # Placeholder
IMAGE_CHEST = "assets/chest.png" # Placeholder
IMAGE_DOOR = "assets/door.png" #Placeholder

# --- Global Variables ---
combat_log = []
MAX_LOG_MESSAGES = 10

# --- Helper Functions ---

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  # Use current working directory if not an executable

    return os.path.join(base_path, relative_path)

def add_to_combat_log(message):
    global combat_log
    combat_log.append(message)
    if len(combat_log) > MAX_LOG_MESSAGES:
        combat_log.pop(0)

# --- Class Definitions ---

class Entity(pygame.sprite.Sprite):  # Inherit from Sprite
    def __init__(self, name, x, y, stats, abilities, inventory=None):
        super().__init__() # Call the Sprite initializer
        self.name = name
        self.x = x  # Grid coordinates (not pixel)
        self.y = y
        self.stats = stats  # Dictionary of base stats
        self.abilities = abilities
        self.inventory = inventory if inventory is not None else {}
        self.equipped_weapon = None
        self.equipped_armor = None
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
        if random.randint(1, 100) <= (self.get_accuracy() - target.get_evasion()):
            damage = int(self.get_attack_damage()) # Base damage
            if random.randint(1, 100) <= self.get_crit_chance():
                damage = int(damage * self.get_crit_damage())
                add_to_combat_log("Critical Hit!")
            damage = max(0, damage - target.get_defense())
            target.hp -= damage
            add_to_combat_log(f"{self.name} attacks {target.name} for {damage} damage!")
            if target.hp <= 0:
                target.hp = 0 # Prevent negative
        else:
            add_to_combat_log(f"{self.name} missed!")


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
                        self.unequip_item(self.equipped_weapon["name"])
                    self.equipped_weapon = item
                    self.inventory[item_name] -= 1
                    if self.inventory[item_name] == 0:
                        del self.inventory[item_name]
                    self.calculate_derived_stats()
                    add_to_combat_log(f"Equipped {item_name}.")
                    return  # Return after equipping

                elif item["type"] == "armor":
                    if self.equipped_armor:
                        self.unequip_item(self.equipped_armor["name"])
                    self.equipped_armor = item
                    self.inventory[item_name] -= 1
                    if self.inventory[item_name] == 0:
                        del self.inventory[item_name]
                    self.calculate_derived_stats()
                    add_to_combat_log(f"Equipped {item_name}.")
                    return  # Return after equipping
        else:
            add_to_combat_log(f"You don't have {item_name} in your inventory.")

    def unequip_item(self, item_name):
        if self.equipped_weapon and self.equipped_weapon["name"] == item_name:
            if item_name not in self.inventory:  # Check if item exists
                self.inventory[item_name] = 0
            self.inventory[item_name] += 1
            self.equipped_weapon = None
            self.calculate_derived_stats()
            add_to_combat_log(f"Unequipped {item_name}.")
        elif self.equipped_armor and self.equipped_armor["name"] == item_name:
            if item_name not in self.inventory:
                self.inventory[item_name] = 0
            self.inventory[item_name] += 1
            self.equipped_armor = None
            self.calculate_derived_stats()
            add_to_combat_log(f"Unequipped {item_name}.")
        else:
            add_to_combat_log(f"You don't have {item_name} equipped.")

class Player(Entity):
    def __init__(self, name, player_class, x, y):
        self.player_class = player_class
        stats = CLASS_STATS[player_class]
        super().__init__(name, x, y, stats, CLASS_ABILITIES[player_class], inventory={"Gold": 10})
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.talent_points = 0  # Placeholder for talent points


    def level_up(self):
        while self.xp >= self.xp_to_next_level:
            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # Exponential increase

            # Get stat increases from CLASS_LEVEL_UP_STATS
            level_up_stats = CLASS_LEVEL_UP_STATS[self.player_class]
            for stat, increase in level_up_stats.items():
                self.stats[stat] += increase

            self.calculate_derived_stats()  # Update derived stats
            self.hp = self.max_hp  # Full heal on level up
            self.mana = self.max_mana  # Restore mana on level up
            self.talent_points += 1  # Placeholder: Award talent point
            add_to_combat_log(f"{self.name} leveled up to level {self.level}!")

    def learn_ability(self, ability_name):
        # Placeholder for learning abilities (e.g., from trainers, level up)
        if ability_name not in self.abilities and ability_name in ABILITIES:
            self.abilities.append(ability_name)
            add_to_combat_log(f"{self.name} learned {ability_name}!")

    def display_talents(self):
        # Placeholder: UI for spending talent points
        pass

    def use_talent(self, talent):
        # Placeholder: Logic for applying talent effects
        pass


class Monster(Entity):
    def __init__(self, name, x, y, stats, abilities, inventory, xp_reward, gold_reward, drops):
        super().__init__(name, x, y, stats, abilities, inventory)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.drops = drops  # List of (item_name, drop_chance) tuples

    def choose_action(self, target):
        # Basic AI:  Prioritize abilities if available and usable, otherwise attack.
        usable_abilities = [
            ability_name for ability_name in self.abilities
            if ABILITIES[ability_name]["mana_cost"] <= self.mana
            and ABILITIES[ability_name]["type"] == "attack" # Only attack abilities
        ]

        if usable_abilities:
             ability_name = random.choice(usable_abilities)
             self.use_ability(ability_name, target)
        else:
            self.attack(target)  # Basic attack

class Party:
    def __init__(self, members, x=0, y=0):  # Start at (0, 0) by default
        self.members = members
        self.x = x  # Grid coordinates (not pixel)
        self.y = y
        self.inventory = {"Gold": 0} # Initial gold

    def is_alive(self):
         return any(member.is_alive() for member in self.members)

    def add_to_inventory(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_from_inventory(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]  # Remove if quantity is 0 or less

    def move(self, dx, dy, dungeon):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < dungeon.width and 0 <= new_y < dungeon.height:
            if dungeon.is_walkable(new_x, new_y):
                self.x = new_x
                self.y = new_y
                dungeon.interact_with_tile(new_x, new_y, self) # For stairs, chests etc
                return True  # Movement successful
            else:
                add_to_combat_log("You can't move there.") # Blocked by wall, etc
                return False
        else:
            add_to_combat_log("You can't go that way.") # Out of bounds
            return False


class Tile(pygame.sprite.Sprite): # Inherit for rendering
    def __init__(self, tile_type, walkable, image=None):
        super().__init__()
        self.tile_type = tile_type  # "floor", "wall", "stairs_up", "stairs_down"
        self.walkable = walkable
        self.image = image # The actual image
        self.rect = None # Set in Dungeon class, needed for rendering
        self.explored = False  # Fog of war
        self.visible = False   # Line of sight
        self.contains_object = None # Chests, etc

    def is_walkable(self):
        return self.walkable

class DungeonTile(Tile):  # Added a subclass for the dungeon
    def __init__(self, tile_type, walkable, image=None):
        super().__init__(tile_type, walkable, image)
        self.enemies = []
        self.cleared = False # Combat boolean

    def is_cleared(self):
        return self.cleared

    def set_cleared(self, cleared):
        self.cleared = cleared


class WorldMapTile(Tile): # Added a subclass for the worldmap
    def __init__(self, tile_type, walkable, image = None):
        super().__init__(tile_type, walkable, image)
        self.connected_dungeons = [] # Dungeons at this location.

    def add_connected_dungeon(self, dungeon_name):
        self.connected_dungeons.append(dungeon_name)


class Stairs(Tile):
    def __init__(self, tile_type, destination, image=None):
        super().__init__(tile_type, True, image)  # Stairs are walkable
        self.destination = destination  # (map_name, x, y) tuple

    def interact(self, party, game_state): # Pass game_state for changing
        destination_map_name, dest_x, dest_y = self.destination
        if destination_map_name == "world_map":
            game_state.current_map = game_state.world_map
            game_state.current_state = STATE_WORLD_MAP
            game_state.party.x = dest_x
            game_state.party.y = dest_y
            add_to_combat_log("You ascend to the world map.")
        elif destination_map_name in game_state.dungeons:
            game_state.current_map = game_state.dungeons[destination_map_name]
            game_state.current_state = STATE_GAME # Back to dungeon state
            game_state.party.x = dest_x
            game_state.party.y = dest_y
            add_to_combat_log(f"You enter {destination_map_name}")
        else:
            print(f"Error: Destination map '{destination_map_name}' not found.")



class Chest(Tile):
    def __init__(self, tile_type, contents, image=None, locked=False, trap=None):
        super().__init__(tile_type, False, image)  # Chests are initially not walkable
        self.contents = contents  # Dictionary of {item_name: quantity}
        self.locked = locked
        self.trap = trap    # None, or a trap type (e.g., "poison", "explosion")
        self.opened = False

    def interact(self, party, game_state): #Added game_state
        if not self.opened:
            if self.locked:
                add_to_combat_log("The chest is locked!")
                # Placeholder for lockpicking/bashing
            else:
                self.opened = True
                self.walkable = True # Now walkable
                self.image = None # Remove chest image
                if self.trap:
                    self.trigger_trap(party)
                self.give_loot(party)


    def trigger_trap(self, party):
        # Placeholder for trap effects
        if self.trap == "poison":
            add_to_combat_log("A poisonous gas fills the air!")
            for member in party.members:
                member.hp -= 5  # Example damage
        elif self.trap == "explosion":
            add_to_combat_log("The chest explodes!")
            for member in party.members:
                member.hp -= 15  # Example damage

    def give_loot(self, party):
        for item_name, quantity in self.contents.items():
            party.add_to_inventory(item_name, quantity)
            add_to_combat_log(f"You found {quantity} {item_name} in the chest!")

class Door(Tile):
    def __init__(self, tile_type, image=None, locked=False, key_name=None):
        super().__init__(tile_type, False, image) # Doors start not walkable.
        self.locked = locked
        self.key_name = key_name # The name of the key, or None.
        self.opened = False # Open or closed

    def interact(self, party, game_state): # Added game_state
        if self.opened == False:
            if self.locked:
                if self.key_name and self.key_name in party.inventory:
                    add_to_combat_log(f"You unlocked the door with the {self.key_name}!")
                    party.remove_from_inventory(self.key_name,1)
                    self.locked = False
                    self.opened = True
                    self.walkable = True # Now walkable
                    self.image = None  # Make invisible.  Could have open door graphic.

                else:
                    add_to_combat_log("The door is locked.")
                    # Add option to pick lock, bash, etc.
            else: # Not locked, just closed
                self.opened = True
                self.walkable = True
                self.image = None # Remove image
                add_to_combat_log("You open the door.")

class Map:  # Base class for both Dungeon and WorldMap
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [] # To be filled by subclasses.

    def is_walkable(self, x, y):
        # Check bounds and walkability of the tile
        return 0 <= x < self.width and 0 <= y < self.height and self.tiles[y][x].is_walkable()

    def interact_with_tile(self, x, y, party):
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.tiles[y][x]
            if hasattr(tile, "interact"): # Check if the object on tile has interact method
                tile.interact(party, self)

class Dungeon(Map):  # Inherits from Map
    def __init__(self, width, height, num_rooms, name = "Unnamed Dungeon"):
        super().__init__(width, height)  # Call Map's initializer
        self.num_rooms = num_rooms
        self.name = name
        self.tiles = [[DungeonTile("wall", False) for _ in range(width)] for _ in range(height)]
        self.rooms = []  # List to store Room objects
        self.generate_dungeon()  # Call the generation method
        self.stairs_up_location = None  # (x, y) of stairs up
        self.stairs_down_location = None # (x, y) of stairs down
        self.place_stairs() # Place the stairs in the dungeon
        self.place_objects()

    def generate_dungeon(self):
        # --- 1. Create Rooms ---
        for _ in range(self.num_rooms):
            w = random.randint(3, 8)  # Room width
            h = random.randint(3, 8)  # Room height
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)
            new_room = Room(x, y, w, h)

            # Check for overlaps
            if not any(new_room.intersects(other_room) for other_room in self.rooms):
                self.rooms.append(new_room)
                self.create_room(new_room)

        # --- 2. Create Corridors ---
        for i in range(1, len(self.rooms)):  # Connect each room to the previous one
            self.connect_rooms(self.rooms[i - 1], self.rooms[i])

    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.tiles[y][x] = DungeonTile("floor", True)

    def connect_rooms(self, room1, room2):
        x1, y1 = room1.center()
        x2, y2 = room2.center()

        # Create L-shaped corridors
        if random.choice([True, False]):  # Randomly choose horizontal or vertical first
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[y][x] = DungeonTile("floor", True)  # Use floor tiles for tunnels

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[y][x] = DungeonTile("floor", True)

    def place_stairs(self):
        # Place stairs up in the first room
        room1_center = self.rooms[0].center()
        self.tiles[room1_center[1]][room1_center[0]] = Stairs("stairs_up", ("world_map", 10, 10))  # Example destination
        self.stairs_up_location = room1_center

        # Place stairs down in the last room
        last_room_center = self.rooms[-1].center()
        self.tiles[last_room_center[1]][last_room_center[0]] = Stairs("stairs_down", ("another_dungeon", 5, 5))  # Example
        self.stairs_down_location = last_room_center

    def place_objects(self):
        # Place chests, doors, etc.
        for room in self.rooms[1:]: # Skip first room, avoid blocking stairs
            if random.random() < 0.2: # 20% to spawn a chest
                x = random.randint(room.x1 + 1, room.x2 - 2)
                y = random.randint(room.y1 + 1, room.y2 - 2)
                if self.tiles[y][x].tile_type == "floor": # Check if the space is clear.
                    self.tiles[y][x] = Chest("chest", {"Potion": 1, "Gold": 10})

            if random.random() < 0.3: # 30% chance for a door
                # Simple door placement: choose a random wall tile in the room
                possible_door_locations = []
                for x in range(room.x1, room.x2):
                    if self.tiles[room.y1 -1][x].tile_type == "wall": # Check North
                        possible_door_locations.append((x, room.y1 -1))
                    if self.tiles[room.y2][x].tile_type == "wall": # Check south
                        possible_door_locations.append((x,room.y2))
                for y in range(room.y1, room.y2):
                    if self.tiles[y][room.x1 - 1].tile_type == "wall": # Check West
                        possible_door_locations.append((room.x1 - 1, y))
                    if self.tiles[y][room.x2].tile_type == "wall":# Check East
                        possible_door_locations.append((room.x2, y))

                if possible_door_locations:
                    x,y = random.choice(possible_door_locations)
                    # 50% chance to be locked
                    locked = random.random() < 0.5
                    key_name = f"key_{self.name}_{x}_{y}" if locked else None # Unique key
                    self.tiles[y][x] = Door("door", locked=locked, key_name=key_name)

    def place_monsters(self, num_monsters):
        placed_monsters = 0
        while placed_monsters < num_monsters:
            # Choose a random room, but not the first room where the stairs are
            room = random.choice(self.rooms[1:])  # Start from index 1
            x = random.randint(room.x1 + 1, room.x2 - 2)
            y = random.randint(room.y1 + 1, room.y2 - 2)

            # Check if the tile is a floor tile and walkable
            if self.tiles[y][x].tile_type == "floor" and self.tiles[y][x].is_walkable:
                monster_stats = {
                    "max_hp": 10,
                    "max_mana": 5,
                    "Strength": 3,
                    "Agility": 2,
                    "Intelligence": 1,
                    "Wisdom": 1,
                    "Dexterity": 2,
                    "Luck": 1,
                    "Charisma": 1
                }
                new_monster = Monster("Goblin", x, y, monster_stats, ["Scratch"],{}, 50, 5, [("Potion", 20)])  # Example
                self.tiles[y][x].enemies.append(new_monster)
                placed_monsters += 1


    def interact_with_tile(self, x, y, party):
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.tiles[y][x]
            if hasattr(tile, "interact"):
                tile.interact(party,self)
            if tile.enemies and not tile.is_cleared():
                combat(party, tile.enemies)
                tile.set_cleared(True)
                tile.enemies = []  # Clear enemies after combat (important fix!)

class WorldMap(Map): # Inherit from map
    def __init__(self, width, height):
        super().__init__(width, height)
        self.tiles = self.generate_map()  # Call World Map generation
        self.towns = []  # Placeholder: list of town locations/names
        self.dungeon_entrances = [] # Placeholder: list of (x,y,dungeon_name)

    def generate_map(self):
        # Very basic world map generation (random for now)
        tiles = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if random.random() < 0.7:  # 70% chance of grass
                    row.append(WorldMapTile("grass", True))
                elif random.random() < 0.2:  # 20% chance of trees
                    row.append(WorldMapTile("trees", False))  # Not walkable
                else:  # 10% chance of mountains
                    row.append(WorldMapTile("mountain", False)) # Not walkable
            tiles.append(row)
        return tiles

    def add_town(self, x, y, town_name):
        # Placeholder: Add town data, change tile graphic, etc.
        self.towns.append((x, y, town_name))
        # Example: self.tiles[y][x] = WorldMapTile("town", True, town_image)

    def add_dungeon_entrance(self, x, y, dungeon_name):
         self.dungeon_entrances.append((x,y,dungeon_name))
         self.tiles[y][x].add_connected_dungeon(dungeon_name)

    def interact_with_tile(self, x, y, party):
        super().interact_with_tile(x, y, party)  # Call base class interaction
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = self.tiles[y][x]
            for dungeon_name in tile.connected_dungeons:  # Check for connected dungeons
                # Placeholder: Transition to dungeon (create/load if needed)
                print(f"Entering dungeon: {dungeon_name}")
                #  game_state.current_map = game_state.dungeons[dungeon_name]
                #  game_state.current_state = STATE_GAME
                #  Find stairs up in the dungeon, and move the party there.
                #  game_state.party.x = game_state.current_map.stairs_up_location[0]
                #  game_state.party.y = game_state.current_map.stairs_up_location[1]
                pass

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y

    def intersects(self, other):
        # Returns True if this room overlaps with another
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Shop: # Placeholder for shops
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def buy(self, item_name, quantity, party):
        pass

    def sell(self, item_name, quantity, party):
        pass

class Quest:  # Placeholder for quests
    def __init__(self, name, description, objectives, reward):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of objective dictionaries
        self.reward = reward
        self.completed = False

    def check_completion(self, party):
        # Check if all objectives are met
        pass

class GameState:
    def __init__(self):
      self.current_state = STATE_MENU
      self.party = None  # Will hold the Party object
      self.dungeons = {}  # Dictionary to store multiple dungeons: {"dungeon_name": Dungeon object}
      self.world_map = None
      self.current_map = None  # Can be a Dungeon or WorldMap object
      self.current_shop = None # Placeholder
      self.quests = [] # Placeholder

    def initialize_game(self):
        # Create player characters (example)
        player1 = Player("Jared", "Warrior", 0, 0)  # Start at (0, 0)
        player2 = Player("Lysa", "Mage", 0, 0)
        self.party = Party([player1, player2], 5, 5) # Place party.

        # Create a dungeon (example)
        self.dungeons["Starter Dungeon"] = Dungeon(20, 15, 5, name = "Starter Dungeon")
        self.dungeons["Starter Dungeon"].place_monsters(3) # Place Monsters
        self.current_map = self.dungeons["Starter Dungeon"]

        # Create the world map
        self.world_map = WorldMap(50, 40)  # Example size
        self.world_map.add_dungeon_entrance(10, 10, "Starter Dungeon")  # Connect world map to dungeon
        # self.current_map = self.world_map # Set to the created map

    def save_game(self, filename="savegame.json"):
        # Placeholder for saving game state to a file
        save_data = {
            "current_state": self.current_state,
            # ... Save other game data ...
        }
        with open(filename, "w") as f:
            json.dump(save_data, f)
        print(f"Game saved to {filename}")

    def load_game(self, filename="savegame.json"):
        # Placeholder for loading game state from a file
        try:
            with open(filename, "r") as f:
                save_data = json.load(f)
            self.current_state = save_data["current_state"]
            # ... Load other game data ...
            print(f"Game loaded from {filename}")
        except FileNotFoundError:
            print(f"No save file found: {filename}")


# --- Combat ---

def combat(party, enemies):
    add_to_combat_log("Combat begins!")

    # Combine participants and sort by initiative
    all_combatants = party.members + enemies
    turn_order = sorted(all_combatants, key=lambda x: x.get_initiative(), reverse=True)
    current_turn_index = 0

    while party.is_alive() and any(enemy.is_alive() for enemy in enemies): # Use is_alive()
        current_entity = turn_order[current_turn_index]

        # --- Player's Turn ---
        if current_entity in party.members:
            current_entity.update_buffs() # Update at start
            if not current_entity.is_alive(): # Skip dead members.
                current_turn_index = (current_turn_index + 1) % len(turn_order)
                continue

            add_to_combat_log(f"\nIt's {current_entity.name}'s turn!")
            add_to_combat_log("Choose an action:")
            add_to_combat_log("1. Attack")
            add_to_combat_log("2. Use Ability")
            add_to_combat_log("3. Use Item")
            add_to_combat_log("4. Check Status")
            add_to_combat_log("5. Flee") # Added flee

            action = input("> ")

            if action == "1":  # Attack
                # Basic target selection (first enemy) - IMPROVE THIS
                target = next((enemy for enemy in enemies if enemy.is_alive()), None)
                if target:
                    current_entity.attack(target)

            elif action == "2":  # Use Ability
                add_to_combat_log("Available Abilities:")
                for i, ability_name in enumerate(current_entity.abilities):
                    add_to_combat_log(f"{i + 1}. {ability_name} ({ABILITIES[ability_name]['mana_cost']} MP)")

                choice = input("Choose an ability (or press Enter to cancel): ")
                try:
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(current_entity.abilities):
                        ability_name = current_entity.abilities[choice_index]
                        # Basic target selection (IMPROVE THIS)
                        target = next((enemy for enemy in enemies if enemy.is_alive()), None)  # Default to enemy
                        if ABILITIES[ability_name]['type'] == 'heal':
                            target = current_entity # Heal self.
                        if target:
                            current_entity.use_ability(ability_name, target)
                except ValueError:
                    pass  # Invalid input, do nothing

            elif action == "3":  # Use Item
                if not party.inventory:
                    add_to_combat_log("Your inventory is empty.")
                else:
                    # Display Inventory
                    add_to_combat_log("Inventory:")
                    for i, (item_name, quantity) in enumerate(party.inventory.items()):
                         if item_name != "Gold":
                            add_to_combat_log(f"{i + 1}. {item_name} ({quantity})")

                    choice = input("Choose an item to use (or press Enter to cancel): ")
                    try:
                        choice_index = int(choice) - 1
                        # Filter out "Gold"
                        non_gold_items = [item for item in party.inventory if item != "Gold"]
                        if 0 <= choice_index < len(non_gold_items):
                            item_name = non_gold_items[choice_index]
                            # Target selection for items (IMPROVE)
                            target = current_entity # Default to using on self.
                            current_entity.use_item(item_name, target)
                    except ValueError:
                        pass  # Invalid input

            elif action == "4":  # Check Status (Placeholder)
                 display_player_status(current_entity) # Display Character info.

            elif action == "5": # Flee
                add_to_combat_log("You attempt to flee...")
                # Placeholder: Implement fleeing logic (e.g., chance based on speed)
                if random.random() < 0.5:  # 50% chance for now
                    add_to_combat_log("You escaped successfully!")
                    return  # End combat immediately
                else:
                    add_to_combat_log("You failed to escape!")


        # --- Enemy's Turn ---
        else:
            current_entity.update_buffs()
            if not current_entity.is_alive():
                current_turn_index = (current_turn_index + 1) % len(turn_order)
                continue

            add_to_combat_log(f"\nIt's {current_entity.name}'s turn!")
            # Basic AI: attack a random living party member
            target = next((member for member in party.members if member.is_alive()), None)
            if target:
                current_entity.choose_action(target)

        # --- Defeated Enemy Handling (simplified) ---
        defeated_enemies = [enemy for enemy in enemies if not enemy.is_alive()]
        for enemy in defeated_enemies:
            add_to_combat_log(f"You defeated the {enemy.name}!")
            # Remove from turn order and enemies list
            if enemy in turn_order:
                turn_order.remove(enemy)

            if current_turn_index >= len(turn_order):
                current_turn_index = 0
            enemies.remove(enemy)

            # Rewards.
            for item_name, drop_chance in enemy.drops:
                if random.randint(1,100) <= drop_chance:
                    party.add_to_inventory(item_name, 1)
                    add_to_combat_log(f"The {enemy.name} dropped a {item_name}!")

        for player in party.members:  # Moved outside
            for enemy in defeated_enemies:
                player.xp += enemy.xp_reward
                add_to_combat_log(f"{player.name} gained {enemy.xp_reward} XP!")
            player.level_up()
            party.add_to_inventory("Gold", enemy.gold_reward)  # Moved Gold here as well
            add_to_combat_log(f"You found {enemy.gold_reward} gold!")

        current_turn_index = (current_turn_index + 1) % len(turn_order)


    if not party.is_alive():
        add_to_combat_log("Your party has been defeated!")
    else:
        add_to_combat_log("You have won the battle!")


# --- UI Rendering Functions ---

def render_main_menu(screen, font, selected_option):
    screen.fill(BLACK)
    title_text = font.render("My RPG Game", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.2)))
    screen.blit(title_text, title_rect)

    options = ["New Game", "Load Game", "Options", "Exit"]
    button_height = int(SCREEN_HEIGHT * MENU_BUTTON_HEIGHT_SCALE)
    button_width = int(SCREEN_WIDTH * MENU_BUTTON_WIDTH_SCALE)
    y_offset = int(SCREEN_HEIGHT * 0.4)

    for i, option in enumerate(options):
        color = WHITE if i == selected_option else GREY
        text = font.render(option, True, color)
        rect = pygame.Rect(0, 0, button_width, button_height)
        rect.center = (SCREEN_WIDTH // 2, y_offset + i * int(button_height + SCREEN_HEIGHT * MENU_BUTTON_SPACING_SCALE))
        pygame.draw.rect(screen, DARK_GREY, rect)  # Button background
        screen.blit(text, text.get_rect(center=rect.center))

def render_status_bar(screen, party, font):
    bar_height = int(SCREEN_HEIGHT * STATUS_BAR_HEIGHT_SCALE)
    padding = int(SCREEN_HEIGHT * STATUS_BAR_PADDING_SCALE)
    pygame.draw.rect(screen, DARK_GREY, (0, 0, SCREEN_WIDTH, bar_height))

    x_offset = padding
    for i, member in enumerate(party.members):
        # Display Name, HP, Mana
        text = font.render(
            f"{member.name} (Lv. {member.level}) - HP: {member.hp}/{member.max_hp}  MP: {member.mana}/{member.max_mana}",
            True, WHITE
        )
        screen.blit(text, (x_offset, padding))
        x_offset += text.get_width() + 4 * padding # Dynamic spacing

        # Display status effects
        status_x = x_offset
        for buff in member.buffs:
            buff_text = font.render(f"{buff['stat']}: {buff['amount']} ({buff['duration']})", True, YELLOW)
            screen.blit(buff_text,(status_x, padding))
            status_x += buff_text.get_width() + padding

def render_combat_log(screen, log, font):
    log_width = int(SCREEN_WIDTH * COMBAT_LOG_WIDTH_SCALE)
    log_height = int(SCREEN_HEIGHT * COMBAT_LOG_HEIGHT_SCALE)
    x = SCREEN_WIDTH - log_width
    y = SCREEN_HEIGHT - log_height
    pygame.draw.rect(screen, DARK_GREY, (x, y, log_width, log_height))

    y_offset = y + int(SCREEN_HEIGHT * STATUS_BAR_PADDING_SCALE)
    for message in reversed(log):  # Show newest messages at the bottom
        text = font.render(message, True, WHITE)
        screen.blit(text, (x + 5, y_offset))
        y_offset += text.get_height() + 5

def render_inventory(screen, party, selected_index, font):
    inventory_rect = pygame.Rect(
        SCREEN_WIDTH * (1 - INVENTORY_WIDTH_SCALE) / 2,
        SCREEN_HEIGHT * (1 - INVENTORY_HEIGHT_SCALE) / 2,
        SCREEN_WIDTH * INVENTORY_WIDTH_SCALE,
        SCREEN_HEIGHT * INVENTORY_HEIGHT_SCALE,
    )
    pygame.draw.rect(screen, DARK_GREY, inventory_rect)

    title_surface = font.render("Inventory", True, WHITE)
    title_rect = title_surface.get_rect(center=(inventory_rect.centerx, inventory_rect.top + 20))
    screen.blit(title_surface, title_rect)

    y_offset = title_rect.bottom + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT

    item_names = list(party.inventory.keys())

    for i, item_name in enumerate(item_names):
        color = WHITE
        if i == selected_index:
            color = YELLOW  # Highlight the selected item

        item_text = f"{item_name}: {party.inventory[item_name]}"
        text_surface = font.render(item_text, True, color)
        text_rect = text_surface.get_rect(topleft=(inventory_rect.left + 20, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_rect.height + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT

    options = ["Equip", "Use", "Unequip", "Return"]
    valid_options = []

    if any(item in WEAPONS or item in ARMOR for item in item_names):
        valid_options.append("Equip")
    if any(item in ITEMS for item in item_names):
        valid_options.append("Use")
    if any(member.equipped_weapon or member.equipped_armor for member in party.members):
        valid_options.append("Unequip")
    valid_options.append("Return")


    x_offset = inventory_rect.left + 20
    y_offset = inventory_rect.centery
    for i, option in enumerate(valid_options):
        option_text = f"{i + 1}. {option}"
        option_surface = font.render(option_text, True, WHITE)
        option_rect = option_surface.get_rect(topleft=(x_offset, y_offset))
        screen.blit(option_surface, option_rect)
        y_offset += option_rect.height + INVENTORY_ITEM_SPACING_SCALE * SCREEN_HEIGHT

def render_dungeon(screen, game_state):
    dungeon = game_state.current_map
    party = game_state.party

    # --- 1. Draw Tiles ---
    for y in range(dungeon.height):
        for x in range(dungeon.width):
            tile = dungeon.tiles[y][x]
            if tile.image:  # Check if the tile has an image (important for opened chests, doors, etc.)
                screen.blit(tile.image, tile.rect) # Use tile.rect!

            # --- 2. Draw Entities within Tiles (Monsters) ---
            if isinstance(tile, DungeonTile):  # Check tile type
                for enemy in tile.enemies:
                    if enemy.is_alive():  # Only draw alive enemies
                        #Update the enemy rect before drawing
                        enemy.rect.topleft = (enemy.x * TILE_SIZE, enemy.y * TILE_SIZE)
                        screen.blit(enemy.image, enemy.rect) # Use the image dictionary and type


    # --- 3. Draw Player (Party Members) ---
    for player in party.members:
        # Update rect position based on player's x, y coordinates
        player.rect.topleft = (player.x * TILE_SIZE, player.y * TILE_SIZE)
        screen.blit(player.image, player.rect)  # Draw using player.image and player.rect


def display_player_status(player): # Added to display player status.
    print("\n--- Player Status ---")
    print(f"Name: {player.name} ({player.player_class})")
    print(f"Level: {player.level}")
    print(f"XP: {player.xp} / {player.xp_to_next_level}")
    print(f"HP: {player.hp} / {player.max_hp}")
    print(f"MP: {player.mana} / {player.max_mana}")
    print(f"Strength: {player.Strength}")
    print(f"Agility: {player.Agility}")
    print(f"Intelligence: {player.Intelligence}")
    print(f"Wisdom: {player.Wisdom}")
    print(f"Dexterity: {player.Dexterity}")
    print(f"Luck: {player.Luck}")
    print(f"Charisma: {player.Charisma}")
    print(f"Attack Damage: {player.get_attack_damage()}")
    print(f"Defense: {player.get_defense()}")
    print(f"Accuracy: {player.get_accuracy()}")
    print(f"Evasion: {player.get_evasion()}")
    print(f"Critical Hit Chance: {player.get_crit_chance()}%")
    print(f"Critical Hit Damage: {player.get_crit_damage()*100}%")


    print("Equipped Weapon:", player.equipped_weapon["name"] if player.equipped_weapon else "None")
    print("Equipped Armor:", player.equipped_armor["name"] if player.equipped_armor else "None")

    print("Inventory:")
    for item, quantity in player.inventory.items():
        print(f"  {item}: {quantity}")

    print("Active Buffs:")
    if player.buffs:
        for buff in player.buffs:
            print(f"  {buff['stat']}: +{buff['amount']} ({buff['duration']} turns remaining)")
    else:
        print("  None")

# --- Game Logic Functions ---

def create_player():
    # Placeholder for character creation screen (replace with Pygame UI later)
    print("Welcome, adventurer! Create your character:")
    name = input("Enter your name: ")
    while True:
        class_choice = input("Choose your class (Warrior, Rogue, Mage): ").capitalize()
        if class_choice in CLASS_STATS:
            break
        else:
            print("Invalid class.  Please choose Warrior, Rogue, or Mage.")

    stats = CLASS_STATS[class_choice]
    abilities = CLASS_ABILITIES[class_choice]
    return Player(name, class_choice, 0, 0, stats['max_hp'], stats['max_hp'], stats['max_mana'], stats['max_mana'], stats["Strength"], stats["Agility"], stats["Intelligence"], stats["Wisdom"], stats["Dexterity"], stats["Luck"], stats["Charisma"], 1, 0, 100, abilities)


# --- Main Game Loop ---

def game_loop():
    game_state = GameState()
    game_state.initialize_game()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My RPG Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, int(MEDIUM_FONT_SCALE * SCREEN_HEIGHT))

    # --- Load Images into Dictionaries ---
    try:
        images = {
            "floor": pygame.transform.scale(pygame.image.load(resource_path("assets/floor.png")).convert(), (TILE_SIZE, TILE_SIZE)),
            "wall": pygame.transform.scale(pygame.image.load(resource_path("assets/wall.png")).convert(), (TILE_SIZE, TILE_SIZE)),
            "player": {  # Nested dictionary for player classes
                "Warrior": pygame.transform.scale(pygame.image.load(resource_path("assets/player.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE)),  # Example: Warrior
                # Add other player classes here (Rogue, Mage, etc.)
            },
            "monster": {  # Nested dictionary for monster types
                "Goblin": pygame.transform.scale(pygame.image.load(resource_path("assets/monster.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE)), # Use same image for all now
                # Add other monster types here
            },
            "stairs_up": pygame.transform.scale(pygame.image.load(resource_path("assets/stairs_up.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE)),  # Placeholder
            "stairs_down": pygame.transform.scale(pygame.image.load(resource_path("assets/stairs_down.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE)),  # Placeholder
            "chest": pygame.transform.scale(pygame.image.load(resource_path("assets/chest.png")).convert_alpha(), (TILE_SIZE, TILE_SIZE)), #Placeholder
            "door": pygame.transform.scale(pygame.image.load(resource_path("assets/door.png")).convert_alpha(), (TILE_SIZE,TILE_SIZE))
        }
    except pygame.error as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        return
    # --- Assign images to tiles ---
    for row in game_state.current_map.tiles:
        for tile in row:
            if tile.tile_type == "floor":
                tile.image = images["floor"]
            elif tile.tile_type == "wall":
                tile.image = images["wall"]
            elif tile.tile_type == "stairs_up":
                tile.image = images["stairs_up"]
            elif tile.tile_type == "stairs_down":
                tile.image = images["stairs_down"]
            elif tile.tile_type == "chest":
                tile.image = images["chest"]
            elif tile.tile_type == "door":
                tile.image = images["door"]
            tile.rect = pygame.Rect(tile.x * TILE_SIZE, tile.y*TILE_SIZE, TILE_SIZE, TILE_SIZE) # CRUCIAL for later sprite-based rendering

    # --- Assign images to entities ---
    for player in game_state.party.members:
        player.image = images["player"][player.player_class]  # Use player class
        player.rect = pygame.Rect(player.x * TILE_SIZE, player.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)

    #Assign Images to Monsters.
    for row in game_state.current_map.tiles:
        for tile in row:
            if isinstance(tile, DungeonTile):
                for enemy in tile.enemies:
                    enemy.image = images["monster"][enemy.name]
                    enemy.rect = pygame.Rect(enemy.x*TILE_SIZE, enemy.y*TILE_SIZE, TILE_SIZE, TILE_SIZE)


    selected_inventory_index = 0
    menu_options = ["New Game", "Load Game", "Options", "Exit"]
    selected_menu_option = 0

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state.current_state == STATE_GAME:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game_state.party.move(0, -1, game_state.current_map)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game_state.party.move(0, 1, game_state.current_map)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game_state.party.move(-1, 0, game_state.current_map)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game_state.party.move(1, 0, game_state.current_map)
                    elif event.key == pygame.K_i:
                        game_state.current_state = STATE_INVENTORY
                        selected_inventory_index = 0
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                elif game_state.current_state == STATE_MENU:
                    if event.key == pygame.K_UP:
                        selected_menu_option = (selected_menu_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_menu_option = (selected_menu_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_menu_option == 0:
                            game_state.current_state = STATE_GAME
                        elif selected_menu_option == 1:
                            game_state.load_game()
                        elif selected_menu_option == 3:
                            running = False


        # --- Game Logic (State-Specific) ---
        if game_state.current_state == STATE_MENU:
            pass

        elif game_state.current_state == STATE_GAME:
            pass

        elif game_state.current_state == STATE_INVENTORY:
            while game_state.current_state == STATE_INVENTORY:
                screen.fill(BLACK)
                render_inventory(screen, game_state.party, selected_inventory_index, font)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_state.current_state = STATE_GAME_OVER
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            selected_inventory_index = max(0, selected_inventory_index - 1)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if game_state.party.inventory:
                                selected_inventory_index = min(len(game_state.party.inventory) - 1, selected_inventory_index + 1)

                        elif event.key == pygame.K_RETURN:
                            item_names = list(game_state.party.inventory.keys())
                            if 0 <= selected_inventory_index < len(item_names):
                                selected_item = item_names[selected_inventory_index]
                                print(f"Selected item: {selected_item}")

                                add_to_combat_log("Select Action: 1.Equip 2.Use 3.Unequip 4.Return")
                                action_selected = True
                                while action_selected:
                                    screen.fill(BLACK)
                                    render_inventory(screen, game_state.party, selected_inventory_index, font)
                                    render_status_bar(screen, game_state.party, font)
                                    render_combat_log(screen,combat_log, font)
                                    pygame.display.flip()
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            running = False
                                            action_selected = False
                                            game_state.current_state = STATE_GAME_OVER
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_1:
                                                if selected_item in WEAPONS or selected_item in ARMOR:
                                                    add_to_combat_log("Select a player to equip to:")
                                                    for i, member in enumerate(game_state.party.members):
                                                        add_to_combat_log(f"{i + 1}. {member.name}")
                                                    choosing_player = True
                                                    while choosing_player:
                                                        screen.fill(BLACK)
                                                        render_inventory(screen, game_state.party, selected_inventory_index, font)
                                                        render_status_bar(screen, game_state.party, font)
                                                        render_combat_log(screen,combat_log, font)
                                                        pygame.display.flip()
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.QUIT:
                                                                running = False
                                                                choosing_player = False
                                                                action_selected = False
                                                                game_state.current_state = STATE_GAME_OVER
                                                            if event.type == pygame.KEYDOWN:
                                                                if pygame.K_1 <= event.key <= pygame.K_9:
                                                                    player_index = event.key - pygame.K_1
                                                                    if 0 <= player_index < len(game_state.party.members):
                                                                        selected_player = game_state.party.members[player_index]
                                                                        selected_player.equip_item(selected_item)
                                                                        game_state.party.remove_from_inventory(selected_item, 1)
                                                                        choosing_player = False
                                                                        action_selected = False
                                                                        game_state.current_state = STATE_GAME
                                                                    else:
                                                                        add_to_combat_log("Invalid player selection.")
                                                                        game_state.current_state = STATE_GAME
                                                                elif event.key == pygame.K_ESCAPE:
                                                                    choosing_player = False
                                                                    game_state.current_state = STATE_INVENTORY

                                                else:
                                                   add_to_combat_log("Cannot equip this item.")
                                                   action_selected = False
                                                   game_state.current_state = STATE_GAME


                                            elif event.key == pygame.K_2:
                                                if selected_item in ITEMS:
                                                    add_to_combat_log("Select a player to use the item on:")
                                                    for i, member in enumerate(game_state.party.members):
                                                        add_to_combat_log(f"{i + 1}. {member.name}")
                                                    choosing_player = True
                                                    while choosing_player:
                                                        screen.fill(BLACK)
                                                        render_inventory(screen, game_state.party, selected_inventory_index, font)
                                                        render_status_bar(screen, game_state.party, font)
                                                        render_combat_log(screen,combat_log, font)
                                                        pygame.display.flip()
                                                        for event in pygame.event.get():
                                                            if event.type == pygame.QUIT:
                                                                running = False
                                                                choosing_player = False
                                                                action_selected = False
                                                                game_state.current_state = STATE_GAME_OVER
                                                            if event.type == pygame.KEYDOWN:
                                                                if pygame.K_1 <= event.key <= pygame.K_9:
                                                                    player_index = event.key - pygame.K_1
                                                                    if 0 <= player_index < len(game_state.party.members):
                                                                        selected_player = game_state.party.members[player_index]
                                                                        selected_player.use_item(selected_item, selected_player)
                                                                        game_state.party.remove_from_inventory(selected_item, 1)
                                                                        choosing_player = False
                                                                        action_selected = False
                                                                        game_state.current_state = STATE_GAME
                                                                    else:
                                                                        add_to_combat_log("Invalid player selection")
                                                                        game_state.current_state = STATE_GAME
                                                                elif event.key == pygame.K_ESCAPE:
                                                                    choosing_player = False
                                                                    game_state.current_state = STATE_INVENTORY
                                                else:
                                                    add_to_combat_log("Cannot use this item.")
                                                    action_selected = False
                                                    game_state.current_state = STATE_GAME


                                            elif event.key == pygame.K_3:
                                                add_to_combat_log("Select a player to unequip from:")
                                                for i, member in enumerate(game_state.party.members):
                                                    add_to_combat_log(f"{i + 1}. {member.name}")
                                                choosing_player = True
                                                while choosing_player:
                                                    screen.fill(BLACK)
                                                    render_inventory(screen, game_state.party, selected_inventory_index, font)
                                                    render_status_bar(screen, game_state.party, font)
                                                    render_combat_log(screen,combat_log, font)
                                                    pygame.display.flip()
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            running = False
                                                            choosing_player = False
                                                            action_selected = False
                                                            game_state.current_state = STATE_GAME_OVER
                                                        if event.type == pygame.KEYDOWN:
                                                            if pygame.K_1 <= event.key <= pygame.K_9:
                                                                player_index = event.key - pygame.K_1
                                                                if 0 <= player_index < len(game_state.party.members):
                                                                    selected_player = game_state.party.members[player_index]
                                                                    add_to_combat_log("Select item to unequip")
                                                                    add_to_combat_log("1. Weapon")
                                                                    add_to_combat_log("2. Armor")
                                                                    unequip_loop = True
                                                                    while unequip_loop:
                                                                        screen.fill(BLACK)
                                                                        render_inventory(screen, game_state.party, selected_inventory_index, font)
                                                                        render_status_bar(screen, game_state.party, font)
                                                                        render_combat_log(screen,combat_log, font)
                                                                        pygame.display.flip()
                                                                        for event in pygame.event.get():
                                                                            if event.type == pygame.QUIT:
                                                                                running = False
                                                                                unequip_loop = False
                                                                                choosing_player = False
                                                                                action_selected = False
                                                                                game_state.current_state = STATE_GAME_OVER
                                                                            if event.type == pygame.KEYDOWN:
                                                                                if event.key == pygame.K_1:
                                                                                    if selected_player.equipped_weapon:
                                                                                        item_name = selected_player.equipped_weapon["name"]
                                                                                        selected_player.unequip_item(item_name)
                                                                                        game_state.party.add_to_inventory(item_name, 1)
                                                                                    else:
                                                                                        add_to_combat_log("No weapon equipped.")
                                                                                    unequip_loop = False
                                                                                    choosing_player = False
                                                                                    action_selected = False
                                                                                    game_state.current_state = STATE_GAME
                                                                                elif event.key == pygame.K_2:
                                                                                    if selected_player.equipped_armor:
                                                                                        item_name = selected_player.equipped_armor["name"]
                                                                                        selected_player.unequip_item(item_name)
                                                                                        game_state.party.add_to_inventory(item_name, 1)
                                                                                    else:
                                                                                        add_to_combat_log("No armor equipped")
                                                                                    unequip_loop = False
                                                                                    choosing_player = False
                                                                                    action_selected = False
                                                                                    game_state.current_state = STATE_GAME
                                                                                elif event.key == pygame.K_ESCAPE:
                                                                                    unequip_loop = False
                                                                                    choosing_player = False
                                                                                    game_state.current_state = STATE_INVENTORY
                                                            else:
                                                                add_to_combat_log("Invalid player selection.")
                                                                game_state.current_state = STATE_GAME
                                                        elif event.key == pygame.K_ESCAPE:
                                                                choosing_player = False
                                                                game_state.current_state = STATE_INVENTORY

                                        elif event.key == pygame.K_4 or event.key == pygame.K_ESCAPE:
                                            action_selected = False
                                            game_state.current_state = STATE_GAME

                        elif event.key == pygame.K_ESCAPE:
                            game_state.current_state = STATE_GAME

        elif game_state.current_state == STATE_COMBAT:
            pass

        elif game_state.current_state == STATE_GAME_OVER:
            # Game over screen/logic could be added here
            break

        # --- Drawing (Outside of State Checks) ---
        screen.fill(BLACK)  # Clear the entire screen

        if game_state.current_state == STATE_GAME:
            render_dungeon(screen, game_state.current_map, game_state.party)  # Pass the current map
            render_status_bar(screen, game_state.party, font)
            render_combat_log(screen, combat_log, font)
        elif game_state.current_state == STATE_MENU:
            render_main_menu(screen, font, selected_menu_option)
        # Other states (shop, combat, etc.) would have their own rendering calls here.

        pygame.display.flip()  # Update the full display
        clock.tick(FPS)  # Limit frame rate

    pygame.quit()

# --- Dictionary Definitions (Moved after classes) ---
# These need to be *after* the class definitions, as they are used in the classes.

CLASS_STATS = {
    "Warrior": {
        "Strength": 7,
        "Agility": 4,
        "Intelligence": 1,
        "Wisdom": 2,
        "Dexterity": 5,
        "Luck": 3,
        "Charisma": 4,
        "max_hp": 100,
        "max_mana": 20,
    },
    "Rogue": {
        "Strength": 4,
        "Agility": 7,
        "Intelligence": 3,
        "Wisdom": 1,
        "Dexterity": 6,
        "Luck": 5,
        "Charisma": 2,
        "max_hp": 80,
        "max_mana": 30,
    },
    "Mage": {
        "Strength": 2,
        "Agility": 3,
        "Intelligence": 8,
        "Wisdom": 6,
        "Dexterity": 4,
        "Luck": 1,
        "Charisma": 5,
        "max_hp": 60,
        "max_mana": 100,
    },
}

CLASS_LEVEL_UP_STATS = {
    "Warrior": {
        "Strength": 4,
        "Agility": 2,
        "Intelligence": 1,
        "Wisdom": 1,
        "Dexterity": 2,
        "Luck": 1,
        "Charisma": 1,
        "max_hp": 15,
        "max_mana": 5,
    },
    "Rogue": {
        "Strength": 2,
        "Agility": 4,
        "Intelligence": 1,
        "Wisdom": 1,
        "Dexterity": 3,
        "Luck": 2,
        "Charisma": 1,
        "max_hp": 10,
        "max_mana": 10,
    },
    "Mage": {
        "Strength": 1,
        "Agility": 1,
        "Intelligence": 4,
        "Wisdom": 3,
        "Dexterity": 1,
        "Luck": 1,
        "Charisma": 2,
        "max_hp": 5,
        "max_mana": 15,
    },
}

CLASS_ABILITIES = {
    "Warrior": ["Attack", "Power Attack", "Defensive Stance"],
    "Rogue": ["Attack", "Sneak Attack", "Evade"],
    "Mage": ["Attack", "Fireball", "Heal"],
}

ABILITIES = {
    "Attack": {
        "type": "attack",
        "power_multiplier": 1.0,
        "mana_cost": 0,
        "description": "A basic attack.",
    },
    "Power Attack": {
        "type": "attack",
        "power_multiplier": 1.5,
        "mana_cost": 5,
        "description": "A strong attack.",
    },
    "Defensive Stance": {
        "type": "buff",
        "stat": "defense",
        "amount": 5,
        "duration": 3,
        "mana_cost": 5,
        "description": "Increases defense.",
    },
    "Sneak Attack": {
        "type": "attack",
        "power_multiplier": 2.0,
        "mana_cost": 8,
        "description": "A precise attack.",
    },
    "Evade": {
        "type": "buff",
        "stat": "evasion",
        "amount": 10,
        "duration": 2,
        "mana_cost": 7,
        "description": "Increases evasion.",
    },
    "Fireball": {
        "type": "attack",
        "power_multiplier": 1.8,
        "mana_cost": 12,
        "description": "A fiery blast.",
    },
    "Heal": {
        "type": "heal",
        "heal_amount": 25,
        "mana_cost": 10,
        "description": "Restores health.",
    },
}

WEAPONS = {
    "Sword": {"name": "Sword", "type": "weapon", "attack": 5, "Strength": 2},
}

ARMOR = {
    "Plate Armor": {"name": "Plate Armor", "type": "armor", "defense": 5, "Strength": 3},
}

ITEMS = {
    "Health Potion": {"name": "Health Potion", "type": "consumable", "effect": "heal", "amount": 20},
}

MONSTERS = {
    "Goblin": {
        "name": "Goblin",
        "Strength": 2,
        "Agility": 3,
        "Intelligence": 1,
        "Wisdom": 1,
        "Dexterity": 3,
        "Luck": 1,
        "Charisma": 1,
        "max_hp": 25,
        "max_mana": 10,
        "level": 1,
        "xp_reward": 10,
        "gold_reward": 5,
        "abilities": ["Attack", "Scratch"],
        "drops": [("Gold", 100), ("Health Potion", 50)],
        "inventory": {},
    },
}

MONSTER_ABILITIES = {
    "Attack": {
        "type": "attack",
        "power_multiplier": 1.0,
        "mana_cost": 0,
        "description": "A basic attack.",
    },
    "Scratch": {
        "type": "attack",
        "power_multiplier": 1.1,
        "mana_cost": 0,
        "description": "A weak scratch.",
    },
}
# --- Main Entry Point ---

if __name__ == "__main__":
    game_loop()