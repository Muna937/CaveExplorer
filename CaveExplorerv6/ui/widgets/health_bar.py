# ui/widgets/health_bar.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, AliasProperty

class HealthBar(Widget):
    max_health = NumericProperty(100)  # Maximum health value
    current_health = NumericProperty(100)  # Current health value

    def _get_health_ratio(self):
        if self.max_health == 0:  # Avoid division by zero
            return 0
        return self.current_health / float(self.max_health)

    health_ratio = AliasProperty(_get_health_ratio, bind=('current_health', 'max_health'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)  # Often needed for custom widgets
        self.size = (100, 20)  # Default size
        self.bind(health_ratio=self.update_bar)
        self.bind(pos=self.update_bar, size=self.update_bar)
        with self.canvas:
          #make background
          Color(0.8, 0.8, 0.8, 1)  # Light grey
          self.back_rect = Rectangle(pos=self.pos, size=self.size)

          #make bar
          Color(0, 1, 0, 1)  # Green
          self.health_rect = Rectangle(pos=self.pos, size=(self.width * self.health_ratio, self.height))

    def update_bar(self, *args):
        self.health_rect.pos = self.pos
        self.health_rect.size = (self.width * self.health_ratio, self.height)
        self.back_rect.pos = self.pos
        self.back_rect.size = self.size

# Example Usage (in another file, like game_screen.py):
# from ui.widgets.health_bar import HealthBar
#
# health_bar = HealthBar(max_health=100, current_health=75, size=(150, 30))
# self.add_widget(health_bar)  # Add it to your layout