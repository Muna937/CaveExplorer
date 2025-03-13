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

#entity.py
# entity.py
class Entity:
    def __init__(self, x, y, name, health=100):  # Correct order: x, y, name, health
        self.x = x
        self.y = y
        self.name = name
        self.health = health
        self.max_health = health  # Use max_health
        self.is_alive = True  # Use the attribute, not a method

    def update(self, dt):
        pass

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            self.on_death()

    def on_death(self):
        print(f"{self.name} has died!")  # Basic example

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health