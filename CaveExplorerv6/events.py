# events.py

# Goals:
#   - Define a system for handling game events (e.g., triggers, cutscenes, timed events).
#   - Provide a way to trigger events based on conditions (player location, quest progress, etc.).
#   - Allow for events to have various effects (start dialogue, spawn monsters, change map, etc.).
#   - Decouple event triggers from event effects (making the system more flexible).

# Interactions:
#   - game.py: The game loop checks for and processes events.
#   - world.py (potentially): Events might be triggered by entering specific areas of the map.
#   - quests.py (potentially): Events might be tied to quest progress.
#   - player.py (potentially): Events might be triggered by player actions.
#   - Any other part of the game that needs to trigger or respond to events.

# Example Structure:

class Event:
    def __init__(self, event_id, trigger_type, condition, actions):
        self.event_id = event_id  # Unique identifier for the event.
        self.trigger_type = trigger_type  # e.g., "location", "quest_update", "timed"
        self.condition = condition  # A function or data that defines when the event is triggered.
        self.actions = actions  # A list of actions to perform when the event is triggered.
        self.has_triggered = False #prevent repeats

    def check_trigger(self, game):
        # Check if the event's trigger condition is met.
        if self.trigger_type == "location":
            # Example: Check if player is at a specific location.
            if game.player.x == self.condition["x"] and game.player.y == self.condition["y"]:
                return True
        elif self.trigger_type == "quest_update":
            # Example: Check if a specific quest is complete.
            pass #check quest
        elif self.trigger_type == "timed":
            # Example: Check if a certain amount of time has passed.
            pass #check time
        # Add more trigger types as needed...
        return False

    def execute_actions(self, game):
        # Perform the actions associated with the event.
      if self.has_triggered:
        return #don't repeat.

      for action in self.actions:
          if action["type"] == "dialogue":
              # Example: Start dialogue with an NPC.
              game.start_dialogue(action["npc_id"])
          elif action["type"] == "spawn_monster":
              # Example: Spawn a monster.
              pass
          elif action["type"] == "change_map":
              # Example: Change to a different map.
              pass
          elif action["type"] == "give_item":
            # Example give the player an item
            pass
          # Add more action types as needed...
      self.has_triggered = True #set triggered.


# --- Example Events (you'd likely load these from a JSON file) ---

events = {
    "enter_town_square": Event(
        event_id="enter_town_square",
        trigger_type="location",
        condition={"x": 10, "y": 10},  # Example coordinates
        actions=[
            {"type": "dialogue", "npc_id": "old_man_town"},
        ]
    ),
    # ... more events ...
}

def update_events(game, dt):
  # Check all events and execute actions if triggered.
  for event_id, event in events.items():
    if event.check_trigger(game):
      event.execute_actions(game)

# --- Example Usage (in game.py) ---
# in game.py's update()
# events.update_events(game, dt)