# npc.py

# Goals:
#   - Represent a Non-Player Character (NPC) in the game.
#   - Store NPC-specific attributes (dialogue ID, merchant status, inventory).
#   - Handle NPC behavior (movement, interaction).

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:  Creates and manages NPC instances.
#   - world.py:  Gets NPC positions from the map data.
#   - data/dialogue/:  Uses the dialogue ID to load dialogue data.
#   - data/npcs.json:  Gets NPC data (name, sprite, etc.).
#   - ui/screens/dialogue_screen.py:  Used to initiate dialogue with the NPC.
#   - save_load.py: Saves and loads NPC state.

from entity import Entity

class NPC(Entity):
    def __init__(self, npc_id, name, x, y, dialogue_id, is_merchant=False, inventory=None):
        super().__init__(x, y, health=1, name=name) # NPCs might not have health, so a default of 1
        self.npc_id = npc_id
        self.dialogue_id = dialogue_id
        self.is_merchant = is_merchant
        self.inventory = inventory or []  # Use an empty list if no inventory is provided
        self.is_alive = False #Don't show on map.

    def interact(self, player):
        # Handle interaction with the player (e.g., start dialogue, open shop).
        pass  # Implement interaction logic here (dialogue, shop, etc.)

    def update(self, dt):
        # Handle NPC-specific updates (e.g., AI, movement).
        super().update(dt) #call entity update
        pass

# Example Usage (in world.py or game.py):
# npc_data = load_json_data("data/npcs.json")["npcs"]["old_man_town"]
# npc = NPC(
#    npc_id="old_man_town",
#     name=npc_data["name"],
#    x=npc_data["position"]["x"],
#    y=npc_data["position"]["y"],
#    dialogue_id=npc_data["dialogue"],
#    is_merchant=npc_data["is_merchant"],
#     inventory=npc_data.get("inventory", []) # Handle cases where inventory might not exist

# )