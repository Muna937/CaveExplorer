# npc.py

# Goals:
#   - Represent a Non-Player Character (NPC) in the game.
#   - Store NPC-specific attributes (dialogue ID, merchant status, inventory).
#   - Handle NPC behavior (currently, just starting dialogue).
#   - Inherit common attributes and methods from Entity.

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:
#       - Creates and manages NPC instances.
#       - Calls npc.interact() when the player interacts with the NPC.
#   - world.py:  Gets NPC positions from the map data during map loading.
#   - data/dialogue/:  Uses the dialogue ID to load dialogue data (indirectly, through game.py).
#   - data/npcs.json:  Gets NPC data (name, sprite, dialogue ID, etc.).
#   - ui/screens/dialogue_screen.py:  Used to initiate dialogue with the NPC.
#   - save_load.py: (Eventually) Saves and loads NPC state.

from entity import Entity

class NPC(Entity):
    def __init__(self, npc_id, name, x, y, dialogue_id, is_merchant=False, inventory=None):
        super().__init__(x, y, health=1, name=name)  # NPCs might not have health, so a default of 1
        self.npc_id = npc_id
        self.dialogue_id = dialogue_id  # This is the important part
        self.is_merchant = is_merchant
        self.inventory = inventory or []  # Use an empty list if no inventory is provided
        self.is_alive = False # Ensure NPCs aren't targeted in combat, etc.

    def interact(self, player, game):
        # Handle interaction with the player (start dialogue).
        game.show_dialogue_screen() #now passing in game object


    def update(self, dt):
        # Handle NPC-specific updates (e.g., AI, movement).
        super().update(dt)
        pass