# ui/widgets/skill_button.py

# Goals:
#   - Create a custom button widget for displaying and using player skills.
#   - Display skill information (name, potentially icon or description).
#   - Handle button presses to trigger skill use.
#   - Provide a callback mechanism to connect the button to the game logic.
#   - Disable button if cannot be used.

# Interactions:
#   - skills.py:  Gets skill data to display.
#   - combat_screen.py (or game_screen.py):
#       - Creates SkillButton instances and adds them to the UI.
#       - Sets the on_skill_use callback to handle skill activation.
#   - player.py (indirectly):  Used to check if a skill can be used.
#   - Kivy Framework: Inherits from kivy.uix.button.Button.

from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

class SkillButton(Button):
    skill_id = StringProperty(None)  # The ID of the skill this button represents
    skill_data = ObjectProperty(None)  # The skill data dictionary
    on_skill_use = ObjectProperty(None)  # Callback function
    disabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''  # Remove default button image
        self.background_color = (0.4, 0.4, 0.4, 1)  # Default background
        self.color = (1, 1, 1, 1) # White Text
        self.bind(on_press=self.trigger_skill_use)

    def set_skill_data(self, skill_id, skill_data, can_use):
      self.skill_id = skill_id
      self.skill_data = skill_data
      self.text = self.skill_data["name"]
      self.disabled = not can_use # Disable button if cant use skill

    def trigger_skill_use(self, instance):
        if self.skill_id and self.on_skill_use:
            self.on_skill_use(self.skill_id)