# ui/screens/dialogue_screen.py

# Goals:
#   - Display dialogue text from NPCs.
#   - Handle branching dialogue (player choices).
#   - Show NPC and player portraits (optional).
#   - Provide a clear and easy-to-read interface.
#   - Use the custom DialogueBox widget.
#   - Load dialogue data dynamically from JSON files.
#   - Get the Game instance using App.get_running_app().

# Interactions:
#   - app.py: Added to ScreenManager.
#   - game.py:  Triggered when the player interacts with an NPC (game.start_dialogue).
#                Gets access to the Game instance via App.get_running_app().
#   - npcs.json: Gets the NPC's dialogue ID (indirectly, via game.py and world.py).
#   - data/dialogue/: Loads dialogue data from JSON files.
#   - ui/widgets/dialogue_box.py: Uses the DialogueBox widget to display the UI.
#   - kivy: Uses kivy for UI
#   - utils.py:  Uses load_json_data to load dialogue files.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from utils import load_json_data
from kivy.app import App
import os

class DialogueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Dialogue Text Label ---
        self.dialogue_label = Label(text="", text_size=(600, None), halign='left', valign='top', size_hint_y=0.7, color=(1,0,0,1), font_size= "24sp")
        self.layout.add_widget(self.dialogue_label)
        print(f"Dialogue label added to layout: {self.dialogue_label in self.layout.children}")

        # --- Choices Layout (GridLayout) ---
        self.choices_layout = GridLayout(cols=1, size_hint_y=None)
        self.choices_layout.bind(minimum_height=self.choices_layout.setter('height'))
        self.layout.add_widget(self.choices_layout)
        print(f"Choices layout added to layout: {self.choices_layout in self.layout.children}")

        # --- Add the main layout to the Screen! ---
        self.add_widget(self.layout)
        print(f"Main layout added to screen: {self.layout in self.children}")

        Clock.schedule_interval(self.update, 1/60.0)

        self.current_dialogue = None
        self.current_node = None
        self.npc_id = None
        self.game = None


    def on_enter(self):
        pass  # Game instance is now obtained in start_dialogue

    def update(self, dt):
      pass

    def start_dialogue(self, npc_id):
        print(f"DialogueScreen.start_dialogue called with npc_id: {npc_id}")
        self.npc_id = npc_id

        app = App.get_running_app()
        if app:
            self.game = app.game_instance
        else:
            print("Error: App instance not found.")
            self.end_dialogue()
            return

        if not self.game:
            print("Error: Game instance not set in DialogueScreen.")
            self.end_dialogue()
            return

        npc = self.game.world.npcs.get(npc_id)
        if not npc:
            print(f"Error: NPC with id '{npc_id}' not found in the world.")
            self.end_dialogue()
            return

        dialogue_id = npc.dialogue_id
        dialogue_filepath = os.path.join("data", "dialogue", f"{dialogue_id}.json")
        self.current_dialogue, self.msg = load_json_data(dialogue_filepath)
        if not self.current_dialogue:
            print(self.msg)
            self.end_dialogue()
            return

        self.current_node = self.current_dialogue.get("start")
        if not self.current_node:
            print("Error: No 'start' node found in dialogue.")
            self.end_dialogue()
            return
        self.show_node()

    def show_node(self):
        print("show_node called")
        if not self.current_node or not self.current_dialogue:
            print("Error: No current node or dialogue.")
            self.end_dialogue()
            return

        node_data = self.current_dialogue.get(self.current_node)
        if not node_data:
            print(f"Error: Node data not found for node '{self.current_node}'.")
            self.end_dialogue()
            return

        if self.npc_id not in self.game.world.npcs:
            print(f"Error: NPC ID '{self.npc_id}' not found in game world.")
            self.end_dialogue()
            return

        npc = self.game.world.npcs.get(self.npc_id)
        if not npc:
            print(f"Error: NPC object not found for ID '{self.npc_id}'.")
            self.end_dialogue()
            return

        print(f"Current node data: {node_data}")

        # --- FORCE VISIBILITY AND POSITION ---
        self.dialogue_label.text = f"{npc.name}: {node_data['text']}"
        self.dialogue_label.opacity = 1  # Ensure it's fully opaque
        print(f"Dialogue label text set to: {self.dialogue_label.text}")


        self.choices_layout.clear_widgets()  # Clear any previous buttons

        if "choices" in node_data:
            for choice in node_data["choices"]:
                button = Button(text=choice["text"], size_hint_y=None, height=40, background_color = (1,0,0,1), font_size = "20sp")
                button.bind(on_press=lambda instance, next_node=choice["next"]: self.handle_dialogue_choice(next_node))
                self.choices_layout.add_widget(button)
                print(f"Added choice button: {choice['text']}")
        else:
            print("No choices in this node")
            button = Button(text="End Dialogue", size_hint_y=None, height=40)
            button.bind(on_press=self.end_dialogue)
            self.choices_layout.add_widget(button)

    def handle_dialogue_choice(self, next_node):
        print(f"handle_dialogue_choice called with next_node: {next_node}")
        if next_node is None:
            self.end_dialogue()
            return

        node_data = self.current_dialogue.get(self.current_node)
        if node_data and "choices" in node_data:
            for choice in node_data["choices"]:
                if choice["next"] == next_node and "action" in choice:
                    self.game.handle_dialogue_action(choice["action"])

        self.current_node = next_node
        self.show_node()


    def end_dialogue(self, instance=None):
        print("end_dialogue called")
        self.manager.current = 'game'  # Switch back to the game screen
        self.current_dialogue = None
        self.current_node = None
        self.npc_id = None
