# ui/widgets/stat_bar.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, AliasProperty, StringProperty, ListProperty

class StatBar(Widget):
    max_value = NumericProperty(100)  # Maximum value
    current_value = NumericProperty(100)  # Current value
    bar_color = ListProperty([0, 1, 0, 1])  # Green (default) - RGBA
    background_color = ListProperty([0.8, 0.8, 0.8, 1])  # Light grey - RGBA
    label_text = StringProperty("") # Text

    def _get_value_ratio(self):
        if self.max_value == 0:
            return 0
        return self.current_value / float(self.max_value)

    value_ratio = AliasProperty(_get_value_ratio, bind=('current_value', 'max_value'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 20)  # Default size
        self.label = Label(text=self.label_text, color = (0,0,0,1), size_hint=(None, None)) #black text
        self.add_widget(self.label) #add as a widget so it is rendered.

        with self.canvas:
            # Background rectangle
            Color(rgba=self.background_color)
            self.back_rect = Rectangle(pos=self.pos, size=self.size)

            # Value rectangle
            Color(rgba=self.bar_color)
            self.value_rect = Rectangle(pos=self.pos, size=(self.width * self.value_ratio, self.height))

        self.bind(value_ratio=self.update_bar, pos=self.update_bar, size=self.update_bar,
                  bar_color=self.update_color, background_color=self.update_background_color, label_text=self.update_text) #bind all properties

    def update_bar(self, *args):
        self.value_rect.pos = self.pos
        self.value_rect.size = (self.width * self.value_ratio, self.height)
        self.back_rect.pos = self.pos
        self.back_rect.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size

    def update_color(self, *args):
      #Update Colors
      self.canvas.children[1].rgba = self.bar_color #index is important.
      #self.canvas.ask_update() #May or may not need.

    def update_background_color(self, *args):
      self.canvas.children[3].rgba = self.background_color

    def update_text(self, *args):
      self.label.text = self.label_text

# Example Usage (in another file, like game_screen.py or combat_screen.py):
# from ui.widgets.stat_bar import StatBar
#
# hp_bar = StatBar(max_value=100, current_value=75, bar_color=[1, 0, 0, 1], label_text = "HP: 75/100")  # Red HP bar
# self.add_widget(hp_bar)
#
# mp_bar = StatBar(max_value=50, current_value=30, bar_color=[0, 0, 1, 1], size=(80, 15))  # Blue MP bar, different size
# self.add_widget(mp_bar)
#
# # Later, to update:
# hp_bar.current_value = 50
# hp_bar.label_text = f'HP: {hp_bar.current_value}/{hp_bar.max_value}'