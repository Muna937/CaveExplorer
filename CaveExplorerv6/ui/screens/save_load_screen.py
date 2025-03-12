# ui/screens/save_load_screen.py

# Goals:
#   - Allow the player to save the game to different save slots.
#   - Allow the player to load the game from a selected save slot.
#   - Handle cases where save slots are empty or occupied.
#   - (Optionally) Show save slot information (date/time, player name, level).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Gets the Game instance for saving/loading.
#   - save_load.py:  Calls the save_game() and load_game() functions.
#   - data/:  Saves and loads game data files (typically in a dedicated "saves" folder).
#   - kivy: Uses Kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os
from save_load import save_game, load_game # Import from your save_load module

class SaveLoadScreen(Screen):
    def __init__(self, is_save_screen=True, **kwargs):
        super().__init__(**kwargs)
        self.is_save_screen = is_save_screen  # Flag: True for save, False for load
        self.num_slots = 5  # Number of save slots

        self.layout = BoxLayout(orientation='vertical')

        # --- Title Label ---
        title_text = "Save Game" if self.is_save_screen else "Load Game"
        self.title_label = Label(text=title_text, font_size=24, size_hint_y=None, height=40)
        self.layout.add_widget(self.title_label)

        # --- Save/Load Slots (GridLayout) ---
        self.slots_layout = GridLayout(cols=3, size_hint_y=None)
        self.slots_layout.bind(minimum_height=self.slots_layout.setter('height'))

        self.slot_buttons = []
        for i in range(1, self.num_slots + 1):
            button_text = f"Slot {i}: Empty"
            slot_button = Button(text=button_text, size_hint_y=None, height=40)
            slot_button.bind(on_press=lambda instance, slot=i: self.slot_selected(slot))
            self.slot_buttons.append(slot_button)
            self.slots_layout.add_widget(slot_button) #add button
            self.slots_layout.add_widget(Label(text="", size_hint_x = None, width=100)) #add time stamp
            delete_button = Button(text="Delete", size_hint_x = None, width = 100)
            delete_button.bind(on_press=lambda instance, slot=i: self.delete_slot(slot))
            self.slots_layout.add_widget(delete_button)

        self.layout.add_widget(self.slots_layout)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def on_enter(self):
        self.game = self.manager.parent.game_instance
        self.refresh_slots()

    def update(self, dt):
        pass

    def refresh_slots(self):
        # Update the text of the save/load slot buttons.
        save_dir = "data/saves"  # Use a dedicated "saves" directory
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for i in range(self.num_slots):
            filepath = os.path.join(save_dir, f"save_{i + 1}.json")
            if os.path.exists(filepath):
                # Load a small amount of data for display (e.g., player name, level)
                # without loading the entire game state.
                try:
                    with open(filepath, "r") as f:
                        save_data = json.load(f)
                        # Get save time
                        timestamp = os.path.getmtime(filepath)
                        datetime_obj = datetime.fromtimestamp(timestamp)
                        formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                        player_name = save_data["player"]["name"] #adjust to file structure
                        #player_level = save_data["player"]["level"]
                        self.slot_buttons[i].text = f"Slot {i + 1}: {player_name}" # Level: {player_level}"
                        self.slots_layout.children[len(self.slots_layout.children)- 2 - (3 * i)].text = formatted_time #get time label, reverse order
                except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
                    self.slot_buttons[i].text = f"Slot {i + 1}: Corrupted"
                    print(f"Error loading save slot {i + 1}: {e}")
            else:
                self.slot_buttons[i].text = f"Slot {i + 1}: Empty"
                self.slots_layout.children[len(self.slots_layout.children)- 2 - (3 * i)].text = "" #get time label


    def slot_selected(self, slot_num):
        # Handle a save/load slot button press.
        filepath = os.path.join("data", "saves", f"save_{slot_num}.json")

        if self.is_save_screen:
            # Save Game
            success, message = save_game(self.game, filepath)
            if success:
              self.show_popup("Save Successful", "Game saved successfully!")
            else:
               self.show_popup("Save Failed", message)
            self.refresh_slots()  # Update button text

        else:
            # Load Game
            success, message = load_game(self.game, filepath)
            if success:
                self.manager.current = "game"  # Switch to the game screen
            else:
                self.show_popup("Load Failed", message)

    def delete_slot(self, slot_num):
      filepath = os.path.join("data", "saves", f"save_{slot_num}.json")
      try:
        os.remove(filepath)
        self.refresh_slots()
        self.show_popup("Delete Successful", f'Deleted Save Slot {slot_num}')
      except FileNotFoundError:
        self.show_popup("Delete Failed", f'Save Slot {slot_num} was not found')
      except Exception as e:
        self.show_popup("Delete Failed", str(e))

    def show_popup(self, title, text):
      popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 200))
      popup.open()

    def go_back(self, instance):
        self.manager.current = "game"