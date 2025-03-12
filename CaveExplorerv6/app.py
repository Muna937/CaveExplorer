# app.py

# Goals:
#   - Kivy App Initialization: Define the main Kivy App class.
#   - Screen Management: Set up a ScreenManager to handle different screens.
#   - Game Instance Creation: Create a single instance of the Game class.
#   - Pass Game Instance: Pass the Game instance to relevant screens.
#  - Import and add all screens

# Interactions:
#   - main.py: main.py imports and runs the App class defined here.
#   - ui/screens/ (all files): Imports screen classes (e.g., MainMenuScreen, GameScreen).
#   - game.py: Imports the Game class and creates an instance of it.
#   - Kivy Framework: Interacts with kivy.app.App and kivy.uix.screenmanager.ScreenManager.

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from ui.screens.main_menu import MainMenuScreen
from ui.screens.game_screen import GameScreen
from ui.screens.inventory_screen import InventoryScreen # Import
from ui.screens.character_screen import CharacterScreen # Import
from ui.screens.quest_log_screen import QuestLogScreen # Import
from ui.screens.options_screen import OptionsScreen  # Import
from ui.screens.save_load_screen import SaveLoadScreen # Import
from ui.screens.bestiary_screen import BestiaryScreen # Import
from ui.screens.combat_screen import CombatScreen # Import
from ui.screens.crafting_screen import CraftingScreen # Import
from ui.screens.dialogue_screen import DialogueScreen # Import
from ui.screens.help_screen import HelpScreen # Import
from ui.screens.map_screen import MapScreen # Import
from ui.screens.skill_tree_screen import SkillTreeScreen # Import
from ui.screens.stats_screen import StatsScreen # Import
from ui.screens.shop_screen import ShopScreen #Import
from ui.screens.game_over_screen import GameOverScreen #Import
from game import Game

class GameApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.game_instance = Game()  # Create the Game instance here
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(GameScreen(name='game', game=self.game_instance)) # Pass game instance
        self.sm.add_widget(InventoryScreen(name='inventory')) # Add
        self.sm.add_widget(CharacterScreen(name='character')) # Add
        self.sm.add_widget(QuestLogScreen(name='quest_log'))  # Add
        self.sm.add_widget(OptionsScreen(name='options'))  # Add
        self.sm.add_widget(SaveLoadScreen(name='save', is_save_screen=True))  # Add
        self.sm.add_widget(SaveLoadScreen(name='load', is_save_screen=False))  # Add
        self.sm.add_widget(BestiaryScreen(name='bestiary'))  # Add
        self.sm.add_widget(CombatScreen(name='combat'))  # Add
        self.sm.add_widget(CraftingScreen(name='crafting'))  # Add
        self.sm.add_widget(DialogueScreen(name='dialogue'))  # Add
        self.sm.add_widget(HelpScreen(name='help'))  # Add
        self.sm.add_widget(MapScreen(name='map'))  # Add
        self.sm.add_widget(SkillTreeScreen(name='skill_tree'))  # Add
        self.sm.add_widget(StatsScreen(name='stats')) #Add
        self.sm.add_widget(ShopScreen(name='shop')) #Add
        self.sm.add_widget(GameOverScreen(name='game_over'))#Add
        return self.sm