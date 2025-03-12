# player.py

# Goals:
#   - Represent the player character in the game.
#   - Store player-specific attributes (name, stats, inventory, skills, etc.).
#   - Handle player movement and actions.
#   - Interact with other game systems (combat, inventory).

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:
#       - Created and managed by the Game class.
#       - Game.update() calls Player.update().
#   - inventory.py: Has an Inventory instance for managing items.
#   - combat.py: Participates in combat encounters.
#   - skills.py (potentially): Uses and manages player skills.
#   - ui/screens/game_screen.py (indirectly):
#     - The game screen will display player information (health, inventory, etc.) and receive player input and will get this indirectly through game.py.
#   - save_load.py: Player data is saved and loaded as part of the game state.

# Example Structure:
from entity import Entity
from inventory import Inventory

class Player(Entity):  # Inherit from Entity
    def __init__(self, name, x, y):
        super().__init__(x, y, health=100, name=name)  # Call the Entity constructor
        self.inventory = Inventory()  # Give the player an inventory.
        self.skills = {}  #  store skills (e.g., {"Fireball": FireballSkill()}).
        self.gold = 0 # Example of a player-specific attribute.
        # ... other player-specific attributes (experience, level, etc.) ...

    def update(self, dt):
        # Handle player-specific updates (e.g., input, animations).
        super().update(dt) # Call the Entity update method.
        # Example: Handle input (replace with your actual input handling).
        # if check_key_pressed("up"):
        #     self.move(0, -1)
        pass;

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

    # ... other player-specific methods (use_item, learn_skill, etc.) ...
    