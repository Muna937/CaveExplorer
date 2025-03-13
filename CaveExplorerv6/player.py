# player.py

# Goals:
#   - Represent the player character in the game.
#   - Store player-specific attributes (name, stats, inventory, skills, character class, level, experience, etc.)
#   - Handle player movement (the actual movement logic).
#   - Interact with other game systems (combat, inventory, skills, quests).
#   - Load character class data (base stats, starting skills) from JSON.
#   - Manage equipped items (weapons, armor) and their effects on stats.

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:
#       - Created and managed by the Game class.
#       - Game.update() calls Player.update().
#   - inventory.py: Has an Inventory instance for managing items.
#   - combat.py: Participates in combat encounters (calculates attack/defense).
#   - skills.py: Uses and manages player skills.
#   - data/character_classes.json: Loads base stats and starting skills.
#   - ui/screens/game_screen.py: (Indirectly) game.py handles input, updates player position.
#   - ui/screens/character_screen.py: (Indirectly) Displays player information.
#   - ui/screens/inventory_screen.py: (Indirectly) Manages inventory.
#   - save_load.py: Player data is saved and loaded.
#   - utils.py: Uses load_json_data.
#   - item.py:  Uses Item, Weapon, Armor, and Consumable classes.

from entity import Entity
from inventory import Inventory
from skills import Skill  # Import Skill class
from utils import load_json_data

class Player(Entity):
    def __init__(self, name, x, y, character_class):
        super().__init__(x, y, health=100, name=name)  # Initialize Entity
        self.inventory = Inventory()
        self.skills = {}
        self.gold = 0
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.load_class_data()
        # --- Equipment Slots (Example) ---
        self.equipped_weapon = None
        self.equipped_armor = None


    def update(self, dt):
        super().update(dt)  # Call Entity's update (if needed)
        # Add player-specific update logic here (e.g., check for level up)

    def load_class_data(self):
        class_data, msg = load_json_data("data/character_classes.json")
        if class_data:
            class_info = class_data["classes"].get(self.character_class)
            if class_info:
                self.base_stats = class_info["base_stats"]
                # Initialize stats based on class data
                self.strength = self.base_stats["strength"]
                self.dexterity = self.base_stats["dexterity"]
                self.constitution = self.base_stats["constitution"]
                self.intelligence = self.base_stats["intelligence"]
                self.wisdom = self.base_stats["wisdom"]
                self.charisma = self.base_stats["charisma"]
                self.max_health = 50 + (self.constitution * 5)  # Example formula
                self.health = self.max_health

                for skill_id in class_info["starting_skills"]:
                    skill_data, msg = load_json_data("data/skills.json")
                    if skill_data:
                      skill_info = skill_data["skills"].get(skill_id)
                      if skill_info:
                        self.add_skill(skill_id, Skill(skill_info['name'], skill_info['description'], skill_info['cost'], skill_info['effect'])) #add skill
                    else:
                      print(msg) #handle error
            else:
                print(f"Error: Class data not found for class '{self.character_class}'")
        else:
            print(msg)

    def move(self, dx, dy):
        # Handle player movement (collision is checked in game.py).
        self.x += dx
        self.y += dy

    def add_gold(self, amount):
        self.gold += amount

    def remove_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        else:
            print("Not enough gold!")
            return False

    def add_to_inventory(self, item):
        return self.inventory.add_item(item)

    def remove_from_inventory(self, item):
        return self.inventory.remove_item(item)

    def add_skill(self, skill_name, skill:Skill):
        self.skills[skill_name] = skill

    def get_attack(self):
        # Calculate attack power, taking equipped weapon into account.
        attack = self.strength  # Base attack on strength
        if self.equipped_weapon:
            attack += self.equipped_weapon.attack
        return attack

    def get_defense(self):
        # Calculate defense, taking equipped armor into account.
        defense = self.constitution  # Base defense on constitution
        if self.equipped_armor:
            defense += self.equipped_armor.defense
        return defense

    def equip_item(self, inventory_index):
      #Equip an item from the inventory
      if 0 <= inventory_index < len(self.inventory.items):
        item_to_equip = self.inventory.items[inventory_index]

        if item_to_equip.item_type == "weapon":
            if self.equipped_weapon:
                self.inventory.add_item(self.equipped_weapon)  # Add current weapon back
            self.equipped_weapon = item_to_equip
            self.inventory.remove_item(item_to_equip)
            print(f"Equipped {item_to_equip.name}")

        elif item_to_equip.item_type == "armor":
            if self.equipped_armor:
                self.inventory.add_item(self.equipped_armor)
            self.equipped_armor = item_to_equip
            self.inventory.remove_item(item_to_equip)
            print(f"Equipped {item_to_equip.name}")
        else:
          print("Cannot equip this item.")
      else:
        print("Invalid inventory index")
    def unequip_item(self, slot):
        # Unequip an item and return to inventory
        if slot == "weapon" and self.equipped_weapon:
            if self.inventory.add_item(self.equipped_weapon):
                self.equipped_weapon = None
                print("Unequipped weapon")
            else:
                print("Inventory full, cannot unequip.")

        elif slot == "armor" and self.equipped_armor:
            if self.inventory.add_item(self.equipped_armor):
                self.equipped_armor = None
                print("Unequipped armor")
            else:
                print("Inventory full, cannot unequip.")
    # ... other player-specific methods (use_item, learn_skill, level_up, etc.) ...