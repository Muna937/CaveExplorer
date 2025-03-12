# ui/screens/quest_log_screen.py

# Goals:
#   - Display the player's active and (optionally) completed quests.
#   - Show quest details (name, description, objectives, progress).
#   - Provide a user-friendly interface for tracking quests.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets quest data from the Game instance.
#   - player.py (potentially, via game.py): Accesses the player's quest log.
#   - quests.py:  Gets quest information (using data loaded from quests.json).
#   - ui/widgets/: Might use custom widgets for displaying quest entries.
#   - kivy: Uses kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class QuestLogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Quest List (inside a ScrollView) ---
        self.scrollview = ScrollView()
        self.quest_list = GridLayout(cols=1, size_hint_y=None)
        self.quest_list.bind(minimum_height=self.quest_list.setter('height'))
        self.scrollview.add_widget(self.quest_list)
        self.layout.add_widget(self.scrollview)

        # --- Quest Details ---
        self.details_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
        self.quest_name_label = Label(text="Quest Name", font_size=20)
        self.quest_description_label = Label(text="Quest Description", text_size=(400, None)) #text_size for wrapping
        self.objective_label = Label(text = "Objectives")

        self.details_layout.add_widget(self.quest_name_label)
        self.details_layout.add_widget(self.quest_description_label)
        self.details_layout.add_widget(self.objective_label)
        self.layout.add_widget(self.details_layout)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.selected_quest = None

    def on_enter(self):
        self.game = self.manager.parent.game_instance
        self.refresh_quests()

    def update(self, dt):
        pass

    def refresh_quests(self):
        # Clear existing quest entries
        self.quest_list.clear_widgets()
        self.selected_quest = None
        self.update_quest_details()

        # Add entries for active quests (you'll need to adapt this to your quest system)
        if self.game and self.game.player:  # Check if game and player are initialized
            # Example: Assuming you have a list of active quests in game.player.quests
            # and each quest has a 'name' attribute.  Adapt this to your actual structure.
            # for quest in self.game.player.quests:
            #     quest_button = Button(text=quest.name, size_hint_y=None, height=40)
            #     quest_button.bind(on_press=lambda instance, q=quest: self.select_quest(q))
            #     self.quest_list.add_widget(quest_button)

            #Temporary example:
            for quest in [quest1, quest2]: #Iterate through quests.
                quest_button = Button(text=quest.name, size_hint_y=None, height=40)
                quest_button.bind(on_press= lambda instance, q=quest: self.select_quest(q))
                self.quest_list.add_widget(quest_button)


    def select_quest(self, quest):
        # Handle quest selection (display details)
        self.selected_quest = quest
        self.update_quest_details()


    def update_quest_details(self):
        # Update the labels with details of the selected quest.
      if self.selected_quest:
        self.quest_name_label.text = self.selected_quest.name
        self.quest_description_label.text = self.selected_quest.description
        objectives_text = ""
        for objective in self.selected_quest.objectives:
            objectives_text += f"- {objective.type} {objective.target}: {objective.current_amount}/{objective.amount}\\n"
        self.objective_label.text = objectives_text
      else:
        self.quest_name_label.text = "Quest Name"
        self.quest_description_label.text = "Quest Description"
        self.objective_label.text = "Objectives"


    def go_back(self, instance):
        self.manager.current = "game"

# --- Temporary Example Quest Data (for testing) ---
# In a real game, this would come from your quests.json and quests.py.
class TempObjective:
    def __init__(self, type, target, amount):
        self.type = type
        self.target = target
        self.amount = amount
        self.current_amount = 0
        self.is_complete = False
class TempQuest:
    def __init__(self, name, description, objectives):
        self.name = name
        self.description = description
        self.objectives = objectives

objective1 = TempObjective("kill", "goblin", 5)
objective2 = TempObjective("collect", "potion", 3)
quest1 = TempQuest("Goblin Hunt", "Kill 5 goblins and collect 3 potions", [objective1, objective2])
quest2 = TempQuest("Another Quest", "Do something else.", [])