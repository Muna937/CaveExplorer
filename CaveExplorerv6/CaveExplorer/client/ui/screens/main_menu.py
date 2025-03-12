from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Main Menu'))
        play_button = Button(text='Play Game')
        play_button.bind(on_press=self.go_to_game_screen)
        layout.add_widget(play_button)
        layout.add_widget(Button(text='Options'))
        layout.add_widget(Button(text='Exit'))
        self.add_widget(layout)

    def go_to_game_screen(self, instance):
        self.manager.current = 'login'  # Assuming you have a login screen.
