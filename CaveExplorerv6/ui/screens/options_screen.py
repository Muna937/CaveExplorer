# ui/screens/options_screen.py

# Goals:
#   - Allow the player to adjust game settings (e.g., volume, resolution, difficulty).
#   - Provide a user-friendly interface for modifying settings.
#   - Save the changes to the configuration file (config.json).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - data/config.json: Reads and writes configuration settings.
#   - utils.py (likely): Uses a function from utils.py to load/save JSON data.
#   - ui/widgets/: Might use custom widgets (e.g., sliders, dropdowns).
#   - kivy: Uses kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window  # Import Window
from utils import load_json_data, save_json_data # Assuming you have save_json_data
import os

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=2)

        # --- Volume Control ---
        self.volume_label = Label(text="Volume:")
        self.volume_slider = Slider(min=0, max=1, value=0.5, step=0.05)
        self.volume_slider.bind(value=self.on_volume_change)
        self.layout.add_widget(self.volume_label)
        self.layout.add_widget(self.volume_slider)


        # --- Resolution Dropdown ---
        self.resolution_label = Label(text="Resolution:")
        self.resolution_dropdown = DropDown()
        # Example resolutions (add more as needed)
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        for res in resolutions:
            btn = Button(text=res, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.resolution_dropdown.select(btn.text))
            self.resolution_dropdown.add_widget(btn)
        self.resolution_button = Button(text="Select Resolution")
        self.resolution_button.bind(on_release=self.open_resolution_dropdown)

        self.layout.add_widget(self.resolution_label)
        self.layout.add_widget(self.resolution_button)

        # --- Back Button ---
        self.back_button = Button(text="Back to Main Menu")
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(Label(text="")) #spacer
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        self.config = {} # Initialize config

    def on_enter(self):
        # Load current settings when entering the screen.
        self.load_settings()

    def open_resolution_dropdown(self, instance):
      self.resolution_dropdown.open(instance)

    def load_settings(self):
        # Load settings from config.json.
        config_path = os.path.join("data", "config.json")
        self.config, self.message = load_json_data(config_path)
        if self.config:
            self.volume_slider.value = self.config.get("default_volume", 0.5)  # Provide a default value
            # Update selected resolution in dropdown
            resolution_str = f"{self.config.get('screen_width', 800)}x{self.config.get('screen_height', 600)}"
            self.resolution_button.text = resolution_str
            # Set initial window size
            Window.size = (self.config.get('screen_width', 800), self.config.get('screen_height', 600))
        else:
            print(f"Error loading config: {self.message}") # Or handle the error more gracefully

    def on_volume_change(self, instance, value):
        # Update the volume setting.
        self.config["default_volume"] = value
        # You might also want to update the actual game volume here (if applicable).

    def save_settings(self):
      # Save settings to config.json.
      # Split resolution string into width and height
      try:
        width, height = map(int, self.resolution_button.text.split("x"))
        self.config["screen_width"] = width
        self.config["screen_height"] = height
      except ValueError:
        print("Error saving resolution")
        # Handle case where resolution string is invalid
        pass
      config_path = os.path.join("data", "config.json")
      success, message = save_json_data(config_path, self.config)
      if not success:
          print(message) # Or handle the error more gracefully

      # Apply new window size after saving
      Window.size = (self.config["screen_width"], self.config["screen_height"])

    def go_back(self, instance):
        self.save_settings()
        self.manager.current = "main_menu"