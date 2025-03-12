# ui/widgets/label.py

from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty

class CustomLabel(Label):
    background_color = ListProperty([0.5, 0.5, 0.5, 0])  # Gray background, initially transparent
    text_color = ListProperty([1, 1, 1, 1])  # White text
    font_size = StringProperty('16sp') #font size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = self.text_color  # Set the Kivy 'color' property
        self.background_color = self.background_color
        self.font_size = self.font_size