# ui/widgets/dialogue_box.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.graphics import Color, Rectangle

class DialogueBox(BoxLayout):
    npc_name = StringProperty("")  # Name of the NPC
    dialogue_text = StringProperty("")  # The dialogue text to display
    choices = ListProperty([])  # List of choice dictionaries: [{"text": "Choice 1", "next": "node2"}, ...]
    bg_color = ListProperty([0.2, 0.2, 0.2, 0.8])  # Semi-transparent dark grey
    text_color = ListProperty([1, 1, 1, 1]) #white
    button_color = ListProperty([0.4,0.4,0.4,1])
    on_choice_callback = ObjectProperty(None)  # Callback function for when a choice is made
    font_size = StringProperty('16sp')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, None)  # Don't take up the whole screen vertically
        self.height = 200  # Default height

        # --- Background (using canvas) ---
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect, bg_color=self.update_bg_color)

        # --- NPC Name Label ---
        self.name_label = Label(text=self.npc_name, size_hint_y=None, height=30, font_size=self.font_size, color=self.text_color)
        self.add_widget(self.name_label)

        # --- Dialogue Text Label ---
        self.text_label = Label(text=self.dialogue_text, size_hint_y=None, text_size=(self.width, None), halign='left', valign='top', color = self.text_color, font_size=self.font_size) # Added text color
        self.text_label.bind(texture_size=self.text_label.setter('size')) # Wrap and resize
        self.add_widget(self.text_label)

        # --- Choices Layout (GridLayout) ---
        self.choices_layout = GridLayout(cols=1, size_hint_y=None)
        self.choices_layout.bind(minimum_height=self.choices_layout.setter('height'))
        self.add_widget(self.choices_layout)


        # --- Bindings ---
        self.bind(npc_name=self.update_name_label, dialogue_text=self.update_text_label,
                  choices=self.update_choices)  # Bind properties to update methods
        self.bind(font_size=self.update_font_size) #Bind font size
        self.bind(text_color=self.update_text_color)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_bg_color(self, *args):
      self.canvas.before.clear()
      with self.canvas.before:
        Color(rgba=self.bg_color)
        self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_name_label(self, *args):
      self.name_label.text = self.npc_name
      self.name_label.color = self.text_color
      self.name_label.font_size = self.font_size

    def update_text_label(self, *args):
        self.text_label.text = self.dialogue_text
        self.text_label.color = self.text_color
        self.text_label.font_size = self.font_size

    def update_choices(self, *args):
        self.choices_layout.clear_widgets()
        for choice in self.choices:
            button = Button(text=choice["text"], size_hint_y=None, height=40, background_color = self.button_color)
            # Use a closure to capture the 'next_node' value correctly
            button.bind(on_press=lambda instance, next_node=choice["next"]: self.make_choice(next_node))
            self.choices_layout.add_widget(button)
        #If there are no choices, add a button to end
        if not self.choices:
          end_button = Button(text="End", size_hint_y=None, height=40, background_color = self.button_color)
          end_button.bind(on_press=self.end_dialogue)
          self.choices_layout.add_widget(end_button)


    def make_choice(self, next_node):
        if self.on_choice_callback:
            self.on_choice_callback(next_node)

    def end_dialogue(self, instance):
      if self.on_choice_callback:
        self.on_choice_callback(None)

    def update_font_size(self, *args):
      self.name_label.font_size = self.font_size
      self.text_label.font_size = self.font_size

    def update_text_color(self, *args):
      self.name_label.color = self.text_color
      self.text_label.color = self.text_color

# Example Usage (in dialogue_screen.py):
# from ui.widgets.dialogue_box import DialogueBox
#
# dialogue_box = DialogueBox(npc_name="Old Man", dialogue_text="Hello there!",
#                             choices=[{"text": "Hi!", "next": "node2"}, {"text": "Go away!", "next": "node3"}])
# self.add_widget(dialogue_box) #add to layout
#
# # Later, to update the dialogue:
# dialogue_box.dialogue_text = "New dialogue text."
# dialogue_box.choices = [{"text": "New Choice", "next": "node4"}]
# dialogue_box.on_choice_callback = self.handle_dialogue_choice  # Set the callback