# inventory.py

# Goals:
#   - Manage the player's (or an entity's) inventory.
#   - Add items to the inventory.
#   - Remove items from the inventory.
#   - Check if an item is present in the inventory.
#   - Get a list of items in the inventory.
#   - (Optionally) Organize the inventory (e.g., by item type, slots).
#   - (Optionally) Handle item stacking (e.g., multiple potions of the same type).
#   - (Optionally) Implement inventory capacity limits.

# Interactions:
#   - player.py: The Player class will likely have an Inventory instance.
#   - game.py:
#       - May call inventory methods when the player picks up items.
#       - May check the inventory for quest items.
#   - items.json (indirectly, likely via a data loading function in utils.py or game.py):
#      - The inventory will store item data, and the definitions of those items will come from a data file.
#   - combat.py (potentially):
#       - If items can be used in combat, combat.py might interact with the inventory.
#   - ui/screens/inventory_screen.py:
#       - The InventoryScreen will display the contents of the inventory and allow the player to interact with it.  It will get the inventory data from the Player object.
#   - save_load.py: The inventory needs to be saved and loaded as part of the game state.

# Example Structure:
class Inventory:
    def __init__(self, capacity=10):  # Default capacity of 10 slots
        self.items = []  # List to store item dictionaries.
        self.capacity = capacity

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True  # Indicate success
        else:
            print("Inventory is full!")  # Or handle this more gracefully (e.g., with a message to the player)
            return False  # Indicate failure

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            print(f"{item['name']} not found in inventory.") #or handle better
            return False

    def has_item(self, item_name):
        for item in self.items:
            if item["name"] == item_name: # Assumes each item has a "name" key
                return True
        return False
    
    def get_item(self, item_name):
        for item in self.items:
            if item["name"] == item_name:
                return item
        return None

    def get_items(self):
        return self.items  # Return the entire list of items

    def clear_inventory(self):
      self.items = []