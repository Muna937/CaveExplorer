# save_load.py

# Goals:
#   - Save the game state to a file.
#   - Load the game state from a file.
#   - Handle potential errors (e.g., file not found, corrupted data).
#   - Use a suitable data format for saving (JSON is recommended).

# Interactions:
#   - game.py: Called by Game.save_game() and Game.load_game().
#   - player.py: Saves and loads player data.
#   - world.py: Saves and loads world data (map state, NPC positions, etc.).
#   - inventory.py: Saves and loads the player's inventory.
#   - quests.py: Saves and loads quest progress.
#   - entity.py (potentially): Saves and loads data for other entities.
#   - data/ (indirectly): Defines the *structure* of the data being saved/loaded.
#   - (Optionally) A dedicated save/load UI screen.

import json
import os

def save_game(game, filename="savegame.json"):
    """Saves the game state to a JSON file."""
    try:
        data = {
            "player": {
                "name": game.player.name,
                "x": game.player.x,
                "y": game.player.y,
                "health": game.player.health,
                "max_health": game.player.max_health,
                "gold": game.player.gold,
                "inventory": game.player.inventory.items,  # Save inventory items
                # ... other player attributes ...
            },
            "world": {
                # ... save world state (current map, etc.) ...
                # "current_map": game.world.current_map_name,
                # "map_states": {}  # Example: Save changes to individual maps.
            },
            "quests": [
              #Example save quest data.
            ],
            # ... other game state data ...
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)  # Use indent for readability
        print(f"Game saved to {filename}")
        return True, "" #return success and a message

    except Exception as e:
        print(f"Error saving game: {e}")
        return False, str(e)



def load_game(game, filename="savegame.json"):
    """Loads the game state from a JSON file."""
    try:
        if not os.path.exists(filename):
          return False, "Save file not found."

        with open(filename, "r") as f:
            data = json.load(f)

        # Load player data
        player_data = data["player"]
        game.player.name = player_data["name"]
        game.player.x = player_data["x"]
        game.player.y = player_data["y"]
        game.player.health = player_data["health"]
        game.player.max_health = player_data["max_health"]
        game.player.gold = player_data["gold"]

        #Important: create the item objects from the saved data!
        game.player.inventory.clear_inventory() # Clear existing inventory
        for item_data in player_data["inventory"]:
            # Assuming a simple item structure for now.  In a real game,
            # you'd probably need to look up item definitions from items.json
            # based on an item ID or name.
            game.player.inventory.add_item(item_data)

        # Load world data
        # world_data = data["world"]
        # game.world.current_map_name = world_data["current_map"]
        # ... load other world data ...

        # Load quest data
        #for quest_data in data["quests"]:
          #Load Quests
        #  pass

        print(f"Game loaded from {filename}")
        return True, "" #return success and a message

    except FileNotFoundError:
        print(f"Error: Save file not found: {filename}")
        return False, "Save file not found"
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in save file: {filename}")
        return False, "Invalid save file format"
    except KeyError as e:
        print(f"Error: Missing data in save file: {e}")
        return False, f"Corrupted save file: missing key {e}"
    except Exception as e:
        print(f"Error loading game: {e}")
        return False, str(e)

#Example of how to use.
#save_game(game_instance) # In game.py
#load_game(game_instance)