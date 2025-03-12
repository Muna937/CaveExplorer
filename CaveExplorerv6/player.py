# player.py

# Goals:
#   - Represent the player character in the game.
#   - Store player-specific attributes (name, stats, inventory, skills, etc.).
#   - Handle player movement (the actual movement logic).
#   - Interact with other game systems (combat, inventory).
#  - Load Character Class Data

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:
#       - Created and managed by the Game class.
#       - Game.update() calls Player.update().
#        - Receives movement commands from Game.
#   - inventory.py: Has an Inventory instance for managing items.
#   - combat.py: Participates in combat encounters.
#   - skills.py: Uses and manages player skills.
#   - data/character_classes.json: Loads base stats and starting skills from here.
#   - ui/screens/game_screen.py: (Indirectly)  game.py handles input and updates player position.
#   - save_load.py: Player data is saved and loaded as part of the game state.
#   - skills.py:  Loads and interacts with Skill objects.
#  - utils.py: Used for loading json data.

from entity import Entity
from inventory import Inventory
from skills import Skill  # Import the Skill class
from utils import load_json_data #for loading class data.

class Player(Entity):  # Inherit from Entity
    def __init__(self, name, x, y, character_class):
        super().__init__(x, y, health=100, name=name)  # Call the Entity constructor
        self.inventory = Inventory()
        self.skills = {}  #  store skills (e.g., {"Fireball": FireballSkill()}).
        self.gold = 0
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.load_class_data()
        # ... other player-specific attributes ...

    def update(self, dt):
        super().update(dt) # Call the Entity update method (if needed).

    def load_class_data(self):
        class_data, msg = load_json_data("data/character_classes.json")
        if class_data:
            class_info = class_data["classes"].get(self.character_class)
            if class_info:
                self.base_stats = class_info["base_stats"]
                #Initialize stats based on class data
                self.strength = self.base_stats["strength"]
                self.dexterity = self.base_stats["dexterity"]
                self.constitution = self.base_stats["constitution"]
                self.intelligence = self.base_stats["intelligence"]
                self.wisdom = self.base_stats["wisdom"]
                self.charisma = self.base_stats["charisma"]
                self.max_hp = 50 + (self.constitution * 5) #Example formula
                self.health = self.max_hp
                for skill_id in class_info["starting_skills"]:
                    skill_data, msg = load_json_data("data/skills.json")
                    if skill_data:
                        skill_info = skill_data["skills"].get(skill_id)
                        if skill_info:
                           self.add_skill(skill_id, Skill(skill_info['name'], skill_info['description'], skill_info['cost'], skill_info['effect']))
                    else:
                      print(msg) #Error handle

            else:
                print(f"Error: Class data not found for class '{self.character_class}'")
        else:
            print(msg) #Error handle loading json.

    def move(self, dx, dy):
        # Handle player movement.  The actual collision check is done in game.py now.
        self.x += dx
        self.y += dy

    def add_gold(self, amount):
        self.gold += amount

    def remove_gold(self, amount):
        if(self.gold >= amount):
            self.gold -= amount
            return True
        else:
            print("Not enough gold") #Or handle however
            return False

    def add_to_inventory(self, item):
        return self.inventory.add_item(item)

    def remove_from_inventory(self, item):
        return self.inventory.remove_item(item)

    def add_skill(self, skill_name, skill:Skill):
        self.skills[skill_name] = skill

    # ... other player-specific methods (use_item, learn_skill, etc.) ...