# ui/screens/main_menu.py

# Goals:
#   - Provide a starting point for the game.
#   - Offer options to the player (start new game, load game, options, exit).
#   - Display the game title and any other relevant information.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - ui/screens/game_screen.py: Transitions to the game screen when starting a new game.
#   - ui/screens/options_screen.py (potentially):  Transitions to the options screen.
#   - save_load.py (potentially):  Handles loading a saved game.
#   - kivy: Uses kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Title Label
        title_label = Label(text="My Awesome RPG", font_size=48)
        layout.add_widget(title_label)

        # --- Buttons ---
        new_game_button = Button(text="New Game")
        new_game_button.bind(on_press=self.start_new_game)
        layout.add_widget(new_game_button)

        load_game_button = Button(text="Load Game")
        load_game_button.bind(on_press=self.load_game)
        layout.add_widget(load_game_button)

        options_button = Button(text="Options")
        options_button.bind(on_press=self.go_to_options)
        layout.add_widget(options_button)

        exit_button = Button(text="Exit")
        exit_button.bind(on_press=self.exit_game)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def start_new_game(self, instance):
        # Start a new game (switch to the game screen).
        self.manager.current = "game"

    def load_game(self, instance):
        # Load a saved game (you'd need to implement the loading logic).
        # Example (using save_load.py):
        # success, message = load_game(self.manager.parent.game_instance)
        # if success:
        #     self.manager.current = "game"  # Go to the game screen
        # else:
            # Display an error message (e.g., using a Popup)
        #   pass

        #For now just go to game screen
        self.manager.current = "game"
        print("Load Game (not yet implemented)")


    def go_to_options(self, instance):
        # Switch to the options screen (you'd need to create an OptionsScreen).
        # self.manager.current = "options"
        print("Options (not yet implemented)") # Placeholder
        pass

    def exit_game(self, instance):
        # Exit the application.
        App.get_running_app().stop()