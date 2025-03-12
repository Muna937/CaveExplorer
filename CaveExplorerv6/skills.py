# skills.py

# Goals:
#   - Define classes for different skills/abilities.
#   - Store skill data (name, description, cost, effects, etc.).
#   - Provide methods for using skills (applying their effects).
#   - (Optionally) Handle skill cooldowns.
#   - (Optionally) Handle skill leveling/upgrades.

# Interactions:
#   - player.py: Player class will use and manage Skill instances.
#   - combat.py: Combat system might use skills to apply effects during combat.
#   - entity.py (potentially): Skills might affect entities (e.g., deal damage, apply buffs/debuffs).
#   - ui/screens/character_screen.py (and potentially game_screen.py):
#       - Displays available skills and allows the player to use them.
#   - data/skills.json (likely loaded via utils.py or a dedicated data loading module):
#       - Skill data (descriptions, costs, effects) could be loaded from a JSON file.
#   - save_load.py: Skill data (learned skills, skill levels) needs to be saved and loaded.


class Skill:
    def __init__(self, name, description, cost, effect):
        self.name = name
        self.description = description
        self.cost = cost  # e.g., mana cost, stamina cost
        self.effect = effect  # A function or object that defines the skill's effect.
        self.cooldown = 0  # Optional: Cooldown in turns/seconds.
        self.current_cooldown = 0

    def use(self, user, target):
        # Check if the skill can be used (enough cost, not on cooldown).
        if self.current_cooldown > 0:
            print(f"{self.name} is on cooldown!")  # Or handle in UI
            return False
        # In a real game, check that user has resources to use skill.

        # Apply the skill's effect.
        if self.effect:
           if self.effect(user, target): #effect returns true
              self.current_cooldown = self.cooldown #apply the cooldown.
              return True #skill was used
           else:
              return False #could not use the skill
        return False

    def update(self, dt):
        # Update the skill's state (e.g., reduce cooldown).
        if self.current_cooldown > 0:
            self.current_cooldown -= dt

    def can_use(self, user):
      #check if a skill can be used, checking for costs
      return self.current_cooldown <= 0

# Example skill effects (could be defined in a separate module or within the Skill class):
def damage_effect(user, target, damage):
    if target:
      target.take_damage(damage)
      print(f"{user.name} used a skill on {target.name}, dealing {damage} damage!")
      return True
    else:
       print("No target")
       return False

def heal_effect(user, target, amount):
    if target:
      target.health += amount
      if target.health > target.max_health:
        target.health = target.max_health
      print(f"{user.name} used a healing skill on {target.name}, healing {amount} HP!")
      return True
    else:
      print("No Target")
      return False

# Example skill instances:
fireball = Skill(
    name="Fireball",
    description="Launches a fiery projectile.",
    cost=10,
    effect=lambda user, target: damage_effect(user, target, 20)  # Use a lambda for simple effects
)

heal = Skill(
    name="Heal",
    description="Restores health to a target.",
    cost=15,
    effect=lambda user, target: heal_effect(user, target, 25)
)
# Example Usage (in player.py or combat.py):

# player.skills["Fireball"] = fireball
# player.skills["Heal"] = heal
#
# target = get_enemy()  # Get a target somehow
# if "Fireball" in player.skills:
#   success = player.skills["Fireball"].use(player, target) # Pass user and target
#   if success:
#      print("Used skill")
#
#   # ... later, in the game loop ...
#for skill_name, skill in player.skills.items():
#   skill.update(dt)