# ui/screens/character_screen.py

# Goals:
#   - Display the player's character information (stats, attributes, skills, etc.).
#   - (Optionally) Allow the player to allocate attribute points or skill points.
#   - (Optionally) Allow the player to equip/unequip items (integrating with inventory_screen).
#   - Provide a visually appealing and informative layout.

# Interactions:
#   - app.py:  Added to the ScreenManager by app.py.
#   - game.py: Gets the player data (stats, skills, etc.) from the Game instance.
#   - player.py: Accesses player attributes directly (via the Game instance).
#   - skills.py (potentially): If allowing skill point allocation.
#   - ui/widgets/: Might use custom widgets (e.g., Label, Button) for layout.
#   - ui/screens/inventory_screen.py (potentially):  Could link to the inventory screen.
#  - kivy framework: Uses kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock  # Import Clock


class CharacterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=2)  # Simple two-column layout

        # --- Left Column: Labels for stat names ---
        self.stat_names_layout = GridLayout(cols=1, size_hint_x = 0.5)
        self.stat_names_layout.add_widget(Label(text="Strength:"))
        self.stat_names_layout.add_widget(Label(text="Dexterity:"))
        self.stat_names_layout.add_widget(Label(text="Constitution:"))
        self.stat_names_layout.add_widget(Label(text="Intelligence:"))
        self.stat_names_layout.add_widget(Label(text="Wisdom:"))
        self.stat_names_layout.add_widget(Label(text="Charisma:"))
        self.stat_names_layout.add_widget(Label(text="Level:"))
        self.stat_names_layout.add_widget(Label(text="Experience:"))
        self.layout.add_widget(self.stat_names_layout)

        # --- Right Column: Labels for stat values ---
        self.stat_values_layout = GridLayout(cols=1, size_hint_x = 0.5)
        self.strength_label = Label(text="")
        self.dexterity_label = Label(text="")
        self.constitution_label = Label(text="")
        self.intelligence_label = Label(text="")
        self.wisdom_label = Label(text="")
        self.charisma_label = Label(text="")
        self.level_label = Label(text="")
        self.experience_label = Label(text="")

        self.stat_values_layout.add_widget(self.strength_label)
        self.stat_values_layout.add_widget(self.dexterity_label)
        self.stat_values_layout.add_widget(self.constitution_label)
        self.stat_values_layout.add_widget(self.intelligence_label)
        self.stat_values_layout.add_widget(self.wisdom_label)
        self.stat_values_layout.add_widget(self.charisma_label)
        self.stat_values_layout.add_widget(self.level_label)
        self.stat_values_layout.add_widget(self.experience_label)
        self.layout.add_widget(self.stat_values_layout)


        # --- Bottom Section: Back Button ---
        self.back_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.back_button = Button(text="Back to Game")
        self.back_button.bind(on_press=self.go_back)
        self.back_button_layout.add_widget(self.back_button)
        self.layout.add_widget(self.back_button_layout)


        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0) # Add this line


    def on_enter(self):
        # This method is called when the screen is displayed.
        self.game = self.manager.parent.game_instance  # Access the Game instance
        self.update_stats()

    def update_stats(self):
        # Update the labels with the current player stats.
      if self.game and self.game.player:
        self.strength_label.text = str(self.game.player.strength) #you would need to define these stats in the player class
        self.dexterity_label.text = str(self.game.player.dexterity)
        self.constitution_label.text = str(self.game.player.constitution)
        self.intelligence_label.text = str(self.game.player.intelligence)
        self.wisdom_label.text = str(self.game.player.wisdom)
        self.charisma_label.text = str(self.game.player.charisma)
        self.level_label.text = str(self.game.player.level)  # Assuming you have a level attribute
        self.experience_label.text = str(self.game.player.experience) # And an experience attribute
      else:
        # Handle case when game or player is not yet initialized
        self.strength_label.text = ""
        self.dexterity_label.text = ""
        self.constitution_label.text = ""
        self.intelligence_label.text = ""
        self.wisdom_label.text = ""
        self.charisma_label.text = ""
        self.level_label.text = ""
        self.experience_label.text =""
    def update(self, dt):
        self.update_stats()

    def go_back(self, instance):
        self.manager.current = "game"  # Go back to the game screen.