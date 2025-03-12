# item.py

# Goals:
#   - Define an Item class to represent items in the game.
#   - Store item properties (name, type, description, value, etc.).
#   - Handle item-specific logic (using consumables, equipping weapons/armor).

# Interactions:
#   - inventory.py: Inventory stores Item instances.
#   - data/items.json:  Gets item data.
#   - data/weapons.json: (If separated) Gets weapon data.
#   - data/armor.json: (If separated) Gets armor data.
#   - player.py:  Player equips and uses items.
#   - combat.py:  Weapons and armor affect combat.
#   - game.py: Creates item instances
#   - ui/:  Displays item information.
#   - save_load.py: Saves and loads item instances.

class Item:
    def __init__(self, item_id, name, item_type, description, value, stackable, max_stack, icon, quantity=1):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.description = description
        self.value = value
        self.stackable = stackable
        self.max_stack = max_stack
        self.icon = icon
        self.quantity = quantity #always track quantity

    def use(self, user):
      #Default use
      print(f'Using item {self.name}')
      pass

class Consumable(Item):
    def __init__(self, item_id, name, item_type, description, value, stackable, max_stack, icon, effect, quantity = 1):
      super().__init__(item_id, name, item_type, description, value, stackable, max_stack, icon, quantity)
      self.effect = effect #dictionary
    def use(self, user):
      #Handle effects, remove if needed.
      super().use(user) # Call base class
      print(f'Consuming {self.name}')
      if "hp" in self.effect:
        user.health += self.effect['hp']
        if user.health > user.max_health:
          user.health = user.max_health
      #TODO: handle other effects.
      self.quantity -= 1 #reduce quantity

class Weapon(Item):
  def __init__(self, item_id, name, item_type, description, value, stackable, max_stack, icon, weapon_type, attack, durability, max_durability, requirements, effects, quantity=1):
    super().__init__(item_id, name, item_type, description, value, stackable, max_stack, icon, quantity)
    self.weapon_type = weapon_type
    self.attack = attack
    self.durability = durability
    self.max_durability = max_durability
    self.requirements = requirements
    self.effects = effects
    def use(self, user):
      super().use(user)
      #Equip

class Armor(Item):
  def __init__(self, item_id, name, item_type, description, value, stackable, max_stack, icon, armor_type, defense, durability, max_durability, requirements, effects, quantity = 1):
    super().__init__(item_id, name, item_type, description, value, stackable, max_stack, icon, quantity)
    self.armor_type = armor_type
    self.defense = defense
    self.durability = durability
    self.max_durability = max_durability
    self.requirements = requirements
    self.effects = effects
  def use(self, user):
      super().use(user)
      #Equip


# Example Usage (in game.py or inventory.py):
# items_data = load_json_data("data/items.json")["items"]
# potion_data = items_data["potion"]
# potion = Consumable(
#     item_id="potion",
#     name=potion_data["name"],
#     item_type=potion_data["type"],
#     description=potion_data["description"],
#     value=potion_data["value"],
#    stackable = potion_data["stackable"],
#    max_stack = potion_data["max_stack"],
#     icon=potion_data["icon"],
#     effect=potion_data["effect"]
# )
# # ... add potion to inventory ...
# potion.use(player)  # Use the potion