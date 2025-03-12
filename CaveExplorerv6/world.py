# world.py

# Goals:
#   - Load and manage the game world (map data).
#   - Render the map (tiles, objects, etc.).
#   - Handle collision detection (if applicable).
#   - Manage map transitions (loading different maps).
#   - (Optionally) Manage dynamic map elements (e.g., moving platforms, opening doors).

# Interactions:
#   - game.py:
#       - Game.update() calls World.update().
#       - Game gets information about the map (e.g., tile data) from World.
#   - data/maps/: Loads map data from JSON files.
#   - entity.py (potentially): For collision detection with entities.
#   - player.py (potentially): For collision detection with the player.
#   - ui/screens/game_screen.py: Renders the map to the screen (likely using data provided by World).
#   - utils.py: May use utility functions (e.g., for loading JSON data).

# Example Structure (using a simple tile-based map):

class World:
    def __init__(self):
        self.map_data = None  # Store the current map data.
        self.current_map_name = "town"  # Example: Start in the "town" map.
        self.tile_size = 32 #Example
        self.load_map(self.current_map_name)

    def load_map(self, map_name):
        # Load map data from a JSON file (using a helper function, e.g., from utils.py).
        map_filepath = f"data/maps/{map_name}.json"
        self.map_data, error_message = load_json_data(map_filepath) # Assuming load_json_data is in utils.py
        if error_message:
          print(error_message) #Or handle however is appropriate
          return False, error_message

        #  process the map data (e.g., create Tile objects).
        #  This is a placeholder; you'll need to adapt it to your map data format.
        # self.tiles = []
        # for row in self.map_data["tiles"]:
        #     tile_row = []
        #     for tile_id in row:
        #         tile = Tile(tile_id)  # Create a Tile object (you'd define a Tile class).
        #         tile_row.append(tile)
        #     self.tiles.append(tile_row)
        return True, ""


    def update(self, dt):
        # Update the world state (e.g., animations, moving objects).
        pass

    def is_tile_walkable(self, x, y):
        # Check if a tile at the given coordinates is walkable (for collision detection).
        #  This is a placeholder; you'll need to implement your collision logic.
        if not self.map_data: # Map hasn't loaded
          return False
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        #check the bounds
        if 0 <= tile_y < len(self.map_data["tiles"]) and 0 <= tile_x < len(self.map_data["tiles"][0]):
            return self.map_data["tiles"][tile_y][tile_x] != 0  # Example: 0 represents a non-walkable tile.
        else:
          return False # Out of bounds is not walkable

    def render(self, screen): #You would likely use a surface or the screen.
        # Render the map to the screen.
        # This is a placeholder; you'll need to implement your rendering logic using Kivy.

        # Example (very basic):
        # for row_index, row in enumerate(self.tiles):
        #     for col_index, tile in enumerate(row):
        #         # Draw the tile at (col_index * tile_size, row_index * tile_size)
        #         # You'd use Kivy's Canvas instructions here.
        #          pass
        pass

    def change_map(self, map_name):
      success, message = self.load_map(map_name)
      if success:
        self.current_map_name = map_name
      return success, message

# Example Usage (in game.py):
# world = World()
# world.load_map("town")
#
# # ... later, in the game loop ...
# world.update(dt)
#
# # ... for collision detection ...
# if world.is_tile_walkable(player.x + dx, player.y + dy):
#     player.move(dx, dy)
#
# # ... for rendering ...
# world.render(screen)  # You'd pass in the Kivy Canvas or a relevant drawing surface.