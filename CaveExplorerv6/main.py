# main.py

# Goals:
#   - Serve as the entry point for the entire application.
#   - Import the necessary modules from the Kivy framework.
#   - Import the main App class (defined in app.py).
#   - Create an instance of the App class.
#   - Start the Kivy event loop by calling the run() method of the App instance.

# Interactions:
#   - app.py: Imports the main Kivy App class (e.g., GameApp) from app.py.
#   - Kivy Framework:  Relies on kivy.app.App for the basic application structure.

# Example Structure:
import sys
import os
# Get the absolute path of the current file (main.py)
current_file_path = os.path.abspath(__file__)
# Get the directory containing the current file (project root)
project_root = os.path.dirname(current_file_path)
# Add the project root to the Python path
sys.path.insert(0, project_root)
from kivy.app import App
from app import GameApp  # Import your main App class

if __name__ == '__main__':
    GameApp().run()