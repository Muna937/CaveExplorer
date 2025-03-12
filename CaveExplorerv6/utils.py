# utils.py

# Goals:
#   - Provide utility functions that are used by multiple parts of the game.
#   - Keep these functions separate from the main game logic to improve code organization.
#   - Avoid code duplication by centralizing common tasks.

# Interactions:
#   - Potentially any other file in the project.  Utility functions are designed to be
#     general-purpose and reusable.

import random
import json
import os

def load_json_data(filepath):
    """Loads JSON data from a file, handling potential errors."""
    try:
        # Ensure the filepath is relative to the project root or is absolute
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.path.dirname(__file__), "..", filepath)  # Go up one level to project root

        with open(filepath, 'r') as f:
            data = json.load(f)
        return data, "" #return data and a message
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None, f"File not found: {filepath}"
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {filepath}")
        return None, f"Invalid JSON in file: {filepath}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, str(e)

def roll_dice(num_dice, num_sides):
    """Simulates rolling dice (e.g., for damage rolls, skill checks)."""
    total = 0
    for _ in range(num_dice):
        total += random.randint(1, num_sides)
    return total

def calculate_distance(x1, y1, x2, y2):
    """Calculates the Euclidean distance between two points."""
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def clamp(value, min_value, max_value):
    """Clamps a value within a given range."""
    return max(min_value, min(value, max_value))

# Example Usage (you wouldn't actually run this here, but it shows how to use the functions):
# data, message = load_json_data("data/items.json")
# if data:
#     print("Loaded item data successfully.")
#
# distance = calculate_distance(1, 2, 4, 6)
# print(f"Distance: {distance}")
#
# clamped_value = clamp(15, 0, 10)
# print(f"Clamped value: {clamped_value}")

# --- Add more utility functions as needed ---