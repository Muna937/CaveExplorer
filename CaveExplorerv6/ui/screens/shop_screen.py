# ui/screens/shop_screen.py

# Goals:
#   - Allow the player to buy and sell items with an NPC merchant.
#   - Display the merchant's inventory and the player's inventory.
#   - Handle transactions (deducting gold, adding/removing items).
#   - Access the Game instance through the ScreenManager to get necessary data.

# Interactions:
#   - app.py: Added to ScreenManager.
#   - game.py:  Gets the merchant's inventory and the player's inventory/gold via App.game_instance.
#   - npcs.json:  Gets the merchant's inventory data (which items they sell).
#   - items.json:  Gets item data (name, description, value).
#   - inventory.py:  Adds and removes items from inventories.
#   - player.py: Accesses and modifies the player's gold.
#   - ui/widgets/: Might use custom widgets.
#   - kivy: Uses kivy for UI
#   - utils.py: Uses load_json_data

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.app import App  # Import App
from utils import load_json_data

class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal')

        # --- Merchant Inventory ---
        self.merchant_layout = BoxLayout(orientation='vertical')
        merchant_label = Label(text="Merchant Inventory", size_hint_y=None, height=40)
        self.merchant_layout.add_widget(merchant_label)
        self.merchant_scrollview = ScrollView()
        self.merchant_inventory = GridLayout(cols=1, size_hint_y=None)
        self.merchant_inventory.bind(minimum_height=self.merchant_inventory.setter('height'))
        self.merchant_scrollview.add_widget(self.merchant_inventory)
        self.merchant_layout.add_widget(self.merchant_scrollview)
        self.layout.add_widget(self.merchant_layout)

        # --- Player Inventory ---
        self.player_layout = BoxLayout(orientation='vertical')
        player_label = Label(text="Player Inventory", size_hint_y=None, height=40)
        self.player_layout.add_widget(player_label)
        self.player_scrollview = ScrollView()
        self.player_inventory = GridLayout(cols=1, size_hint_y=None)
        self.player_inventory.bind(minimum_height=self.player_inventory.setter('height'))
        self.player_scrollview.add_widget(self.player_inventory)
        self.player_layout.add_widget(self.player_scrollview)
        self.layout.add_widget(self.player_layout)

        # --- Gold Display ---
        self.gold_layout = BoxLayout(orientation = 'vertical', size_hint_y = None, height = 40)
        self.player_gold_label = Label(text="Your Gold: 0")
        self.merchant_gold_label = Label(text="Merchant Gold: 0") #optional
        self.gold_layout.add_widget(self.player_gold_label)
        self.gold_layout.add_widget(self.merchant_gold_label)
        self.layout.add_widget(self.gold_layout)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.merchant = None
        self.items_data = {}
        self.game = None # Initialize self.game


    def on_enter(self):
        # Get the Game instance from the App
        self.game = App.get_running_app().game_instance # Correct way
        # Get the interacting NPC (you'll need a mechanism for this in game.py)
        # Example: self.merchant = self.game.interacting_npc
        #For showcase purposes using the blacksmith
        self.merchant = "blacksmith_town"
        self.load_item_data()
        self.refresh_inventories()

    def update(self, dt):
        if self.game and self.game.player:
          self.player_gold_label.text = f"Your Gold: {self.game.player.gold}"
        #self.merchant_gold_label.text = f'Merchant Gold: {self.merchant.gold}' #If tracking merchant gold

    def load_item_data(self):
      self.items_data, self.msg = load_json_data("data/items.json")
      if self.items_data:
        self.items_data = self.items_data['items']
      else:
        print(self.msg)
        #handle however

    def refresh_inventories(self):
        self.merchant_inventory.clear_widgets()
        self.player_inventory.clear_widgets()

        if self.merchant and self.items_data and self.game and self.game.world: #check for game and world
            # Display merchant's inventory
            npc_data = self.game.world.map_data['npcs'].get(self.merchant) #get npc from world
            if not npc_data:
              print(f'Error: NPC data not found for {self.merchant}')
              self.go_back()
              return

            for item_id in npc_data["inventory"]:
              if item_id in self.items_data:
                item_data = self.items_data[item_id]
                button_text = f"{item_data['name']} ({item_data['value']} gold)"
                buy_button = Button(text=button_text, size_hint_y=None, height=40)
                buy_button.bind(on_press=lambda instance, item=item_id: self.buy_item(item))
                self.merchant_inventory.add_widget(buy_button)
              else:
                print(f'Error item id not found: {item_id}')

        if self.game and self.game.player:
            # Display player's inventory
            for item in self.game.player.inventory.get_items():
                button_text = f"{item['name']} ({item['value']} gold)"
                sell_button = Button(text=button_text, size_hint_y=None, height=40)
                sell_button.bind(on_press=lambda instance, item=item: self.sell_item(item))
                self.player_inventory.add_widget(sell_button)

    def buy_item(self, item_id):
        # Handle buying an item from the merchant.
        if self.game and self.game.player and item_id in self.items_data:
            item_data = self.items_data[item_id]
            if self.game.player.gold >= item_data["value"]:
                self.game.player.add_gold(-item_data["value"])
                self.game.player.add_to_inventory(item_data.copy())  # Add a *copy* of the item data
                self.refresh_inventories()
                print(f'Bought: {item_data["name"]}') #Debug
            else:
                print("Not enough gold!") # Or handle with a message

    def sell_item(self, item_data):
        # Handle selling an item to the merchant.
        if self.game and self.game.player:
          self.game.player.add_gold(item_data["value"])
          self.game.player.remove_from_inventory(item_data)
          self.refresh_inventories()
          print(f'Sold {item_data["name"]}') #debug

    def go_back(self, instance):
        self.manager.current = "game"