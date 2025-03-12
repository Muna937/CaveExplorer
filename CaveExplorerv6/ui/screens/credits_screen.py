# ui/screens/credits_screen.py

# Goals:
#   - Display credits for the game (developers, artists, music, libraries, etc.).
#   - Provide a visually appealing presentation (scrolling text, images, etc.).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock

class CreditsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Credits Text (ScrollView) ---
        self.scrollview = ScrollView()
        self.credits_label = Label(
            text=self.get_credits_text(),  # Get the credits text
            size_hint_y=None,
            halign='center'  # Center-align the text
        )
        self.credits_label.bind(texture_size=self.credits_label.setter('size'))
        self.scrollview.add_widget(self.credits_label)
        self.layout.add_widget(self.scrollview)


        # --- Back Button ---
        self.back_button = Button(text="Back to Main Menu", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        self.anim = None  # Store the animation object here

    def get_credits_text(self):
        # Define the credits text (you can also load this from a file).
        credits = """
        My Awesome RPG

        Developed by:
        Your Name Here

        Art by:
        Artist 1
        Artist 2

        Music by:
        Composer 1
        Composer 2

        Using Kivy:
        [ref=https://kivy.org]Kivy Website[/ref]

        Special Thanks:
        To everyone who helped!

        [size=24]Thank you for playing![/size]
        """
        return credits

    def on_enter(self):
        # Start the scrolling animation when the screen is entered.
        self.scrollview.scroll_y = 1  # Start at the top
        # Animate the scroll_y property to 0 over 30 seconds
        self.anim = Animation(scroll_y=0, duration=30)
        self.anim.start(self.scrollview)
        Clock.schedule_interval(self.check_scroll_end, 1.0 / 60.0)

    def on_leave(self):
      if self.anim:
        self.anim.stop(self.scrollview)
        Clock.unschedule(self.check_scroll_end)


    def check_scroll_end(self, dt):
      if self.scrollview.scroll_y <= 0.001 and self.anim and self.anim.have_properties_to_animate(self.scrollview):
        self.anim.stop(self.scrollview) # Stop current animation.
        self.anim = Animation(scroll_y = 1, duration=30) # Restart
        self.anim.start(self.scrollview)
        Clock.schedule_once(lambda dt: self.anim and self.anim.start(self.scrollview), 30) #delay repeat


    def go_back(self, instance):
        self.manager.current = "main_menu"