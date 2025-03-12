# tile.py

# Goals:
#   - Represent a single tile on the map.
#   - Store tile properties (ID, walkability, image path, etc.).
#   - (Optionally) Handle tile-specific logic (e.g., special effects when stepped on).

# Interactions:
#   - world.py:  World.load_map() creates Tile instances based on map data.
#   - ui/screens/game_screen.py:  Uses tile information for rendering.
#   - game.py (potentially): For tile-specific events or interactions.

class Tile:
    def __init__(self, tile_id, walkable=True, image_path=""): #Added default
        self.tile_id = tile_id
        self.walkable = walkable
        self.image_path = image_path  # Path to the tile's image
        # ... other tile properties (e.g., damage, special effects) ...

    # ... other methods (e.g., for drawing, handling interaction) ...
    # Example:  A method to handle a player stepping on the tile.
    # def on_step(self, player):
    #   if self.tile_id == "trap":
    #      player.take_damage(10)

# Example Usage (in world.py):
# tiles = []
# for row in map_data["tiles"]:
#   tile_row = []
#     for tile_id in row:
#       # Map tile IDs to properties (you'd likely have a dictionary or configuration for this).
#       if tile_id == 0:  # Example: 0 is a wall
#         tile = Tile(tile_id, walkable=False, image_path="assets/images/tiles/wall.png")
#       elif tile_id == 1:  # Example: 1 is floor
#         tile = Tile(tile_id, walkable=True, image_path="assets/images/tiles/floor.png")
#       # ... add more tile types ...
#       tile_row.append(tile)
#   tiles.append(tile_row)