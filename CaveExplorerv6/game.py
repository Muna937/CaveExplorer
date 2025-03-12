# game.py

# Goals:
#   - Initialize and manage the overall game state.
#   - Create and manage the player object.
#   - Load and manage the current game map and associated data (NPCs, monsters, items, quests).
#   - Handle the main game loop (updating game logic).
#   - Delegate input handling to the InputHandler.
#   - Manage player interactions with NPCs and the world (dialogue, combat).
#   - Coordinate saving and loading of the game.
#   - Track monster kill counts.
#   - Provide access to loaded item data.
#   - Integrate with the quest system (load quests, update quests).
#   - Add quest-related methods (start_quest, complete_quest).
#   - Handle dialogue actions.
#  - Switch to combat and back

# Interactions:
#   - app.py: The App class creates the Game instance.
#   - player.py: Creates and manages the Player object.
#   - world.py: Loads and updates the game world (map, NPCs, monsters, items).
#   - combat.py: Initiates and manages combat encounters.
#   - inventory.py: Accesses and modifies the player's inventory (through Player).
#   - quests.py: Updates quest progress, loads quest data.
#   - ui/screens/game_screen.py: Displays the game world.
#   - ui/screens/dialogue_screen.py: Starts dialogue with NPCs.
#   - ui/screens/combat_screen.py: Starts combat.
#   - save_load.py: Saves and loads the game state.
#   - entity.py: Uses Entity as a base class for Player, NPC, Monster.
#   - utils.py: Uses utility functions (load_json_data).
#   - npc.py: Interacts with NPCs.
#   - monster.py: Interacts with monsters.
#   - item.py: Handles item interactions (pickup).
#   - kivy.core.window:  Indirectly, via InputHandler.
#   - input_handler.py: Receives processed input events.
#   - App: Gets the kivy app instance.
#   - skills.py:  (Indirectly) Through Player and Combat
#   - quests.py: Loads quest data.
#   - data/items.json: Loads item data.
#   - data/quests.json: Loads in quest information.

from player import Player
from world import World
from kivy.app import App  # For getting the ScreenManager
from combat import Combat
import quests  # Import the quests module
from utils import load_json_data

class Game:
    def __init__(self):
        self.player = Player(name="Hero", x=5, y=5, character_class="warrior")  # Initial position
        self.world = World()
        self.is_running = True
        self.current_npc = None  # Track the NPC we are interacting with.
        self.combat = None
        self.quests = {}       # Dictionary to store quest instances, {quest_id: Quest object}
        self.kill_counts = {}  # Dictionary to track monster kills {monster_id: count}
        self.load_item_data() # Load item data.
        self.load_quests()    # Load quest data.


    def update(self, dt):
        if not self.is_running:
            return

        if self.combat:
          self.combat.update(dt)
          if self.combat.is_combat_over:
            #Combat is over, handle result, and return to game
            self.combat = None
            self.show_game_screen()

        else:
          #Regular game update
          self.player.update(dt)  # Update player (for things like animation)
          self.world.update(dt)   # Update world (NPCs, monsters, timed events)
          self.update_quests(dt) # Update quests

          for npc_id, npc in self.world.npcs.items():
              if self.player.x == npc.x and self.player.y == npc.y:
                  self.current_npc = npc
                  break
          else:
              self.current_npc = None

          for monster in self.world.monsters:
              if self.player.x == monster.x and self.player.y == monster.y:
                  self.start_combat(monster) #start combat
                  break

          items_to_remove = []
          for item in self.world.items:
              if self.player.x == item.x and self.player.y == item.y:
                  if self.player.add_to_inventory(item):
                    items_to_remove.append(item)
          for item in items_to_remove:
              self.world.items.remove(item)


    def check_move(self, dx, dy):
        if self.player:
            new_x = self.player.x + dx
            new_y = self.player.y + dy
            if self.world.is_tile_walkable(new_x * self.world.tile_size, new_y * self.world.tile_size):
                self.player.move(dx, dy)


    def handle_interaction(self):
      if self.current_npc:
        self.current_npc.interact(self.player, self) #now passing in game object

    def start_dialogue(self, npc_id):
        app = App.get_running_app()
        if app and app.root:
            app.root.get_screen('dialogue').start_dialogue(npc_id)

    def start_combat(self, monster):
        # self.combat_instance = Combat([self.player] + enemies_nearby)
        # self.combat_instance.start_combat()
        # while not self.combat_instance.is_combat_over():
        #   self.combat_instance.update(dt) # You might need a separate dt or a way to pause the main loop
        # results = self.combat_instance.get_results()
        # ... handle combat results ...
        self.combat = Combat(self.player, [monster]) # Create combat instance
        self.combat.start_combat()
        self.show_combat_screen()

    def show_combat_screen(self):
      app = App.get_running_app()
      if app and app.root:
        app.root.current = "combat"

    def show_game_screen(self):
      app = App.get_running_app()
      if app and app.root:
        app.root.current = "game"


    def load_game(self):
        pass  # TODO

    def save_game(self):
        pass  # TODO

    def quit_game(self):
        self.is_running = False

    def open_inventory(self):
      app = App.get_running_app()
      if app and app.root:
        app.root.current = "inventory"


    def open_character_screen(self):
      app = App.get_running_app()
      if app and app.root:
        app.root.current = "character"

    def load_item_data(self):
        self.items_data, self.msg = load_json_data("data/items.json")
        if self.items_data:
          self.items_data = self.items_data['items']
        else:
            print(self.msg) #handle however

    def load_quests(self):
        # Load quests from JSON and create Quest instances.
        self.quests = quests.load_quests("data/quests.json", self.items_data) # Pass item data.

    def add_quest(self, quest_id, quest):
        self.quests[quest_id] = quest

    def get_quest(self, quest_id):
        return self.quests.get(quest_id)

    def start_quest(self, quest_id):
      if quest_id in self.quests and not self.quests[quest_id].is_active:
        self.quests[quest_id].start_quest()

    def complete_quest(self, quest_id):
      if quest_id in self.quests and self.quests[quest_id].is_active:
        if self.quests[quest_id].check_completion():
          self.quests[quest_id].complete_quest(self) #pass in game
          #Handle Rewards
          rewards = self.quests[quest_id].rewards
          self.player.add_gold(rewards.get("gold", 0))
          self.player.experience += rewards.get("experience",0)
          for item_id, quantity in rewards.get("items", {}).items():
            item_data = self.items_data.get(item_id)
            if item_data:
                self.player.inventory.add_item(item_data.copy())

    def update_quests(self, dt):
        for quest_id, quest in self.quests.items():
            quest.update(self)

    def handle_dialogue_action(self, action_string):
      #Handle actions in dialogue
      if action_string is None:
        return

      actions = action_string.split(',')
      for action in actions:
        action_parts = action.split(':')
        action_type = action_parts[0]

        if action_type == "start_quest":
          quest_ids = action_parts[1:]
          for quest_id in quest_ids:
            self.start_quest(quest_id) # Start the quest
        elif action_type == "complete_quest":
          quest_ids = action_parts[1:]
          for quest_id in quest_ids:
            self.complete_quest(quest_id)
        #Handle other actions here.

    def get_kill_count(self, monster_id):
      return self.kill_counts.get(monster_id, 0)

    def increment_kill_count(self, monster_id):
      if monster_id not in self.kill_counts:
        self.kill_counts[monster_id] = 0
      self.kill_counts[monster_id] += 1