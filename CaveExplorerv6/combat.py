# combat.py

# Goals:
#   - Implement the combat system logic.
#   - Handle turn order (if turn-based).
#   - Handle attack calculations (damage, hit chance, critical hits).
#   - Manage combatant state (HP, status effects).
#   - Determine when combat ends (all enemies defeated, player defeated).
#   - (Optionally) Integrate with a separate combat screen (combat_screen.py).
#   - (Optionally) Handle AI for monsters.

# Interactions:
#   - game.py:  Initiates combat encounters.
#   - player.py:  Gets player stats and actions.
#   - entity.py:  Gets/sets entity HP, applies status effects.
#   - monster.py: Gets monster stats and actions.
#   - skills.py:  Uses skill effects during combat.
#   - items.py (potentially):  If items can be used in combat.
#   - ui/screens/combat_screen.py (potentially):  Displays combat information.
#   - ai.py (potentially):  Used for monster AI.
#   - save_load.py: (Potentially) If you allow saving/loading during combat.
# -  utils.py: For calculations
#  - constants.py for constants

from utils import roll_dice # Example utility function

class Combat:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies  # List of Monster instances
        self.combatants = [self.player] + self.enemies # List of all combat participants
        self.current_turn_index = 0  # Index of the current combatant
        self.is_combat_over = False
        self.log = []  # Combat log (for displaying messages)

    def start_combat(self):
        # Initialize combat state (e.g., determine turn order)
        self.log.append("Combat started!")
        #Simple turn order, could be based on speed
        #self.combatants.sort(key=lambda entity: entity.speed, reverse=True)

    def update(self, dt):
      if not self.is_combat_over:
        current_combatant = self.combatants[self.current_turn_index]

        if current_combatant == self.player:
            # Player's turn - wait for player input (from UI)
            # Example (assuming a method in combat_screen.py):
            # self.ui.show_player_options(self.player.get_available_actions())
            pass #Wait for player input.
        else:
            # Monster's turn - use AI
            self.monster_turn(current_combatant)
            self.next_turn() # Go to the next turn immediately after the monster acts

    def next_turn(self):
      self.current_turn_index = (self.current_turn_index + 1) % len(self.combatants)
      if self.current_turn_index == 0: #back to player
        pass #Handle start of player turn (e.g. status effects on player turn start)

    def calculate_damage(self, attacker, defender):
        # Basic damage calculation (replace with your actual formula)
        attack_roll = roll_dice(1, 20) + attacker.attack  # Example: 1d20 + attack bonus
        if attack_roll >= defender.defense:
            damage = roll_dice(1, 6) + attacker.attack - defender.defense  # Example: 1d6 + attack - defense
            damage = max(0, damage)  # Ensure damage is not negative
            self.log.append(f"{attacker.name} hits {defender.name} for {damage} damage!")
            return damage
        else:
            self.log.append(f"{attacker.name} misses {defender.name}!")
            return 0

    def apply_damage(self, entity, damage):
        entity.take_damage(damage)
        if not entity.is_alive:
            self.log.append(f"{entity.name} is defeated!")
            self.remove_combatant(entity) #remove from combat.

    def remove_combatant(self, entity):
      if entity in self.combatants:
        self.combatants.remove(entity)
      if entity in self.enemies:
        self.enemies.remove(entity) #remove from enemy list
      if len(self.enemies) == 0:
        self.end_combat(victory=True)
      elif not self.player.is_alive:
        self.end_combat(victory=False)
    def player_turn(self, action, target=None):
        #Handle the players turn
        # Example actions: "attack", "use_skill", "use_item"
        if action == "attack":
          if target:
            damage = self.calculate_damage(self.player, target)
            self.apply_damage(target, damage)
          else:
            self.log.append("No Target Selected")

        elif action == "use_skill":
          pass #will add later

        elif action == "use_item":
          pass
        self.next_turn()

    def monster_turn(self, monster):
        # Simple AI: Just attack the player
        damage = self.calculate_damage(monster, self.player)
        self.apply_damage(self.player, damage)

    def end_combat(self, victory):
      self.is_combat_over = True
      if victory:
        self.log.append("Victory!")
        #Handle giving rewards (exp, gold, items)
      else:
        self.log.append("Defeat!")
        #Handle game over.

    def get_log(self):
      return "\\n".join(self.log)