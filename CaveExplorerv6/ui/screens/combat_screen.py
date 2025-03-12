# ui/screens/combat_screen.py

# Goals:
#   - Display the combat interface (if separate from game_screen.py).
#   - Show combatants (player and enemies), their health, and other relevant stats.
#   - Provide controls for player actions (attack, use skills, use items, flee).
#   - Display combat messages (damage dealt, status effects, etc.).
#   - Handle turn order and transitions between turns.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Receives combat information (combatants, turn order, etc.).
#                Sends player actions to the combat system.
#   - combat.py:  Gets updates from the combat system.
#   - player.py:  Gets player information (health, skills, etc.).
#   - entity.py (or monster.py): Gets enemy information.
#   - skills.py:  If skills are used in combat, displays available skills.
#   - inventory.py (potentially):  If items can be used in combat.
#   - ui/widgets/: Might use custom widgets (e.g., health bars, action buttons).
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

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
        self.log_label = Label(text="Combat Log", size_hint_y=None, height=100)
        self.layout.add_widget(self.log_label)

        # --- Back Button (for testing - you'd normally exit combat differently) ---
        self.back_button = Button(text="Back to Game (TEMP)", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def on_enter(self):
        # Initialize combat (get combat instance from game.py).
        self.game = self.manager.parent.game_instance
        #  self.combat = self.game.current_combat  # Assuming game.py has a current_combat attribute
        #  self.update_combat_info()
        pass


    def update(self, dt):
        # Update combat information (health bars, combat log, etc.).
        # You'd get this information from the Combat instance.
        # Example (replace with actual data from your combat system):
      #   if self.combat:
      #     self.player_label.text = f"Player HP: {self.combat.player.health}"  # Assuming Combat has player and enemy
      #     self.enemy_label.text = f"Enemy HP: {self.combat.enemy.health}"
      #     self.log_label.text += self.combat.get_log_messages() #get log messages from combat
      pass

    def player_attack(self, instance):
        # Handle the player's attack action.
        # Example:
        # if self.combat:
        #     self.combat.player_turn("attack") # Tell combat its the players turn
        pass

    # ... other methods for handling skills, items, fleeing ...

    def go_back(self, instance):
        self.manager.current = "game"

# --- Temporary Example Data (for testing) ---
class TempEntity:
  def __init__(self, name, health):
    self.name = name
    self.health = health

class TempCombat:
  def __init__(self, player, enemy):
    self.player = player
    self.enemy = enemy
    self.log = []

  def player_turn(self, action):
    if action == "attack":
      damage = 10 #random damage
      self.enemy.health -= damage
      self.log.append(f'Player attacks, dealing {damage}')
      if self.enemy.health <=0:
        self.log.append("Enemy defeated!")

  def get_log_messages(self):
    result = "\\n".join(self.log)
    self.log = [] #clear log
    return result