# ui/screens/game_screen.py

# Goals:
#   - Display the main game world (map, player, entities).
#   - Handle player input (movement, actions).
#   - Interact with the Game instance to update the game state.
#   - Provide a user interface for interacting with the game world.

# Interactions:
#   - app.py: Added to the ScreenManager by app.py. Receives the Game instance.
#   - game.py: Gets game state information (player position, map data, etc.).
#                 Sends player input to the game.
#   - player.py:  (Indirectly) Controls the player's actions through game.py.
#   - world.py:  (Indirectly) Gets map data for rendering through game.py.
#   - ui/widgets/: May use custom widgets for UI elements (e.g., health bar).
#   - kivy.input:  Handles keyboard/mouse/touch input.
#   - ui/screens/inventory_screen.py (potentially):  Can switch to the inventory screen.
#   - ui/screens/character_screen.py (potentially): Can switch to the character screen.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

class GameScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.label = Label(text="Game Screen")  # Placeholder
        self.add_widget(self.label)

        # --- UI Setup (Example: Buttons for menus) ---
        self.ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.inventory_button = Button(text="Inventory")
        self.inventory_button.bind(on_press=self.go_to_inventory)
        self.character_button = Button(text="Character")
        self.character_button.bind(on_press=self.go_to_character)
        self.ui_layout.add_widget(self.inventory_button)
        self.ui_layout.add_widget(self.character_button)
        self.add_widget(self.ui_layout)


        # --- Input Handling ---
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def on_enter(self):
        # Start/resume the game when the screen is entered.
        pass #add anything to happen on enter

    def update(self, dt):
        self.game.update(dt)
        self.label.text = f'Player X: {self.game.player.x}, Y: {self.game.player.y}'

    def go_to_inventory(self, instance):
        self.manager.current = "inventory" # Switch to Inventory Screen

    def go_to_character(self, instance):
        self.manager.current = "character"  # Switch to character screen

    def _keyboard_closed(self):
        # Cleanup when the keyboard is closed.
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Handle keyboard input.  keycode is a tuple: (key_code, key_name)
        if keycode[1] == 'w':
            self.game.player.move(0, -1)  # Move up
        elif keycode[1] == 's':
            self.game.player.move(0, 1)  # Move down
        elif keycode[1] == 'a':
            self.game.player.move(-1, 0)  # Move left
        elif keycode[1] == 'd':
            self.game.player.move(1, 0)  # Move right
        elif keycode[1] == 'q':
            self.game.quit_game() #quit the game

        return True  # Consumed the key event