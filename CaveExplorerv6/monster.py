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

# monster.py

# monster.py
from entity import Entity

class Monster(Entity):
    def __init__(self, monster_id, name, x, y, hp, max_hp, attack, defense, speed, experience, gold_drop, drops, sprite, ai, resistances, weaknesses):
        super().__init__(x, y, name, hp)  # Pass name and hp to Entity
        self.monster_id = monster_id
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.experience = experience
        self.gold_drop = gold_drop
        self.drops = drops
        self.sprite = sprite
        self.ai = ai
        self.resistances = resistances
        self.weaknesses = weaknesses
        self.damage_type = "physical"  # Add damage_type

    def update(self, dt):
        super().update(dt)
        # AI logic will go here (eventually)

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def take_damage(self, damage):
        super().take_damage(damage)  # Call parent class.

    def on_death(self):
        super().on_death()
        # Add any monster-specific death logic (animations, sounds, etc.)