# game.py

# Goals:
#   - Initialize and manage the overall game state.
#   - Create and manage the player object.
#   - Load and manage the current game map.
#   - Handle the main game loop (updating game logic, handling input).
#   - Manage game time (if applicable).
#   - Interact with other game systems (combat, inventory, quests, etc.).
#   - Coordinate saving and loading of the game.
#   - **Centralize input handling.**
#   - **Manage player interactions with NPCs, monsters and items**

# Interactions:
#   - app.py: The App class creates the Game instance.
#   - player.py: Creates and manages the Player object.
#   - world.py: Loads and updates the game world (map).
#   - combat.py: Initiates and manages combat encounters.
#   - inventory.py: Accesses and modifies the player's inventory.
#   - quests.py: Updates quest progress.
#   - ui/screens/game_screen.py: Provides input to the game and receives data to display.
#   - ui/screens/dialogue_screen.py: Starts dialogue with NPCs.
#   - save_load.py: Saves and loads the game state.
#   - entity.py (potentially): If you have other entities besides the player, Game manages them.
#   - utils.py: May use utility functions (e.g., for loading data, pathfinding).
#   - npc.py: Interacts with NPCs.
#   - monster.py: Interacts with monsters.
#   - item.py: Handles item interactions (pickup).
#   - kivy.core.window:  Gets keyboard input.


from player import Player
from world import World
from kivy.core.window import Window

class Game:
    def __init__(self):
        self.player = Player(name="Hero", x=5, y=5, character_class="warrior")  # Initial position
        self.world = World()
        self.is_running = True
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.current_npc = None # Track the NPC we are interacting with.

    def update(self, dt):
        if not self.is_running:
            return

        # Input is handled separately now.
        self.player.update(dt)  # Update player (for things like animation)
        self.world.update(dt)   # Update world (NPCs, monsters)

        # --- NPC Interaction (Example) ---
        for npc_id, npc in self.world.npcs.items():
            if self.player.x == npc.x and self.player.y == npc.y:
                # Trigger interaction (e.g., start dialogue)
                self.current_npc = npc
                break  # Stop checking after the first interaction
            else:
                self.current_npc = None


        #--- Monster interaction (Example) ---
        for monster in self.world.monsters:
          if self.player.x == monster.x and self.player.y == monster.y:
            #Start Combat
            pass
        # --- Item Interaction (Example) ---
        items_to_remove = []
        for item in self.world.items:
          if self.player.x == item.x and self.player.y == item.y:
            #add to inventory
            if self.player.add_to_inventory(item):
              items_to_remove.append(item) #remove after loop
        for item in items_to_remove:
          self.world.items.remove(item)
    def _keyboard_closed(self):
        # Cleanup when the keyboard is closed.
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Handle keyboard input.  keycode is a tuple: (key_code, key_name)
        dx = 0
        dy = 0
        if keycode[1] == 'w':
            dy = -1
        elif keycode[1] == 's':
            dy = 1
        elif keycode[1] == 'a':
            dx = -1
        elif keycode[1] == 'd':
            dx = 1
        elif keycode[1] == 'q': #Quit
            self.quit_game()
        #Added e for interaction
        elif keycode[1] == 'e':
            self.handle_interaction()  # Check for interaction

        self.check_move(dx, dy) # Moved to game.py
        return True # Suppress other

    def handle_interaction(self):
      if self.current_npc:
        self.current_npc.interact(self.player, self) #call npc interact

    def check_move(self, dx, dy):
        if self.player:
            new_x = self.player.x + dx
            new_y = self.player.y + dy
            # The map size check is now within is_tile_walkable().
            if self.world.is_tile_walkable(new_x * self.world.tile_size, new_y * self.world.tile_size):
                self.player.move(dx, dy)


    def start_dialogue(self, npc_id):
        # Start dialogue with the specified NPC.
        # IMPORTANT:  Get the *current* ScreenManager from the running App.
        app = App.get_running_app()
        if app and app.root:  # Check that the app and root are available
            app.root.get_screen('dialogue').start_dialogue(npc_id)

    def start_combat(self):
        # combat_instance = Combat([self.player] + enemies_nearby)
        # combat_instance.start_combat()
        # while not combat_instance.is_combat_over():
        #   combat_instance.update(dt) # You might need a separate dt
        # results = combat_instance.get_results()
        # ... handle combat results ...
        pass

    def load_game(self):
        pass

    def save_game(self):
        pass

    def quit_game(self):
        self.is_running = False