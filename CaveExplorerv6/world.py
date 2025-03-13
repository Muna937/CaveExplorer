# world.py

# Goals:
#   - Load and manage the game world (map data).
#   - Create and manage Tile objects based on map data.
#   - Create and manage NPC, Monster, and Item instances on the map, based on map data.
#   - Handle collision detection (using Tile.walkable).
#   - Manage map transitions (loading different maps).  Currently loads initial map.
#   - Update the state of dynamic elements on the map (NPCs, monsters).  Calls their update() methods.
#   - Provide is_tile_walkable() for collision checks.

# Interactions:
#   - game.py:
#       - Game.update() calls World.update().
#       - Game gets information about the map (tiles, NPCs, monsters, items) from World.
#       - Game calls check_move() which uses is_tile_walkable().
#   - data/maps/: Loads map data from JSON files.
#   - tile.py: Creates Tile instances.
#   - npc.py: Creates NPC instances.
#   - monster.py: Creates Monster instances.
#   - item.py: Creates Item instances.
#   - ui/screens/game_screen.py: Renders the map, NPCs, monsters, and items (using data provided by World).
#   - utils.py: Uses utility functions (e.g., for loading JSON data).
#   - player.py: Used for collision detection (indirectly, via game.py).
#   - save_load.py:  Will need to handle saving/loading the *state* of NPCs, monsters, and items on the map.
# - combat.py

from tile import Tile
from npc import NPC
from monster import Monster
from item import Item, Consumable, Weapon, Armor  # Import Item classes
from utils import load_json_data
import os
from constants import *

class World:
    def __init__(self):
        self.map_data = None
        self.current_map_name = "town"  # Example: Start in the "town" map.
        self.tile_size = TILE_SIZE
        self.tiles = []  # Store Tile objects
        self.npcs = {}     # Store NPC instances {npc_id: NPC object}
        self.monsters = []  # Store Monster instances
        self.items = [] # Store Item instances
        self.load_map(self.current_map_name)

    def load_map(self, map_name):
        map_filepath = os.path.join("data", "maps", f"{map_name}.json")
        self.map_data, error_message = load_json_data(map_filepath)
        if error_message:
            print(error_message)
            return False, error_message

        # --- Tile Creation ---
        self.tiles = []  # Clear previous tiles
        for row_index, row in enumerate(self.map_data["tiles"]):
            tile_row = []
            for col_index, tile_id in enumerate(row):
                # Tile Mapping Logic (ONLY WALLS AND FLOORS)
                if tile_id == 0:
                    tile = Tile(tile_id, walkable=False, image_path="assets/images/tiles/wall.png")
                elif tile_id == 1:
                    tile = Tile(tile_id, walkable=True, image_path="assets/images/tiles/floor.png")
                else:  # Default to walkable floor (for now)
                    tile = Tile(tile_id, walkable=True, image_path="assets/images/tiles/floor.png")
                tile_row.append(tile)
            self.tiles.append(tile_row)

        # --- NPC Creation ---
        self.npcs = {} # Clear existing NPC instances
        if "npcs" in self.map_data:
          npc_data, msg = load_json_data("data/npcs.json") #load npc data
          if npc_data:
            npc_data = npc_data['npcs'] #get the inner dictionary
            for npc_id, npc_pos in self.map_data["npcs"].items():
                if npc_id in npc_data:
                  npc_info = npc_data[npc_id]
                  self.npcs[npc_id] = NPC(
                      npc_id=npc_id,
                      name=npc_info["name"],
                      x=npc_pos["x"],
                      y=npc_pos["y"],
                      dialogue_id=npc_info["dialogue"],
                      is_merchant=npc_info.get("is_merchant", False),  # Use .get()
                      inventory=npc_info.get("inventory", [])  # Use .get()
                  )
                else:
                  print(f"NPC ID {npc_id} not found in npcs.json") #Error Handle
          else:
            print(msg) #Error Handle


        # --- Monster Creation ---
        self.monsters = []  # Clear existing instances
        if "monsters" in self.map_data:
          monsters_data, msg = load_json_data("data/monsters.json")
          if monsters_data:
            monsters_data = monsters_data['monsters']
            for monster_spawn in self.map_data["monsters"]:
                monster_type = monster_spawn["type"]
                if monster_type in monsters_data:
                    monster_info = monsters_data[monster_type]
                    self.monsters.append(Monster(
                          monster_id = monster_type,
                          name=monster_info["name"],
                          x=monster_spawn["x"],
                          y=monster_spawn["y"],
                          hp=monster_info["hp"],
                          max_hp = monster_info["max_hp"],
                          attack=monster_info["attack"],
                          defense=monster_info["defense"],
                          speed = monster_info["speed"],
                          experience = monster_info["experience"],
                          gold_drop = monster_info["gold_drop"],
                          drops=monster_info["drops"],
                          sprite=monster_info["sprite"],
                          ai = monster_info["ai"],
                          resistances = monster_info.get("resistances",{}),
                          weaknesses = monster_info.get("weaknesses",{})
                    ))
                else:
                    print(f"Monster ID {monster_type} not found in monsters.json.")
          else:
            print(msg) #Error handle

        # --- Item Creation ---
        self.items = []  # Clear existing
        if "items" in self.map_data:
          items_data, msg = load_json_data("data/items.json")
          if items_data:
            items_data = items_data['items']
            for item_spawn in self.map_data["items"]:
                item_type = item_spawn["type"]
                if item_type in items_data:
                    item_info = items_data[item_type]
                    if item_info["type"] == "consumable":
                      item = Consumable(
                        item_id = item_type,
                        name = item_info["name"],
                        item_type = item_info["type"],
                        description = item_info["description"],
                        value = item_info["value"],
                        stackable = item_info["stackable"],
                        max_stack = item_info["max_stack"],
                        icon = item_info["icon"],
                        effect = item_info["effect"],
                        quantity = item_spawn["quantity"]
                      )
                    elif item_info["type"] == "weapon":
                      item = Weapon(
                        item_id = item_type,
                        name = item_info["name"],
                        item_type = item_info["type"],
                        description = item_info["description"],
                        value = item_info["value"],
                        stackable = item_info["stackable"],
                        max_stack = item_info["max_stack"],
                        icon = item_info["icon"],
                        weapon_type = item_info["weapon_type"],
                        attack = item_info["attack"],
                        durability = item_info["durability"],
                        max_durability = item_info["max_durability"],
                        requirements = item_info["requirements"],
                        effects = item_info["effects"],
                        quantity = item_spawn["quantity"]
                      )
                    elif item_info["type"] == "armor":
                      item = Armor(
                        item_id = item_type,
                        name = item_info["name"],
                        item_type = item_info["type"],
                        description = item_info["description"],
                        value = item_info["value"],
                        stackable = item_info["stackable"],
                        max_stack = item_info["max_stack"],
                        icon = item_info["icon"],
                        armor_type = item_info["armor_type"],
                        defense = item_info["defense"],
                        durability = item_info["durability"],
                        max_durability = item_info["max_durability"],
                        requirements = item_info["requirements"],
                        effects = item_info["effects"],
                        quantity = item_spawn["quantity"]
                      )
                    else: # Fallback to generic item
                      item = Item(
                        item_id = item_type,
                        name = item_info["name"],
                        item_type = item_info["type"],
                        description = item_info["description"],
                        value = item_info["value"],
                        stackable = item_info["stackable"],
                        max_stack = item_info["max_stack"],
                        icon = item_info["icon"],
                        quantity = item_spawn["quantity"]
                      )
                    item.x = item_spawn["x"]
                    item.y = item_spawn["y"]
                    self.items.append(item)

            else:
              print(f"Item type not found in items.json {item_type}") #error handle
          else:
            print(msg) #error handle
        return True, ""

    def update(self, dt):
        for npc in self.npcs.values():  # Iterate through NPC *instances*
            npc.update(dt)
        for monster in self.monsters:
            monster.update(dt)
        # Items usually don't need updating, unless they have some active effect

    def is_tile_walkable(self, x, y):
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        if not self.map_data: # ADD THIS CHECK!
            return False
        if 0 <= tile_y < len(self.tiles) and 0 <= tile_x < len(self.tiles[0]):
            return self.tiles[tile_y][tile_x].walkable
        else:
            return False
    def change_map(self, map_name):
      success, message = self.load_map(map_name)
      if success:
        self.current_map_name = map_name
      return success, message

    def render(self, screen): #Placeholder
      pass