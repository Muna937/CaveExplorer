from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.host_input = TextInput(hint_text='Host', multiline=False)
        self.port_input = TextInput(hint_text='Port', multiline=False)
        self.connect_button = Button(text='Connect')
        self.connect_button.bind(on_press=self.connect_to_server)
        self.status_label = Label(text='')  # Label to display connection status
        self.layout.add_widget(self.host_input)
        self.layout.add_widget(self.port_input)
        self.layout.add_widget(self.connect_button)
        self.layout.add_widget(self.status_label)
        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def connect_to_server(self, instance):
      host = self.host_input.text
      port = self.port_input.text

      app = self.manager.parent  # Access the App instance
      success, message = app.connection.connect(host, port)
      if success:
        self.status_label.text = 'Connecting...'
        #Transition to game screen handled in the network updates.
      else:
        self.status_label.text = f'Connection failed: {message}'

    def update(self, dt):
        if self.manager.parent.connection.client:
          self.manager.parent.connection.check_connection_loop()
          if self.manager.parent.connection.client.player_id is not None:
            self.status_label.text = 'Connected'
            self.manager.current = 'game'
