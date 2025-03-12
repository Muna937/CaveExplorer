from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text='Game Screen')
        self.add_widget(self.label)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_enter(self):
        # Get the GameClient instance from the app
       self.game_client = self.manager.parent.client
       self.game_client.game = self.manager.parent.client.game_client_app.root.get_screen('game')

    def update(self, dt):
        if self.manager.parent.connection.client:
          self.manager.parent.connection.check_connection_loop()
          if self.game_client.game:
            self.game_client.game.update(dt)
            self.label.text = f'Player ID: {self.game_client.player_id},  X: {self.game_client.game.local_player.x if self.game_client.game.local_player else ''}, Y:{self.game_client.game.local_player.y if self.game_client.game.local_player else ''}'
