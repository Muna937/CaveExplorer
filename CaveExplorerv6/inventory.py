# inventory.py

# Goals:
#   - Manage the player's (or an entity's) inventory.
#   - Add items to the inventory.
#   - Remove items from the inventory.
#   - Check if an item is present in the inventory.
#   - Get a list of items in the inventory.
#   - Organize the inventory (e.g., by item type, slots).
#   - Handle item stacking (multiple potions of the same type).
#   - Implement inventory capacity limits.
#   - **Count the quantity of a specific item ID.**

# Interactions:
#   - player.py: The Player class will likely have an Inventory instance.
#   - game.py:
#       - May call inventory methods when the player picks up items.
#       - May check the inventory for quest items.
#   - item.py: Uses the Item class to represent items.
#   - items.json (indirectly): Uses item data to create Item instances.
#   - combat.py (potentially):  If items can be used in combat.
#   - ui/screens/inventory_screen.py: Displays and interacts with the inventory.
#   - save_load.py: The inventory needs to be saved and loaded.
#   - quests.py:  Checks inventory for quest items ("collect" objectives).

class Inventory:
    def __init__(self, capacity=20):  # Increased default capacity
        self.items = []
        self.capacity = capacity

    def add_item(self, item):
        if len(self.items) < self.capacity:
            # Check for stacking
            if item.stackable:
                for existing_item in self.items:
                    if existing_item.item_id == item.item_id:
                        if existing_item.quantity < existing_item.max_stack:
                            existing_item.quantity += item.quantity  # Add to the stack
                            return True  # Indicate success
                        #If the item stack is already maxed out, continue to attempt to add to a new slot.

            # Not stackable or no existing stack, add as a new item
            self.items.append(item)
            return True
        else:
            print("Inventory is full!")
            return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            print(f"{item.name} not found in inventory.")  # Or handle better
            return False

    def has_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return True
        return False

    def get_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def get_items(self):
        return self.items

    def clear_inventory(self):
        self.items = []

    def count_item(self, item_id):
        """Counts how many of a specific item are in the inventory."""
        count = 0
        for item in self.items:
            if item.item_id == item_id:
                count += item.quantity  # Use item.quantity
        return count