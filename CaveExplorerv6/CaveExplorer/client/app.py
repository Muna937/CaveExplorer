from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from client.ui.screens.login_screen import LoginScreen
from client.ui.screens.game_screen import GameScreen
from client.network import GameClient
from client.connection import ClientConnection


class GameClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the connection here, but don't connect yet
        self.connection = ClientConnection(self)
        self.client = None  # Will hold the GameClient instance

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(GameScreen(name='game'))
        return self.sm

    def on_stop(self):
        # Make sure to disconnect cleanly when the app closes
        if self.client:
            self.client.close_connection()
