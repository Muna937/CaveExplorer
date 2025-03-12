# ui/screens/crafting_screen.py

# Goals:
#   - Allow the player to combine items to create new items (crafting).
#   - Display available crafting recipes.
#   - Show required ingredients and the resulting crafted item.
#   - Handle the crafting process (deducting ingredients, adding the crafted item).

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets crafting recipes and player inventory.
#   - items.json:  Gets item data (for recipes and crafted items).
#   - inventory.py:  Removes ingredients and adds crafted items.
#   - ui/widgets/: Might use custom widgets for displaying recipes and items.
#   - kivy: Uses kivy for UI

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from utils import load_json_data # Assuming you have this in utils.py

class CraftingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Recipe List (ScrollView) ---
        self.recipe_scrollview = ScrollView()
        self.recipe_list = GridLayout(cols=1, size_hint_y=None)
        self.recipe_list.bind(minimum_height=self.recipe_list.setter('height'))
        self.recipe_scrollview.add_widget(self.recipe_list)
        self.layout.add_widget(self.recipe_scrollview)

        # --- Crafting Details ---
        self.details_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        self.recipe_name_label = Label(text="Recipe Name")
        self.ingredients_label = Label(text="Ingredients: ")
        self.result_label = Label(text="Result: ")
        self.details_layout.add_widget(self.recipe_name_label)
        self.details_layout.add_widget(self.ingredients_label)
        self.details_layout.add_widget(self.result_label)
        self.layout.add_widget(self.details_layout)


        # --- Craft Button ---
        self.craft_button = Button(text="Craft", size_hint_y=None, height=40, disabled = True)
        self.craft_button.bind(on_press=self.craft_item)
        self.layout.add_widget(self.craft_button)

        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint_y=None, height=40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.selected_recipe = None
        self.recipes = {}  # Store loaded recipes


    def on_enter(self):
        self.game = self.manager.parent.game_instance
        self.load_recipes()
        self.refresh_recipes()

    def update(self, dt):
        pass


    def load_recipes(self):
        # Load crafting recipes from a JSON file (you'll need to create this file).
        # Example: data/crafting_recipes.json
        recipes_data, self.msg = load_json_data("data/crafting_recipes.json")
        if recipes_data:
          self.recipes = recipes_data['recipes']
        else:
          print(self.msg) #handle however

    def refresh_recipes(self):
        self.recipe_list.clear_widgets()
        self.selected_recipe = None
        self.update_recipe_details()
        self.craft_button.disabled = True

        # Display available recipes.
        if self.recipes:
          for recipe_id, recipe_data in self.recipes.items():
              recipe_button = Button(text=recipe_data["result"]["name"], size_hint_y=None, height=40)
              recipe_button.bind(on_press=lambda instance, r_id=recipe_id: self.select_recipe(r_id))
              self.recipe_list.add_widget(recipe_button)
        else:
          self.recipe_list.add_widget(Label(text="No Recipes Available"))

    def select_recipe(self, recipe_id):
        # Handle recipe selection.
        if recipe_id in self.recipes:
            self.selected_recipe = recipe_id
            self.update_recipe_details()

    def update_recipe_details(self):
        # Display details of the selected recipe.
        if self.selected_recipe and self.selected_recipe in self.recipes:
            recipe_data = self.recipes[self.selected_recipe]
            self.recipe_name_label.text = f'{recipe_data["result"]["name"]}'

            ingredients_text = "Ingredients: "
            for ingredient, amount in recipe_data["ingredients"].items():
                ingredients_text += f"{ingredient} x{amount}, " #TODO make names not ID
            ingredients_text = ingredients_text[:-2]  # Remove trailing ", "
            self.ingredients_label.text = ingredients_text

            self.result_label.text = f'Result: 1 x {recipe_data["result"]["item_id"]}' #TODO make names not ID
            self.craft_button.disabled = False
        else:
            self.recipe_name_label.text = "Recipe Name"
            self.ingredients_label.text = "Ingredients: "
            self.result_label.text = "Result: "

    def craft_item(self, instance):
      if self.selected_recipe and self.selected_recipe in self.recipes:
        recipe_data = self.recipes[self.selected_recipe]
        # Check if the player has the required ingredients.
        can_craft = True
        if self.game and self.game.player:
          for ingredient, required_amount in recipe_data["ingredients"].items():
              if not self.game.player.inventory.has_item(ingredient):
                can_craft = False
                break;
              #check amount
              item = self.game.player.inventory.get_item(ingredient)
              if item.get("quantity", 0) < required_amount:
                can_craft = False
                break;

          if can_craft:
              # Remove ingredients
              for ingredient, required_amount in recipe_data["ingredients"].items():
                  for _ in range(required_amount):
                    item = self.game.player.inventory.get_item(ingredient) #get the item object
                    self.game.player.inventory.remove_item(item)  #remove one at a time

              # Add crafted item
              crafted_item_data = items_data.get(recipe_data["result"]["item_id"])
              if crafted_item_data:
                self.game.player.inventory.add_item(crafted_item_data.copy())  # Add a *copy* of the item data
                print(f"Crafted: {crafted_item_data['name']}")
                self.refresh_recipes() # Refresh the recipe list (in case recipes have requirements)
              else:
                print(f'Could not find item data {recipe_data["result"]["item_id"]}')
          else:
              print("Not enough ingredients!")  # Or display a message to the player.
      else:
        print("No recipe selected")


    def go_back(self, instance):
        self.manager.current = "game"