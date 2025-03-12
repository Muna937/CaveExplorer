# monster.py

# Goals:
#   - Represent a monster in the game.
#   - Store monster-specific attributes (stats, drops, AI behavior).
#   - Handle monster actions (movement, combat).

# Interactions:
#   - entity.py: Inherits from the Entity class.
#   - game.py:  Creates and manages Monster instances.
#   - world.py:  Gets monster spawn locations from the map data.
#   - combat.py:  Participates in combat encounters.
#   - data/monsters.json:  Gets monster data (stats, drops, sprite).
#   - save_load.py:  Saves and loads monster state (if monsters are persistent).

from entity import Entity

class Monster(Entity):
    def __init__(self, monster_id, name, x, y, hp, max_hp, attack, defense, speed, experience, gold_drop, drops, sprite, ai, resistances, weaknesses):
        super().__init__(x, y, hp, name) # Call Entity constructor
        self.monster_id = monster_id
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.experience = experience
        self.gold_drop = gold_drop  # Dictionary: {"min": 1, "max": 5}
        self.drops = drops  # List of drop data
        self.sprite = sprite
        self.ai = ai  # String representing AI type (e.g., "basic_melee")
        self.resistances = resistances
        self.weaknesses = weaknesses

    def update(self, dt):
      super().update(dt) #call entity update
      #Handle AI
      pass

    def take_damage(self, damage):
      super().take_damage(damage) # Call parent class.

    def on_death(self):
      super().on_death() #Call parent class
      #Handle Drops
      pass

# Example Usage (in world.py or game.py):
# monster_data = load_json_data("data/monsters.json")["monsters"]["goblin"]
# monster = Monster(
#     monster_id="goblin",
#     name=monster_data["name"],
#    x=10,
#    y=5,
#     hp=monster_data["hp"],
#     max_hp = monster_data["max_hp"],
#     attack=monster_data["attack"],
#     defense=monster_data["defense"],
#    speed = monster_data["speed"],
#    experience = monster_data["experience"],
#    gold_drop = monster_data["gold_drop"],
#     drops=monster_data["drops"],
#     sprite=monster_data["sprite"],
#    ai = monster_data["ai"],
#    resistances = monster_data["resistances"],
#    weaknesses = monster_data["weaknesses"]
# )