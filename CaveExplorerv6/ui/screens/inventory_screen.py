# ui/screens/inventory_screen.py

# Goals:
#   - Display the player's inventory to the user.
#   - Allow the player to interact with items (use, equip, drop, etc.).
#   - Provide a clear and user-friendly interface.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets the player's inventory data from the Game instance.
#   - player.py: Accesses the player's inventory (via the Game instance).
#   - ui/widgets/ (potentially):  Could use custom widgets to display inventory slots.
#   - ui/screens/game_screen.py:  Typically, you'll switch back to the game screen
#     after closing the inventory.
#   - items.json (indirectly):  Gets item information (name, description, etc.)
#     to display.
#   - kivy: Uses kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')

        # --- Inventory Grid (inside a ScrollView) ---
        self.scrollview = ScrollView()
        self.inventory_grid = GridLayout(cols=4, size_hint_y=None)
        self.inventory_grid.bind(minimum_height=self.inventory_grid.setter('height')) #for scrolling
        self.scrollview.add_widget(self.inventory_grid)
        self.layout.add_widget(self.scrollview)

        # --- Item Info ---
        self.item_info_label = Label(text="Item Info", size_hint_y=None, height=40)
        self.layout.add_widget(self.item_info_label)

        # --- Buttons ---
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.use_button = Button(text="Use", size_hint_x = 0.3, disabled = True)
        self.use_button.bind(on_press=self.use_item)
        self.drop_button = Button(text="Drop", size_hint_x = 0.3, disabled = True)
        self.drop_button.bind(on_press=self.drop_item)
        self.close_button = Button(text="Close", size_hint_x = 0.3)
        self.close_button.bind(on_press=self.close_inventory)
        self.button_layout.add_widget(self.use_button)
        self.button_layout.add_widget(self.drop_button)
        self.button_layout.add_widget(self.close_button)

        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.selected_item = None  # Store the currently selected item.



    def on_enter(self):
      self.game = self.manager.parent.game_instance
      self.refresh_inventory()

    def update(self, dt):
      pass

    def refresh_inventory(self):
        # Clear existing items
        self.inventory_grid.clear_widgets()
        self.selected_item = None
        self.use_button.disabled = True
        self.drop_button.disabled = True
        self.item_info_label.text = "Item Info"

        # Add items from the player's inventory
        if self.game and self.game.player:  # Check if game and player exist
            for item_data in self.game.player.inventory.get_items():
                # Create a button for each item
                item_button = Button(text=item_data["name"])
                item_button.bind(on_press=lambda instance, item=item_data: self.select_item(item))
                self.inventory_grid.add_widget(item_button)

    def select_item(self, item_data):
        # Handle item selection (display info, enable buttons)
        self.selected_item = item_data
        self.item_info_label.text = f"Name: {item_data['name']}\\nDescription: {item_data['description']}"  # Show name and description
        #Enable buttons based on context
        self.use_button.disabled = False
        self.drop_button.disabled = False

        if item_data['type'] != "consumable":
            self.use_button.disabled = True # Disable the use button for non consumables
            self.use_button.text = "Use"
        else:
          self.use_button.text = "Use"



    def use_item(self, instance):
      if self.selected_item and self.game and self.game.player:
          # Handle using the item (e.g., consume potion, equip weapon)
          print("Using item:", self.selected_item["name"])
          if self.selected_item['type'] == "consumable":
            if "hp" in self.selected_item['effect']:
              self.game.player.health += self.selected_item['effect']['hp']
              if self.game.player.health > self.game.player.max_health:
                self.game.player.health = self.game.player.max_health
            elif "mp" in self.selected_item['effect']:
              pass #Handle mana
            self.game.player.remove_from_inventory(self.selected_item) #Remove from inventory.
            self.refresh_inventory() #Refresh UI


    def drop_item(self, instance):
        # Handle dropping the item
        if self.selected_item and self.game and self.game.player:
          print("Dropping item", self.selected_item['name'])
          self.game.player.remove_from_inventory(self.selected_item)
          self.refresh_inventory()

    def close_inventory(self, instance):
        self.manager.current = "game"  # Go back to the game screen