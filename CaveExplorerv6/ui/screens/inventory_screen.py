# ui/screens/inventory_screen.py

# Goals:
#   - Display the player's inventory and equipped items.
#   - Allow the player to select items in their inventory.
#   - Provide buttons for using/equipping and dropping items.
#   - Update the display when items are added, removed, or equipped.
#   - Use the custom InventorySlot widget.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets the player's inventory data and equipped items via App.game_instance.
#   - player.py: Calls player.inventory methods (add_item, remove_item, equip_item, unequip_item).
#   - ui/widgets/inventory_slot.py: Uses InventorySlot widgets to display items.
#   - item.py:  Uses item data (name, description, type) for display and actions.
#   - kivy: Uses kivy for UI.
#   - utils.py: No direct interactions, but indirectly uses data loaded by utils.py.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App
from ui.widgets.inventory_slot import InventorySlot  # Import InventorySlot


class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Equipped Items ---
        self.equipped_layout = GridLayout(cols=2, size_hint_y=None, height=80)
        self.equipped_weapon_label = Label(text="Weapon: None")
        self.equipped_armor_label = Label(text="Armor: None")
        self.equipped_layout.add_widget(self.equipped_weapon_label)
        self.equipped_layout.add_widget(self.equipped_armor_label)
        self.layout.add_widget(self.equipped_layout)

        # --- Inventory Grid (inside a ScrollView) ---
        self.scrollview = ScrollView()
        self.inventory_grid = GridLayout(cols=4, size_hint_y=None)
        self.inventory_grid.bind(minimum_height=self.inventory_grid.setter('height'))
        self.scrollview.add_widget(self.inventory_grid)
        self.layout.add_widget(self.scrollview)

        # --- Item Info ---
        self.item_info_label = Label(text="Item Info", size_hint_y=None, height=40)
        self.layout.add_widget(self.item_info_label)

        # --- Buttons ---
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.use_button = Button(text="Use/Equip", size_hint_x=0.3, disabled=True)  # Combined button
        self.use_button.bind(on_press=self.use_equip_item)
        self.drop_button = Button(text="Drop", size_hint_x=0.3, disabled=True)
        self.drop_button.bind(on_press=self.drop_item)
        self.close_button = Button(text="Close", size_hint_x=0.3)
        self.close_button.bind(on_press=self.close_inventory)
        self.button_layout.add_widget(self.use_button)
        self.button_layout.add_widget(self.drop_button)
        self.button_layout.add_widget(self.close_button)

        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.selected_slot = None
        self.inventory_slots = []  # Keep track of InventorySlot widgets
        self.game = None #init

    def on_enter(self):
        self.game = App.get_running_app().game_instance #correct way to get game instance
        self.refresh_inventory()


    def update(self, dt):
        if self.game and self.game.player:
          #Update the equipped item labels
          if self.game.player.equipped_weapon:
              self.equipped_weapon_label.text = f"Weapon: {self.game.player.equipped_weapon.name}"
          else:
              self.equipped_weapon_label.text = "Weapon: None"

          if self.game.player.equipped_armor:
              self.equipped_armor_label.text = f"Armor: {self.game.player.equipped_armor.name}"
          else:
              self.equipped_armor_label.text = "Armor: None"


    def refresh_inventory(self):
      self.inventory_grid.clear_widgets()
      self.selected_slot = None
      self.use_button.disabled = True
      self.use_button.text = "Use/Equip" #reset
      self.drop_button.disabled = True
      self.item_info_label.text = "Item Info"
      self.inventory_slots = []

      if self.game and self.game.player:
          # Use InventorySlots instead of Buttons
          for i, item in enumerate(self.game.player.inventory.items):
              slot = InventorySlot()
              slot.update_slot(item)
              slot.slot_index = i  # Set the slot index
              slot.on_slot_pressed = self.select_item  # Set the callback
              self.inventory_grid.add_widget(slot)
              self.inventory_slots.append(slot)

          # Add empty slots to fill the capacity
          for i in range(len(self.game.player.inventory.items), self.game.player.inventory.capacity):
            slot = InventorySlot()
            slot.slot_index = i
            slot.on_slot_pressed = self.select_item
            self.inventory_grid.add_widget(slot)
            self.inventory_slots.append(slot)

    def select_item(self, slot_index):
        # Handle item selection (display info, enable buttons)
        if slot_index < len(self.game.player.inventory.items):
            self.selected_slot = slot_index
            item = self.game.player.inventory.items[slot_index]
            self.item_info_label.text = f"Name: {item.name}\nDescription: {item.description}"
            self.use_button.disabled = False
            self.drop_button.disabled = False

            if item.item_type == "consumable":
              self.use_button.text = "Use"
            elif item.item_type == "weapon" or item.item_type == "armor":
                self.use_button.text = "Equip"
            else:
              self.use_button.text = "Use/Equip" #shouldn't happen, but just in case
        else:
          # Clicked an empty slot
          self.selected_slot = None
          self.item_info_label.text = "Item Info"
          self.use_button.disabled = True
          self.drop_button.disabled = True

    def use_equip_item(self, instance):
      if self.selected_slot is not None and self.game and self.game.player:
          item = self.game.player.inventory.items[self.selected_slot]
          if item.item_type == "consumable":
              item.use(self.game.player)  # Use the item
              if item.quantity <= 0: #remove if empty
                self.game.player.remove_from_inventory(item)
              self.refresh_inventory()

          elif item.item_type == "weapon" or item.item_type == "armor":
            self.game.player.equip_item(self.selected_slot)
            self.refresh_inventory()
            self.update(0) #update equip display

    def drop_item(self, instance):
        if self.selected_slot is not None and self.game and self.game.player:
            item = self.game.player.inventory.items[self.selected_slot]
            self.game.player.remove_from_inventory(item)
            self.refresh_inventory()

    def close_inventory(self, instance):
        self.manager.current = "game"