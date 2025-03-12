# entity.py

# Goals:
#   - Define a base class for all game entities (player, monsters, NPCs).
#   - Store common attributes like position (x, y), health, etc.
#   - Provide common methods like moving, taking damage, checking if alive.
#   - Act as a base for inheritance (Player, Monster, NPC classes will inherit from Entity).

# Interactions:
#   - player.py: Player class inherits from Entity.
#   - combat.py: Combat system uses Entity objects to represent participants.
#   - game.py: Game logic creates and manages Entity instances.
#   - world.py: (Potentially) World might interact with entities for collision detection.
#   - ui/ (indirectly): UI elements might display Entity information (e.g., health bars).
#      This interaction happens through game.py, which provides data to the UI.

# Example Structure:
class Entity:
    def __init__(self, x, y, health, name="Entity"):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health  # Store max health for healing, etc.
        self.name = name
        self.is_alive = True

    def move(self, dx, dy):
        # Basic movement (can be overridden in subclasses).
        self.x += dx
        self.y += dy

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0  # Prevent negative health
            self.is_alive = False
            self.on_death()

    def on_death(self):
        # Actions to perform when the entity dies (e.g., play a sound, drop items).
        print(f"{self.name} has died!") #Basic Example

    def update(self, dt):
      #Update the entity
      pass