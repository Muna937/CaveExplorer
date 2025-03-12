# ui/screens/game_over_screen.py

# Goals:
#   - Display a "Game Over" message when the player dies.
#   - Offer options to the player (e.g., reload last save, restart from beginning).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Transitions to this screen when the player's health reaches 0.
#   - save_load.py (potentially):  Used to reload a saved game.
#   - kivy: Uses Kivy for UI.
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        game_over_label = Label(text="Game Over", font_size=48)
        self.layout.add_widget(game_over_label)

        # --- Buttons ---
        reload_button = Button(text="Reload Last Save")
        reload_button.bind(on_press=self.reload_game)
        self.layout.add_widget(reload_button)

        restart_button = Button(text="Restart from Beginning")
        restart_button.bind(on_press=self.restart_game)
        self.layout.add_widget(restart_button)

        main_menu_button = Button(text="Return to Main Menu")
        main_menu_button.bind(on_press=self.return_to_main_menu)
        self.layout.add_widget(main_menu_button)

        self.add_widget(self.layout)

    def reload_game(self, instance):
        # Reload the last saved game (you'd need to implement this using save_load.py).
        # Example (using save_load.py):
        success, message = load_game(self.manager.parent.game_instance) #load the game instance
        if success:
          self.manager.current = "game"
        else:
          #Display and error
          print(message)
          pass

        print("Reload Game (not fully implemented)")


    def restart_game(self, instance):
        # Start a completely new game.
        self.manager.parent.game_instance = Game() #create a new game instance
        self.manager.get_screen('game').game = self.manager.parent.game_instance #update the reference.
        self.manager.current = "game"
        print("Restart Game (not fully implemented)")


    def return_to_main_menu(self, instance):
        # Return to the main menu.

        self.manager.current = "main_menu"