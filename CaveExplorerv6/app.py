# app.py
# Goals:
#   - Kivy App Initialization: Define the main Kivy App class.
#   - Screen Management: Set up a ScreenManager to handle different screens.
#   - Game Instance Creation: Create a single instance of the Game class.
#   - Pass Game Instance: Pass the Game instance to relevant screens.

# Interactions:
#   - main.py: main.py imports and runs the App class defined here.
#   - ui/screens/ (all files): Imports screen classes (e.g., MainMenuScreen, GameScreen).
#   - game.py: Imports the Game class and creates an instance of it.
#   - Kivy Framework: Interacts with kivy.app.App and kivy.uix.screenmanager.ScreenManager.

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ui.screens.main_menu import MainMenuScreen
from ui.screens.game_screen import GameScreen
from game import Game

class GameApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.game_instance = Game()
        self.sm.add_widget(GameScreen(name='game', game=self.game_instance))
        return self.sm