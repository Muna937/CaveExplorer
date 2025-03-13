# app.py

# Goals:
#   - Kivy App Initialization: Define the main Kivy App class.
#   - Screen Management: Set up a ScreenManager to handle different screens.
#   - Game Instance Creation: Create a single instance of the Game class.
#   - Input Handler Initialization: Create an instance of InputHandler and pass in the game instance.
#   - Initial Map Load: Ensure the initial map is loaded *before* creating the GameScreen.
#   - Import and add all screens.

# Interactions:
#   - main.py: main.py imports and runs the App class defined here.
#   - ui/screens/ (all files): Imports screen classes (e.g., MainMenuScreen, GameScreen).
#   - game.py: Imports the Game class and creates an instance of it.
#   - input_handler.py:  Imports and creates an instance of InputHandler.
#   - Kivy Framework: Interacts with kivy.app.App and kivy.uix.screenmanager.ScreenManager.

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ui.screens.main_menu import MainMenuScreen
from ui.screens.game_screen import GameScreen
from ui.screens.inventory_screen import InventoryScreen
from ui.screens.character_screen import CharacterScreen
from ui.screens.quest_log_screen import QuestLogScreen
from ui.screens.options_screen import OptionsScreen
from ui.screens.save_load_screen import SaveLoadScreen
from ui.screens.beastiary_screen import BestiaryScreen
from ui.screens.combat_screen import CombatScreen
from ui.screens.crafting_screen import CraftingScreen
from ui.screens.dialogue_screen import DialogueScreen
from ui.screens.help_screen import HelpScreen
from ui.screens.map_screen import MapScreen
from ui.screens.skill_tree_screen import SkillTreeScreen
from ui.screens.stats_screen import StatsScreen
from ui.screens.shop_screen import ShopScreen
from ui.screens.game_over_screen import GameOverScreen
from game import Game
from input_handler import InputHandler  # Import InputHandler
import kivy


class GameApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.game_instance = Game()  # Create the Game instance *first*
        self.game_instance.load_initial_map()  # Load initial map *before* screens
        self.input_handler = InputHandler(self.game_instance)  # Create InputHandler, pass Game
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(GameScreen(name='game', game=self.game_instance))  # Pass game
        self.sm.add_widget(InventoryScreen(name='inventory'))
        self.sm.add_widget(CharacterScreen(name='character'))
        self.sm.add_widget(QuestLogScreen(name='quest_log'))
        self.sm.add_widget(OptionsScreen(name='options'))
        self.sm.add_widget(SaveLoadScreen(name='save', is_save_screen=True))
        self.sm.add_widget(SaveLoadScreen(name='load', is_save_screen=False))
        self.sm.add_widget(BestiaryScreen(name='bestiary'))
        self.sm.add_widget(CombatScreen(name='combat'))
        self.sm.add_widget(CraftingScreen(name='crafting'))
        self.sm.add_widget(DialogueScreen(name='dialogue'))
        self.sm.add_widget(HelpScreen(name='help'))
        self.sm.add_widget(MapScreen(name='map'))
        self.sm.add_widget(SkillTreeScreen(name='skill_tree'))
        self.sm.add_widget(StatsScreen(name='stats'))
        self.sm.add_widget(ShopScreen(name='shop'))
        self.sm.add_widget(GameOverScreen(name='game_over'))
        print(f"Kivy Version: {kivy.__version__}")  # Add this line

        return self.sm