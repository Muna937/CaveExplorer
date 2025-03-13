# ui/screens/game_screen.py

# Goals:
#   - Display the main game world (map, player, entities, items).
#   - Interact with the Game instance to update the game state and retrieve data.
#   - Provide a user interface for interacting with the game world (moving, opening menus).
#   - Render tiles using the Tile objects and their image_path attributes.
#   - Render NPCs, monsters, and items on top of the map.
#   - Use a RelativeLayout for correct Z-ordering and absolute positioning.
#   - Handle NO input, let the game class handle input.

# Interactions:
#   - app.py: Added to the ScreenManager by app.py. Receives the Game instance.
#   - game.py: Gets game state information (player position, map data, etc.).
#   - player.py:  (Indirectly) Controls the player's actions through game.py.
#   - world.py:  Gets map data (tiles, NPCs, monsters, items) for rendering.
#   - tile.py:  Uses Tile.image_path for rendering.
#   - npc.py:  Gets NPC data (including sprite paths) for rendering.
#   - monster.py: Gets Monster data (including sprite paths) for rendering.
#   - item.py: Gets item data (including icon paths) for rendering.
#   - ui/widgets/: May use custom widgets for UI elements (not used in this basic example).
#   - kivy.uix.relativelayout.RelativeLayout:  Uses RelativeLayout for absolute positioning.
#   - kivy.uix.image.Image: Uses Image widgets to display tiles, player, NPCs, etc.
#   - ui/screens/inventory_screen.py:  Can switch to the inventory screen.
#   - ui/screens/character_screen.py: Can switch to the character screen.

# ui/screens/game_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout  # Use RelativeLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App

class GameScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.tile_widgets = {}  # Store references to tile widgets.  Key: (col, row)

        # --- UI Setup ---
        self.layout = BoxLayout(orientation='vertical')

        # --- Map Display (RelativeLayout) ---
        self.map_view = RelativeLayout(size_hint=(None, None))  # Use RelativeLayout
        self.map_view.width = self.game.world.map_data['width'] * self.game.world.tile_size
        self.map_view.height = self.game.world.map_data['height'] * self.game.world.tile_size
        self.layout.add_widget(self.map_view)

        # --- Create Player Image HERE, in __init__ ---
        self.player_image = Image(source="assets/images/player.png",
                                  size=(self.game.world.tile_size, self.game.world.tile_size),
                                  size_hint=(None, None))
        self.map_view.add_widget(self.player_image)
        self.player_image.bind(texture=self.on_player_texture)  # Bind to texture.

        # --- UI Setup (Buttons for menus) ---
        self.ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.inventory_button = Button(text="Inventory")
        self.inventory_button.bind(on_press=self.go_to_inventory)
        self.character_button = Button(text="Character")
        self.character_button.bind(on_press=self.go_to_character)
        self.ui_layout.add_widget(self.inventory_button)
        self.ui_layout.add_widget(self.character_button)
        self.layout.add_widget(self.ui_layout)
        self.add_widget(self.layout)


        Clock.schedule_interval(self.update, 1.0 / 60.0)
        # --- Lists to hold entity images ---
        self.npc_images = []
        self.monster_images = []
        self.item_images = []

    def on_enter(self):
        self.render_map()  # Render tiles *first*
        self.render_entities() # Then render entities
        self.game.player.x = 5  # Example starting position
        self.game.player.y = 5


    def update(self, dt):
        self.game.update(dt)  # Update the game logic (player movement, NPC AI, etc.).
        #self.render_map()  # Re-render the map every frame. NO LONGER NEEDED
        self.render_entities() # Re-render entities every frame
        #self.label.text = f'Player X: {self.game.player.x}, Y: {self.game.player.y}' #Remove

    def go_to_inventory(self, instance):
        self.manager.current = "inventory" # Switch to Inventory Screen

    def go_to_character(self, instance):
        self.manager.current = "character"  # Switch to character screen

    def render_map(self):
        self.map_view.clear_widgets()
        self.tile_widgets.clear()

        for row_index, tile_row in enumerate(self.game.world.tiles):
            for col_index, tile in enumerate(tile_row):
                tile_widget = Image(
                    source=tile.image_path,
                    size=(self.game.world.tile_size, self.game.world.tile_size),
                    size_hint=(None, None),
                    pos=(col_index * self.game.world.tile_size, row_index * self.game.world.tile_size)  # Absolute positioning
                )
                self.map_view.add_widget(tile_widget)
                self.tile_widgets[(col_index, row_index)] = tile_widget


    def render_entities(self):

      # Render Player
      # Calculate player position on screen based on tile size.  NO LONGER conditional.
      self.update_player_position()


      # Render NPCs
      #Clear old images
      for image in self.npc_images:
        self.map_view.remove_widget(image)
      self.npc_images = []

      for npc_id, npc in self.game.world.npcs.items():
          npc_screen_x = npc.x * self.game.world.tile_size
          npc_screen_y = npc.y * self.game.world.tile_size
          npc_image = Image(source="assets/images/npcs/old_man.png",  # Replace with npc.sprite
                              size=(self.game.world.tile_size, self.game.world.tile_size),
                              size_hint=(None, None),
                              pos=(npc_screen_x, npc_screen_y))
          self.npc_images.append(npc_image) #add to list
          self.map_view.add_widget(npc_image)  # Add to map_view

        # Render Monsters (similar to NPCs)
      for image in self.monster_images:
        self.map_view.remove_widget(image)
      self.monster_images = []
      for monster in self.game.world.monsters:
          monster_screen_x = monster.x * self.game.world.tile_size
          monster_screen_y = monster.y * self.game.world.tile_size

          monster_image = Image(source=monster.sprite,
                                size=(self.game.world.tile_size, self.game.world.tile_size),
                                size_hint=(None, None),
                                pos=(monster_screen_x, monster_screen_y))
          self.monster_images.append(monster_image) #add to list
          self.map_view.add_widget(monster_image)

       #Render Items
      for image in self.item_images:
        self.map_view.remove_widget(image)
      self.item_images = []

      for item in self.game.world.items:
        item_screen_x = item.x * self.game.world.tile_size
        item_screen_y = item.y * self.game.world.tile_size

        item_image = Image(source = item.icon,
                           size = (self.game.world.tile_size, self.game.world.tile_size),
                           size_hint = (None, None),
                           pos = (item_screen_x, item_screen_y))
        self.item_images.append(item_image) #add to list
        self.map_view.add_widget(item_image)


    def on_player_texture(self, instance, value):
        # This method is called when the player image's texture is updated.
        if value:  # Make sure the texture is actually loaded
            self.update_player_position()

    def update_player_position(self):
        # This method now ONLY updates the position, and is called initially
        # and AFTER the texture is loaded.
        player_screen_x = self.game.player.x * self.game.world.tile_size
        player_screen_y = self.game.player.y * self.game.world.tile_size
        self.player_image.pos = (player_screen_x, player_screen_y)