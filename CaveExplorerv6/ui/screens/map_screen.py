# ui/screens/map_screen.py

# Goals:
#   - Display a world map (if your game has one).
#   - Show the player's current location on the map.
#   - Allow the player to view different areas of the map (scrolling/panning).
#   - Potentially show points of interest (towns, dungeons, etc.).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Gets the player's current location.
#   - data/maps/:  Loads the world map image or tile data.
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color  # Import Rectangle and Color


class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Map (Scatter for zoom/pan) ---
        self.scatter = Scatter(do_rotation=False, do_scale=True, do_translation=True)
        #You can either have one large image, or use the tile method
        #Large Image Method:
        self.map_image = Image(source="assets/images/world_map.png", allow_stretch=True, keep_ratio = False) # Replace with your map image
        self.scatter.add_widget(self.map_image)

        #Tile Method:
        # self.map_layout = GridLayout(cols=number_of_columns_in_world_map, size_hint=(None, None))
        # self.map_layout.bind(minimum_width=self.map_layout.setter('width'))
        # self.map_layout.bind(minimum_height=self.map_layout.setter('height'))
        # self.scatter.add_widget(self.map_layout)

        self.layout.add_widget(self.scatter)

        # Player Marker (added to Scatter, so it moves with the map)
        with self.scatter.canvas:
            Color(1, 0, 0, 1)  # Red color
            self.player_marker = Rectangle(pos=(0, 0), size=(10, 10))  # Adjust size as needed



        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0/60.0)


    def on_enter(self):
      self.game = self.manager.parent.game_instance
      #self.load_map() # If using tiled method
      self.update_player_marker()

    def update(self, dt):
      pass
    # def load_map(self): #If using tiled method
    #   #Load the map
    #   pass

    def update_player_marker(self):
        # Update the position of the player marker on the map.  This is just an example.
        # You'll need to map your game world coordinates to pixel coordinates on the map image.
        if self.game and self.game.player:
            # Example: Assuming your map image is 1000x1000 pixels and your game world is 100x100.
            map_width = self.map_image.texture_size[0] #get from image
            map_height = self.map_image.texture_size[1]

            #Simple conversion:
            marker_x = (self.game.player.x / 100) * map_width
            marker_y = (self.game.player.y / 100) * map_height

            # Center the marker
            self.player_marker.pos = (marker_x - self.player_marker.size[0] / 2 ,
                                       marker_y - self.player_marker.size[1] / 2)


    def go_back(self, instance):
        self.manager.current = "game"