# ui/screens/stats_screen.py

# Goals:
#   - Display detailed player statistics.
#   - Provide a clear and organized view of the player's attributes, resistances, etc.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Gets the player's stats.
#   - player.py: Accesses the Player object's attributes.
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock  # Import Clock

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Stats Display (GridLayout) ---
        self.stats_layout = GridLayout(cols=2, size_hint_y=None)
        self.stats_layout.bind(minimum_height=self.stats_layout.setter('height'))
        self.layout.add_widget(self.stats_layout)

        # --- Labels (will be updated dynamically) ---
        self.stat_labels = {}  # Dictionary to store stat labels

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0) # Add this line


    def on_enter(self):
        self.game = self.manager.parent.game_instance
        self.refresh_stats()

    def update(self, dt):
        pass

    def refresh_stats(self):
        # Clear existing stat labels
        self.stats_layout.clear_widgets()
        self.stat_labels.clear()

        if self.game and self.game.player:
            # Example stats (adapt to your actual stats):
            stats_to_display = {
                "Name": self.game.player.name,
                "Level": self.game.player.level,
                "Experience": self.game.player.experience,
                "HP": self.game.player.hp,
                "Max HP": self.game.player.max_hp,
                "Strength": self.game.player.strength,
                "Dexterity": self.game.player.dexterity,
                "Intelligence": self.game.player.intelligence,
                "Defense": self.game.player.defense,  # Example resistance
                # Add more stats as needed...
            }

            for stat_name, stat_value in stats_to_display.items():
                name_label = Label(text=f"{stat_name}:", size_hint_y=None, height=30)
                value_label = Label(text=str(stat_value), size_hint_y=None, height=30)
                self.stat_labels[stat_name] = value_label  # Store the value label
                self.stats_layout.add_widget(name_label)
                self.stats_layout.add_widget(value_label)

        else:  # Handle the case where game or player is not initialized
            self.stats_layout.add_widget(Label(text="No player data available."))

    def go_back(self, instance):
        self.manager.current = "game"