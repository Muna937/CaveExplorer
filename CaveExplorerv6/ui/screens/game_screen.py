# ui/screens/game_screen.py

# Goals:
#   - Display the main game world (map, player, entities, items).
#   - Interact with the Game instance to update the game state.
#   - Provide a user interface for interacting with the game world.
#   - Render tiles using the Tile objects and their image_path attributes.
#   - Render NPCs, monsters, and items.
#   - **No longer handles movement, now just calls game.update()**

# Interactions:
#   - app.py: Added to the ScreenManager by app.py. Receives the Game instance.
#   - game.py: Gets game state information (player position, map data, etc.).
#                 Sends player input to the game.
#   - player.py:  (Indirectly) Controls the player's actions through game.py.
#   - world.py:  Gets map data (tiles, NPCs, monsters, items) for rendering.
#   - tile.py:  Uses Tile.image_path for rendering.
#   - npc.py:  Gets NPC data for rendering.
#   - monster.py: Gets Monster data for rendering.
#   - item.py: Gets item data for rendering.
#   - ui/widgets/: May use custom widgets for UI elements (e.g., health bar).
#   - kivy.input:  Handles keyboard/mouse/touch input.
#   - ui/screens/inventory_screen.py (potentially):  Can switch to the inventory screen.
#   - ui/screens/character_screen.py (potentially): Can switch to the character screen.
#   - ui/screens/dialogue_screen.py: Transitions to dialogue when interacting with NPCs.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image #for tiles
from kivy.uix.gridlayout import GridLayout

class GameScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.tile_widgets = {}  # Store references to tile widgets

        # --- UI Setup ---
        self.layout = BoxLayout(orientation = 'vertical')

        # --- Map Display (GridLayout within a ScrollView) ---
        self.map_view = GridLayout(cols=self.game.world.map_data['width'],
                                   rows=self.game.world.map_data['height'],
                                   size_hint=(None, None))
        self.map_view.bind(minimum_width=self.map_view.setter('width'))
        self.map_view.bind(minimum_height=self.map_view.setter('height'))
        self.map_view.width = self.game.world.map_data['width'] * self.game.world.map_data['tile_size']
        self.map_view.height = self.game.world.map_data['height'] * self.game.world.map_data['tile_size']

        self.layout.add_widget(self.map_view)


        # --- UI Setup (Example: Buttons for menus) ---
        self.ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.inventory_button = Button(text="Inventory")
        self.inventory_button.bind(on_press=self.go_to_inventory)
        self.character_button = Button(text="Character")
        self.character_button.bind(on_press=self.go_to_character)
        self.ui_layout.add_widget(self.inventory_button)
        self.ui_layout.add_widget(self.character_button)
        self.layout.add_widget(self.ui_layout) #add to main screen
        self.add_widget(self.layout) #add layout


        # --- Input Handling --- REMOVED, now in game.py
        #self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        #self._keyboard.bind(on_key_down=self._on_keyboard_down)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_enter(self):
      self.render_map()
      self.game.player.x = 5 #temp
      self.game.player.y = 5

    def update(self, dt):
      self.game.update(dt)
      self.render_entities() #render enties, items and player
      #self.label.text = f'Player X: {self.game.player.x}, Y: {self.game.player.y}' #Remove

    def go_to_inventory(self, instance):
        self.manager.current = "inventory" # Switch to Inventory Screen

    def go_to_character(self, instance):
        self.manager.current = "character"  # Switch to character screen

    # --- Input Handling --- REMOVED, now in game.py
    # def _keyboard_closed(self):
    #     # Cleanup when the keyboard is closed.
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None

    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #   pass #removed

    # def check_move(self, dx, dy):
    #   pass #removed

    def render_map(self):
        self.map_view.clear_widgets()
        self.tile_widgets.clear()

        for row_index, tile_row in enumerate(self.game.world.tiles):
            for col_index, tile in enumerate(tile_row):
                tile_widget = Image(source=tile.image_path,
                                    size=(self.game.world.tile_size, self.game.world.tile_size),
                                    size_hint=(None,None))
                self.map_view.add_widget(tile_widget)
                # Store a reference to the widget for later updates (if needed)
                self.tile_widgets[(col_index, row_index)] = tile_widget

    def render_entities(self):
      # Clear existing entity representations (you might have separate widgets for these)
      #  This is a placeholder; you'll need a more efficient way to update only
      #  entities that have moved.
      for widget in self.map_view.children[:]: #copy of the list so we can remove
        if isinstance(widget, Image) and widget != self.player_image: # Check if its not a tile.
          self.map_view.remove_widget(widget)

      # Render Player
      # Create the player image if it doesn't exist
      if not hasattr(self, 'player_image'):
        self.player_image = Image(source="assets/images/player.png",
                                  size=(self.game.world.tile_size, self.game.world.tile_size),
                                  size_hint=(None, None))
        self.map_view.add_widget(self.player_image)
      # Calculate player position on screen based on tile size
      player_screen_x = self.game.player.x * self.game.world.tile_size
      player_screen_y = self.game.player.y * self.game.world.tile_size
      # Adjust for grid layout positioning (top-to-bottom rendering)
      grid_y = (self.game.world.map_data['height'] - 1 - self.game.player.y) * self.game.world.tile_size
      self.player_image.pos = (player_screen_x, grid_y)



      # Render NPCs
      for npc_id, npc in self.game.world.npcs.items():
          npc_screen_x = npc.x * self.game.world.tile_size
          npc_screen_y = npc.y * self.game.world.tile_size
          grid_y = (self.game.world.map_data['height'] - 1 - npc.y) * self.game.world.tile_size
          npc_image = Image(source="assets/images/npcs/old_man.png",  # Replace with npc.sprite
                              size=(self.game.world.tile_size, self.game.world.tile_size),
                              size_hint=(None, None),
                              pos=(npc_screen_x, grid_y))
          self.map_view.add_widget(npc_image)

      # Render Monsters (similar to NPCs)
      for monster in self.game.world.monsters:
          monster_screen_x = monster.x * self.game.world.tile_size
          monster_screen_y = monster.y * self.game.world.tile_size
          grid_y = (self.game.world.map_data['height'] - 1 - monster.y) * self.game.world.tile_size

          monster_image = Image(source=monster.sprite,
                                size=(self.game.world.tile_size, self.game.world.tile_size),
                                size_hint=(None, None),
                                pos=(monster_screen_x, grid_y))
          self.map_view.add_widget(monster_image)

       #Render Items
      for item in self.game.world.items:
        item_screen_x = item.x * self.game.world.tile_size
        item_screen_y = item.y * self.game.world.tile_size
        grid_y = (self.game.world.map_data['height'] -1 - item.y) * self.game.world.tile_size

        item_image = Image(source = item.icon,
                           size = (self.game.world.tile_size, self.game.world.tile_size),
                           size_hint = (None, None),
                           pos = (item_screen_x, grid_y))
        self.map_view.add_widget(item_image)