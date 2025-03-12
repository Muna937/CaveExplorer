# quests.py

# Goals:
#   - Define a Quest class to represent individual quests.
#   - Store quest information (name, description, objectives, rewards).
#   - Track quest progress (e.g., number of enemies killed, items collected).
#   - Check if quest objectives are complete.
#   - Provide methods for accepting, completing, and (optionally) abandoning quests.
#   - Manage a list of the player's active and completed quests.

# Interactions:
#   - game.py:
#       - Game might add quests to the player's quest log.
#       - Game checks for quest completion during updates.
#   - player.py (potentially, or through game.py):
#       - Player object might store a list of active/completed quests.
#   - ui/screens/quest_log_screen.py:
#       - Displays the player's quests and their progress.
#   - inventory.py (potentially):
#       - Quests might require collecting specific items.
#   - entity.py (potentially):
#       - Quests might require defeating specific enemies.
#   - data/quests.json (likely loaded via utils.py or game.py):
#       - Quest data (descriptions, objectives, rewards) would likely be loaded from a JSON file.
#   - save_load.py: Quest progress needs to be saved and loaded.

# Example Structure:

class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of Objective objects (see below).
        self.rewards = rewards  # Dictionary of rewards (e.g., {"gold": 100, "item": "Potion"}).
        self.is_complete = False
        self.is_active = False

    def check_completion(self):
        # Check if all objectives are complete.
        for objective in self.objectives:
            if not objective.is_complete:
                return False
        self.is_complete = True
        return True

    def complete_quest(self):
        # Mark the quest as complete and give rewards (likely handled by game.py).
      if self.is_complete:
        print(f"Quest '{self.name}' completed!")  # Replace with actual reward handling
        # game.player.add_gold(self.rewards.get("gold", 0))
        # ... other reward logic ...

    def start_quest(self):
      self.is_active = True
      print(f'Quest: "{self.name}" started!')

    def update(self, game):
      #update quest objectives if the quest is active.
      if self.is_active:
        for objective in self.objectives:
          objective.update(game)
        self.check_completion()

class Objective:  # Separate class for objectives
    def __init__(self, type, target, amount):
        self.type = type  # e.g., "kill", "collect", "reach"
        self.target = target  # e.g., "goblin", "potion", (x, y)
        self.amount = amount  # e.g., 10 (goblins), 3 (potions)
        self.current_amount = 0
        self.is_complete = False

    def update(self, game):
        # Update the objective's progress.
        if self.type == "kill":
            # Example: Check how many enemies of type 'target' have been killed.
            # This would likely involve interacting with the game.py or a separate
            #  'kill_tracker' object.  For now, we use a placeholder.
            # self.current_amount = game.get_kill_count(self.target) # Example

          pass #placeholder
        elif self.type == "collect":
            # Example: Check the player's inventory.
            if game.player.inventory.has_item(self.target):
                item = game.player.inventory.get_item(self.target)
                #Need a way to get item count here. Assuming item has quantity
                self.current_amount = item.get("quantity", 0)  # Placeholder for actual quantity.
        elif self.type == "reach":
          #Example: check if player is at location
          if game.player.x == self.target[0] and game.player.y == self.target[1]:
            self.current_amount = self.amount

        if self.current_amount >= self.amount:
            self.is_complete = True

# Example Usage (in game.py or a quest manager class):

# Define objectives
objective1 = Objective("kill", "goblin", 5)
objective2 = Objective("collect", "potion", 3)

# Define a quest
quest1 = Quest(
    name="Goblin Hunt",
    description="Eliminate 5 goblins and collect 3 potions.",
    objectives=[objective1, objective2],
    rewards={"gold": 50, "item": "Sword"}
)
#quest1.start_quest()  #would be activated on a trigger or through a function call.

# ... later, in the game loop ...
# quest1.update()
# if quest1.check_completion():
#     quest1.complete_quest()
#     # ... give rewards to player ...