# input_handler.py

# Goals:
#   - Receive all raw input events (keyboard, mouse, etc.) from Kivy.
#   - Translate raw input events into game-specific actions (e.g., "move_up", "attack", "open_inventory").
#   - Call appropriate methods on the Game instance (or other game objects) in response to actions.
#   - Centralize input handling logic.
#   - Decouple input handling from the rest of the game logic.
#   - Make it easier to implement key rebinding.
#   - Facilitate a future multiplayer implementation.

# Interactions:
#   - app.py: The App class creates an instance of InputHandler and passes the Game instance to it.
#   - game.py: InputHandler calls methods on the Game instance (e.g., game.move_player(), game.open_inventory()).
#   - ui/screens/game_screen.py: No longer handles input directly.
#   - Kivy Framework: Receives input events from kivy.core.window.Window.

from kivy.core.window import Window
from kivy.uix.widget import Widget

class InputHandler(Widget): #Inherit from Widget
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Map key presses to game actions
        if keycode[1] == 'w':
            self.game.check_move(0, -1)  # Call methods on the Game instance
        elif keycode[1] == 's':
            self.game.check_move(0, 1)
        elif keycode[1] == 'a':
            self.game.check_move(-1, 0)
        elif keycode[1] == 'd':
            self.game.check_move(1, 0)
        elif keycode[1] == 'e':
            self.game.handle_interaction()
        elif keycode[1] == 'i':
            self.game.open_inventory() # Example
        elif keycode[1] == 'q':
            self.game.quit_game()
        elif keycode[1] == 'c': #Character Screen
            self.game.open_character_screen()
        # ... add more key bindings ...

        return True