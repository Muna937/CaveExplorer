# ui/widgets/button.py

from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty #for properties

class CustomButton(Button):
    bg_color = ListProperty([0.2, 0.6, 0.9, 1])  # Default background color (blue)
    text_color = ListProperty([1,1,1,1])
    font_size = StringProperty("14sp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''  # Remove default button image
        self.background_color = self.bg_color  # Use our custom color
        self.color = self.text_color
        self.font_size = self.font_size
# Example Usage (in another file):
# from ui.widgets.button import CustomButton
#
# button = CustomButton(text="My Button", bg_color=[1, 0, 0, 1])  # Red button
# self.add_widget(button)