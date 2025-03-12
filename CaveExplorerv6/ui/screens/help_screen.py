# ui/screens/help_screen.py

# Goals:
#   - Provide information to the player about the game.
#   - Explain controls, game mechanics, lore, or any other relevant details.
#   - Offer a user-friendly way to access help information.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Help Text (ScrollView) ---
        self.scrollview = ScrollView()
        self.help_label = Label(text=self.get_help_text(), size_hint_y=None, halign='left', valign='top')
        self.help_label.bind(texture_size=self.help_label.setter('size'))  # For text wrapping
        self.scrollview.add_widget(self.help_label)
        self.layout.add_widget(self.scrollview)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def get_help_text(self):
        # Define the help text (you can also load this from a file).
        help_text = """
        [b]My Awesome RPG - Help[/b]

        [size=18]Controls:[/size]

        - [b]Movement:[/b] WASD keys
        - [b]Interact:[/b] E key
        - [b]Inventory:[/b] I key
        - [b]Character Sheet:[/b] C Key
        - [b]Quest Log:[/b] Q Key
        - [b]Map(If Applicable):[/b] M Key
        - [b]Options:[/b] ESC Key (Usually goes to the main menu or a pause menu first)

        [size=18]Gameplay:[/size]

        - Explore the world and talk to NPCs.
        - Complete quests to earn rewards and experience.
        - Defeat monsters in combat to gain experience and loot.
        - Manage your inventory and equip powerful items.
        - Level up your character and improve your stats.
        - Craft new items.

        [size=18]Tips:[/size]

        - Save your game often!
        - Talk to everyone you meet.  They might have useful information or quests.
        - Explore thoroughly.  There might be hidden treasures or secrets.
        - Don't be afraid to experiment with different skills and items.

        [size=18]Credits[/size]
        Add in credits here
        """
        return help_text

    def go_back(self, instance):
        self.manager.current = "game"  # Or "main_menu", depending on where you want to go back to