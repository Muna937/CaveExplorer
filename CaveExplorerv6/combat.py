# combat.py

# Goals:
#   - Implement the combat system logic.
#   - Handle turn order (if turn-based).
#   - Handle attack calculations (damage, hit chance, critical hits).
#   - Manage combatant state (HP, status effects).
#   - Determine when combat ends (all enemies defeated, player defeated).
#   - (Optionally) Integrate with a separate combat screen (combat_screen.py).
#   - (Optionally) Handle AI for monsters.
#   - Provide a get_log method

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

from utils import roll_dice, calculate_distance  # Import both
import random
from item import Item, Weapon, Armor, Consumable
from kivy.app import App
from monster import Monster
class Combat:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.combatants = [self.player] + self.enemies
        self.current_turn_index = 0
        self.is_combat_over = False
        self.log = []

    def start_combat(self):
        self.log.append("Combat started!")
        # For simplicity, we'll keep the player-first turn order for now.
        # You can add more complex turn order determination later.

    def update(self, dt):
        if not self.is_combat_over:
            current_combatant = self.combatants[self.current_turn_index]

            if current_combatant == self.player:
                # Player's turn.  Wait for input from the UI.
                pass  # UI will call player_turn()
            else:
                # Monster's turn - use AI.
                self.monster_turn(current_combatant)  # Pass the monster instance
                self.next_turn()

    def next_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.combatants)

    def calculate_damage(self, attacker, defender):
        attack_roll = roll_dice(1, 20)
        # Use get_attack() and get_defense() to account for equipment
        total_attack = attacker.get_attack() + attack_roll
        total_defense = defender.get_defense()

        if attack_roll == 20:  # Critical hit!
            damage = (roll_dice(2, 6) + total_attack) - total_defense # Double damage dice
            self.log.append(f"{attacker.name} scores a CRITICAL HIT on {defender.name}!")
        elif total_attack > total_defense:
            damage = roll_dice(1, 6) + total_attack - total_defense
        else:
            self.log.append(f"{attacker.name} misses {defender.name}!")
            return 0  # No damage on a miss

        damage = max(0, damage) # Ensure damage isn't negative
         # Apply resistances/weaknesses (if applicable)
        if hasattr(defender, 'resistances') and attacker.damage_type in defender.resistances:
            damage = max(0, int(damage * (1- defender.resistances[attacker.damage_type]))) #reduce damage, can't go below 0
        if hasattr(defender, 'weaknesses') and attacker.damage_type in defender.weaknesses:
            damage = int(damage * (1 + defender.weaknesses[attacker.damage_type])) #Increase damage


        self.log.append(f"{attacker.name} hits {defender.name} for {damage} damage!")
        return damage

    def apply_damage(self, entity, damage):
        entity.take_damage(damage)
        if not entity.is_alive:
            self.log.append(f"{entity.name} is defeated!")
            self.remove_combatant(entity)

    def remove_combatant(self, entity):
        if entity in self.combatants:
            self.combatants.remove(entity)
        if entity in self.enemies:
            self.enemies.remove(entity)  # Remove from the enemy list
        if len(self.enemies) == 0:
            self.end_combat(victory=True)
        elif not self.player.is_alive:
            self.end_combat(victory=False)

        # NEW: Call game.remove_monster() if the entity is a monster
        if isinstance(entity, Monster):
            app = App.get_running_app()
            if app and app.game_instance:
                app.game_instance.remove_monster(entity)


    def player_turn(self, action, target=None):
        # Handle the player's turn
        if action == "attack":
            if target:
                damage = self.calculate_damage(self.player, target)
                self.apply_damage(target, damage)
            else:
                self.log.append("No target selected!")  # Should not happen with current UI
        # Add other actions (use_skill, use_item) later
        self.next_turn()

    def monster_turn(self, monster):
        # Use the AI module to determine the monster's action
        from ai import update_ai  # Import here to avoid circular imports
        app = App.get_running_app()
        if app and app.game_instance:
          update_ai(monster, app.game_instance, self, 0)  # Pass the game instance!

    def end_combat(self, victory):
        self.is_combat_over = True
        app = App.get_running_app()
        if victory:
            self.log.append("Victory!")
            # --- Give Rewards ---
            for monster in self.enemies:  # Iterate over original enemies
              if hasattr(monster, "experience"):
                self.player.experience += monster.experience
              if hasattr(monster, "gold_drop"):
                gold = random.randint(monster.gold_drop['min'], monster.gold_drop['max'])
                self.player.add_gold(gold)
                self.log.append(f"Gained {gold} gold!")

              # Handle item drops
              if hasattr(monster, "drops"):
                for drop in monster.drops:
                    if random.random() < drop["chance"]:
                        item_data = app.game_instance.items_data.get(drop["item_id"])
                        if item_data:
                            # Create item instance based on its type
                            if item_data["type"] == "consumable":
                                item = Consumable(
                                    item_id=item_data["item_id"],
                                    name=item_data["name"],
                                    item_type=item_data["type"],
                                    description=item_data["description"],
                                    value=item_data["value"],
                                    stackable=item_data["stackable"],
                                    max_stack=item_data["max_stack"],
                                    icon=item_data["icon"],
                                    effect=item_data["effect"]
                                )
                            elif item_data["type"] == "weapon":
                                item = Weapon(
                                    item_id=item_data["item_id"],
                                    name=item_data["name"],
                                    item_type=item_data["type"],
                                    description=item_data["description"],
                                    value=item_data["value"],
                                    stackable=item_data["stackable"],
                                    max_stack=item_data["max_stack"],
                                    icon=item_data["icon"],
                                    weapon_type=item_data["weapon_type"],
                                    attack=item_data["attack"],
                                    durability=item_data["durability"],
                                    max_durability=item_data["max_durability"],
                                    requirements=item_data["requirements"],
                                    effects=item_data["effects"]
                                )
                            elif item_data["type"] == "armor":
                                item = Armor(
                                    item_id=item_data["item_id"],
                                    name=item_data["name"],
                                    item_type=item_data["type"],
                                    description=item_data["description"],
                                    value=item_data["value"],
                                    stackable=item_data["stackable"],
                                    max_stack=item_data["max_stack"],
                                    icon=item_data["icon"],
                                    armor_type=item_data["armor_type"],
                                    defense=item_data["defense"],
                                    durability=item_data["durability"],
                                    max_durability=item_data["max_durability"],
                                    requirements=item_data["requirements"],
                                    effects=item_data["effects"]
                                )
                            else:  # Fallback to generic item
                                item = Item(
                                    item_id=item_data["item_id"],
                                    name=item_data["name"],
                                    item_type=item_data["type"],
                                    description=item_data["description"],
                                    value=item_data["value"],
                                    stackable=item_data["stackable"],
                                    max_stack=item_data["max_stack"],
                                    icon=item_data["icon"]
                                )
                            self.player.add_to_inventory(item)
                            self.log.append(f"Looted {item.name}!")
                        else:
                            print(f'Could not find item {drop["item_id"]}')

              if hasattr(monster, "monster_id"):
                app.game_instance.increment_kill_count(monster.monster_id)

        else:
            self.log.append("Defeat!")
            app.root.current = "game_over"  # Go to game over.

    def get_log(self):
        result = "\n".join(self.log)
        self.log = []  # Clear log after retrieving it
        return result