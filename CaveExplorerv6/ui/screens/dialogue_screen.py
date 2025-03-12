# ... (previous imports) ...
from ui.widgets.dialogue_box import DialogueBox # Import the custom widget

class DialogueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Dialogue Box (Use the custom widget) ---
        self.dialogue_box = DialogueBox()
        self.dialogue_box.on_choice_callback = self.handle_dialogue_choice  # Set the callback
        self.layout.add_widget(self.dialogue_box)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0/60.0)

        self.current_dialogue = None
        self.current_node = None
        self.npc_id = None

    def on_enter(self):
      self.game = self.manager.parent.game_instance

    def update(self, dt):
      pass

    def start_dialogue(self, npc_id):
        # Load dialogue data and start the conversation.
        self.npc_id = npc_id #store npc id
        npc_data = self.game.world.map_data['npcs'].get(npc_id) #get npc from world
        if not npc_data:
            print(f"Error: NPC data not found for {npc_id}")
            self.end_dialogue()  # Go back if NPC data is missing
            return

        dialogue_id = npc_data["dialogue"]
        dialogue_filepath = os.path.join("data", "dialogue", f"{dialogue_id}.json")
        self.current_dialogue, self.msg = load_json_data(dialogue_filepath)
        if not self.current_dialogue:
          print(self.msg) #handle error
          self.end_dialogue()
          return

        # Find the starting node (you might have a specific entry point).
        self.current_node = self.current_dialogue.get("start")
        if not self.current_node:
            print("Error: No 'start' node found in dialogue.")
            self.end_dialogue()  # Go back if no start node
            return
        self.show_node()

    def show_node(self):
      # Display the current dialogue node.
      if not self.current_node or not self.current_dialogue:
          self.end_dialogue()
          return

      node_data = self.current_dialogue.get(self.current_node)
      if not node_data:
        print("error node not found")
        self.end_dialogue()
        return

      self.dialogue_box.npc_name = self.game.world.npcs[self.npc_id].name  # Set NPC name
      self.dialogue_box.dialogue_text = node_data["text"]

      # Clear previous choices and add new ones
      if "choices" in node_data:
        self.dialogue_box.choices = node_data["choices"]
      else:
        self.dialogue_box.choices = []


    def handle_dialogue_choice(self, next_node):
      # Handle player choice (called by the DialogueBox).
      if next_node is None: #End
        self.end_dialogue()
        return
      self.current_node = next_node
      self.show_node()


    def end_dialogue(self):
      # End the conversation and go back to the game screen.
      self.manager.current = "game"
      self.current_dialogue = None
      self.current_node = None
      self.npc_id = None #reset