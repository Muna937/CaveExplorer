# entity.py

# Goals:
#   - Define a base class for all entities in the game (player, NPCs, monsters).
#   - Provide common attributes and methods that all entities share.
#   - Abstract away common functionality to avoid code duplication.

# Interactions:
#   - player.py: Player inherits from Entity.
#   - npc.py: NPC inherits from Entity.
#   - monster.py: Monster inherits from Entity.
#   - combat.py: (Potentially) Used for combat calculations.
#   - game.py: Manages entities.
#   - save_load.py: (Potentially) Saves and loads entity data.

class Entity:
    def __init__(self, x, y, health, name):
        self.x = x  # World coordinates (not tile coordinates)
        self.y = y
        self.health = health
        self.max_health = health #Added
        self.name = name
        self.is_alive = True

    def update(self, dt):
        # Common update logic for all entities (e.g., animation).
        # This might be empty in many cases.
        pass

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0 #prevent negative health
            self.on_death() # Trigger any on-death effects.

    def on_death(self):
      self.is_alive = False
      # Common death handling (e.g., play death animation, remove from world)
      pass

    def heal(self, amount):
      self.health += amount
      if self.health > self.max_health:
        self.health = self.max_health