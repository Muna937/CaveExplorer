# ui/screens/combat_screen.py

# Goals:
#   - Display the combat interface.
#   - Show combatants (player and enemies), their health, and other relevant stats.
#   - Provide controls for player actions (attack, use skills, use items, flee).
#   - Display combat messages (damage dealt, status effects, etc.).
#   - Handle turn order and transitions between turns (visually).
#   - Get combat information from the Combat instance.
#   - Send player actions to the Combat instance.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py:  Gets the Combat instance when combat starts.
#   - combat.py:  Gets updates from the combat system (turn, health, log).
#   - player.py:  Gets player information (health, skills, etc.).
#   - entity.py: Gets entity information.
#   - monster.py: Gets enemy information.
#   - skills.py:  If skills are used in combat, displays available skills.
#   - inventory.py (potentially):  If items can be used in combat.
#   - ui/widgets/: Might use custom widgets (e.g., health bars, action buttons).
#   - kivy: Uses Kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App  # Import App


class CombatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Combatant Display (Example: Simple labels for now) ---
        self.combatants_layout = GridLayout(cols=2)
        self.player_label = Label(text="Player HP: ")
        self.enemy_label = Label(text="Enemy HP: ")
        self.combatants_layout.add_widget(self.player_label)
        self.combatants_layout.add_widget(self.enemy_label)
        self.layout.add_widget(self.combatants_layout)

        # --- Action Buttons ---
        self.actions_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.attack_button = Button(text="Attack")
        self.attack_button.bind(on_press=self.player_attack)
        self.skills_button = Button(text="Skills")
        # self.skills_button.bind(on_press=self.show_skills) # You'd need a skill selection UI
        self.items_button = Button(text="Items")
        # self.items_button.bind(on_press=self.show_items)  # You'd need an item selection UI
        self.flee_button = Button(text="Flee")
        # self.flee_button.bind(on_press=self.attempt_flee)

        self.actions_layout.add_widget(self.attack_button)
        self.actions_layout.add_widget(self.skills_button)
        self.actions_layout.add_widget(self.items_button)
        self.actions_layout.add_widget(self.flee_button)
        self.layout.add_widget(self.actions_layout)

        # --- Combat Log (Example: Simple label) ---
        self.log_label = Label(text="Combat Log", size_hint_y=None, height=100, markup=True) #Added markup
        self.layout.add_widget(self.log_label)

        # --- Back Button (for testing - you'd normally exit combat differently) ---
        self.back_button = Button(text="Back to Game (TEMP)", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.combat = None #Keep track of combat instance


    def on_enter(self):
        # Initialize combat (get combat instance from game.py).
        self.game = App.get_running_app().game_instance
        self.combat = self.game.combat  # Get combat instance
        self.update_combat_info()



    def update(self, dt):
        # Update combat information (health bars, combat log, etc.).
        if self.combat:
            self.combat.update(dt)  # *Crucially* update the Combat instance
            self.update_combat_info()  # Update UI
            if not self.combat.player.is_alive:
              #Game over screen if player is dead
              self.game.show_game_screen() #go back to game, will add game over later
            if self.combat.is_combat_over:
              self.game.show_game_screen() #go back to game.

    def update_combat_info(self):
      # Update combat information (health bars, combat log, etc.).
      if self.combat:
        self.player_label.text = f"Player HP: {self.combat.player.health} / {self.combat.player.max_health}"
        if self.combat.enemies: #Make sure enemy exists
          self.enemy_label.text = f"Enemy HP: {self.combat.enemies[0].health} / {self.combat.enemies[0].max_health}" #get first enemy
        self.log_label.text = self.combat.get_log()

    def player_attack(self, instance):
        # Handle the player's attack action.
        if self.combat and self.combat.current_turn_index == 0 : #player turn
            # For now, assume the target is the first enemy.  Later, you'll need
            # a way for the player to select a target.
            target = self.combat.enemies[0] if self.combat.enemies else None #get first enemy
            if target:
              self.combat.player_turn("attack", target)
            #self.update_combat_info() #Update after every action

    # ... other methods for handling skills, items, fleeing ...

    def go_back(self, instance):
      self.manager.current = "game"