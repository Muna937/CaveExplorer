# ui/screens/bestiary_screen.py

# Goals:
#   - Display information about monsters the player has encountered.
#   - Show monster stats, descriptions, images (sprites), and potentially drop information.
#   - Provide a way to browse and search the bestiary.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Gets information about discovered monsters.
#   - monsters.json:  Gets monster data (stats, descriptions, sprite paths).
#   - ui/widgets/: Might use custom widgets to display monster entries.
#   - kivy: Uses kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock  # Import Clock


class BestiaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Monster List (ScrollView) ---
        self.scrollview = ScrollView()
        self.monster_list = GridLayout(cols=1, size_hint_y=None)
        self.monster_list.bind(minimum_height=self.monster_list.setter('height'))
        self.scrollview.add_widget(self.monster_list)
        self.layout.add_widget(self.scrollview)

        # --- Monster Details ---
        self.details_layout = GridLayout(cols=2, size_hint_y=None, height=200)
        self.monster_image = Image(source="")  # Placeholder for image
        self.details_layout.add_widget(self.monster_image)

        self.stats_layout = GridLayout(cols=1)
        self.monster_name_label = Label(text="Monster Name", font_size=20)
        self.monster_description_label = Label(text="Monster Description", halign='left', valign='top')
        self.monster_hp_label = Label(text="HP: ")
        self.monster_attack_label = Label(text="Attack: ")
        self.monster_defense_label = Label(text="Defense: ")

        self.stats_layout.add_widget(self.monster_name_label)
        self.stats_layout.add_widget(self.monster_description_label)
        self.stats_layout.add_widget(self.monster_hp_label)
        self.stats_layout.add_widget(self.monster_attack_label)
        self.stats_layout.add_widget(self.monster_defense_label)
        self.details_layout.add_widget(self.stats_layout)
        self.layout.add_widget(self.details_layout)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0) # Add this line
        self.selected_monster = None
        self.monsters_data = {} # Initialize as an empty dictionary


    def on_enter(self):
        self.game = self.manager.parent.game_instance
        # Load monster data (you might want to do this only once, not every time)
        self.monsters_data, self.msg = load_json_data("data/monsters.json") #load monster data
        if self.monsters_data:
          self.monsters_data = self.monsters_data['monsters']
          self.refresh_bestiary()  # Populate the list when entering the screen.
        else:
          print(self.msg) # Handle the case where the load fails.


    def update(self, dt):
        pass


    def refresh_bestiary(self):
        self.monster_list.clear_widgets()
        self.selected_monster = None
        self.update_monster_details()

        # Example: Assuming you have a list of discovered monster IDs in game.player.discovered_monsters
        # You'd need to implement this tracking in your game logic.
        if self.monsters_data:
          for monster_id in self.monsters_data: #Iterate through them all for now, self.game.player.discovered_monsters:
              if monster_id in self.monsters_data:  # Check if the ID is valid
                monster_data = self.monsters_data[monster_id]
                monster_button = Button(text=monster_data["name"], size_hint_y=None, height=40)
                monster_button.bind(on_press=lambda instance, m=monster_id: self.select_monster(m))
                self.monster_list.add_widget(monster_button)

    def select_monster(self, monster_id):
        # Display details of the selected monster.
        if monster_id in self.monsters_data:
            self.selected_monster = monster_id
            self.update_monster_details()


    def update_monster_details(self):
        # Update labels and image with the selected monster's data
        if self.selected_monster and self.selected_monster in self.monsters_data:
            monster_data = self.monsters_data[self.selected_monster]
            self.monster_name_label.text = monster_data["name"]
            self.monster_description_label.text = monster_data["description"]
            self.monster_hp_label.text = f"HP: {monster_data['hp']}"
            self.monster_attack_label.text = f"Attack: {monster_data['attack']}"
            self.monster_defense_label.text = f"Defense: {monster_data['defense']}"
            self.monster_image.source = monster_data["sprite"]
        else:
          self.monster_name_label.text = "Monster Name"
          self.monster_description_label.text = "Monster Description"
          self.monster_hp_label.text = f"HP: "
          self.monster_attack_label.text = f"Attack: "
          self.monster_defense_label.text = f"Defense: "
          self.monster_image.source = ""

    def go_back(self, instance):
        self.manager.current = "game"