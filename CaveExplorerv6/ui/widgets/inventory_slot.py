# ui/widgets/inventory_slot.py

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty

class InventorySlot(Button):  # Inherit from Button for easy interaction
    item = ObjectProperty(None, allownone=True)  # The item in this slot (can be None)
    slot_index = NumericProperty(0) #added slot index
    on_slot_pressed = ObjectProperty(None)  # Callback for when the slot is pressed
    empty_text = StringProperty("Empty") # Text
    disabled = BooleanProperty(False) # Make sure it is not disabled

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.2, 0.2, 1)  # Dark grey background
        self.color = (1, 1, 1, 1) # White text color
        self.label = Label(text=self.empty_text, markup=True, color=(1,1,1,1)) #added markup
        self.add_widget(self.label)
        self.bind(on_press=self.trigger_slot_pressed)

    def update_slot(self, item=None):
        self.item = item
        if item:
            self.label.text = f"[b]{item.name}[/b]\nQty: {item.quantity}" #bold name
            # You might also display an item icon here (if you have icons)
            # self.icon.source = item.icon  # Example, if you add an Image widget
        else:
            self.label.text = self.empty_text
            #self.icon.source = ""

    def trigger_slot_pressed(self, instance):
      if self.on_slot_pressed and not self.disabled:
        self.on_slot_pressed(self.slot_index)

    def on_item(self, instance, value):
      self.update_slot(value)