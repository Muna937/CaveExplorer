# ui/screens/character_screen.py

# Goals:
#   - Display the player's character information (stats, attributes, skills).
#   - Provide a read-only view of character data (no direct editing on this screen).
#   - Access the Game instance through the ScreenManager to get player data.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets player data (stats, skills, etc.) via App.game_instance.
#   - player.py: Accesses player attributes indirectly (through game.py).
#   - ui/widgets/:  Could use custom widgets (but this example uses standard Labels).
#   - kivy.app:  Uses App.get_running_app() to get the running App instance.
#   - kivy.uix.screenmanager: Uses Screen for the base class.
#   - kivy.uix.label: Uses Label for displaying text.
#   - kivy.uix.button: Uses Button for the "Back" button.
#   - kivy.uix.gridlayout: Uses GridLayout for layout
#  - kivy.clock: Uses Clock.schedule_once for delayed updates

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App  # Import App


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
        self.update_stats()

    def update_stats(self, dt=0):  # Add dt argument for Clock
          # Access the game instance through the ScreenManager's parent (the App)
        app = App.get_running_app()
        if app and app.game_instance and app.game_instance.player:
            player = app.game_instance.player
            self.strength_label.text = str(player.strength) #you would need to define these stats in the player class
            self.dexterity_label.text = str(player.dexterity)
            self.constitution_label.text = str(player.constitution)
            self.intelligence_label.text = str(player.intelligence)
            self.wisdom_label.text = str(player.wisdom)
            self.charisma_label.text = str(player.charisma)
            self.level_label.text = str(player.level)  # Assuming you have a level attribute
            self.experience_label.text = str(player.experience) # And an experience attribute
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