# ui/screens/skill_tree_screen.py

# Goals:
#   - Display a skill tree (if your game uses one).
#   - Allow the player to spend skill points to unlock skills.
#   - Show skill dependencies (which skills need to be unlocked before others).
#   - Provide a visually clear representation of the skill tree.

# Interactions:
#   - app.py: Added to the ScreenManager.
#   - game.py: Gets the player's skill data and available skill points.
#   - player.py: Modifies the player's skills when a skill is unlocked.
#   - skills.json: Gets skill data (name, description, requirements, effects).
#   - ui/widgets/:  Likely requires *custom widgets* to represent skill nodes.
#   - kivy: Uses Kivy for UI.

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.clock import Clock
from utils import load_json_data

class SkillNodeWidget(Widget): # Custom Widget for skill nodes
    def __init__(self, skill_id, skill_data, player_skills, can_unlock, on_unlock, **kwargs):
      super().__init__(**kwargs)
      self.skill_id = skill_id
      self.skill_data = skill_data
      self.player_skills = player_skills
      self.can_unlock = can_unlock
      self.on_unlock_callback = on_unlock
      self.is_unlocked = skill_id in self.player_skills

      self.size_hint = (None, None)
      self.size = (100, 40)  # Adjust size as needed

      with self.canvas:
          # Change the color of the rectangle based on state.
          if self.is_unlocked:
            Color(0, 1, 0, 1)  # Green if unlocked
          elif self.can_unlock:
            Color(0,0,1,1)  #blue if can be unlocked
          else:
            Color(1, 0, 0, 1)  # Red if locked

          self.rect = Rectangle(pos=self.pos, size=self.size)

          # Add lines for dependencies (you'll need to adjust positioning)
          if "requires" in self.skill_data:
            for req_skill_id in self.skill_data["requires"]:
              pass #Will be linked to lines in SkillTreeScreen

      self.label = Label(text=self.skill_data["name"], color=(0, 0, 0, 1))  # Black text
      self.add_widget(self.label)
      self.bind(pos=self.update_rect, size=self.update_rect)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.label.pos = self.pos  # Adjust label position as needed

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.can_unlock:
            # Handle skill unlocking here (deduct skill points, add skill to player)
            print(f"Unlock Skill: {self.skill_data['name']}")
            # Call back to skill tree to handle logic.
            if self.on_unlock_callback:
              self.on_unlock_callback(self.skill_id)
            return True  # Consume the touch event
        return super().on_touch_down(touch)

class SkillTreeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # --- Skill Tree (Scatter for pan/zoom) ---
        self.scatter = Scatter(do_rotation=False, do_scale=True, do_translation=True, size_hint=(1,1))
        # Create a Widget to hold skill nodes (so we can draw lines)
        self.skill_tree_widget = Widget(size_hint=(None, None), size=(1000, 1000))  # Adjust size as needed
        self.scatter.add_widget(self.skill_tree_widget)
        self.layout.add_widget(self.scatter)


        # --- Back Button ---
        self.back_button = Button(text="Back to Game", size_hint=(1,None), height = 40)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.skills_data = {}
        self.player_skills = {}  # Store player's unlocked skills (e.g., a set of skill IDs)

    def on_enter(self):
        self.game = self.manager.parent.game_instance
        self.load_skill_data()
        self.load_player_skills()  # Load the player's currently unlocked skills
        self.create_skill_tree()

    def update(self, dt):
        pass

    def load_skill_data(self):
        # Load skill data from skills.json.
        skills_data, self.msg = load_json_data("data/skills.json")
        if skills_data:
          self.skills_data = skills_data['skills']
        else:
          print(self.msg)
          #Handle error

    def load_player_skills(self):
        # Load the player's unlocked skills (from the Player object or save data).
        # Example:
      if self.game and self.game.player:
        self.player_skills = set(self.game.player.skills.keys()) # Use a set for efficient checking.
      else:
        print("No player") #handle error

    def create_skill_tree(self):
      self.skill_tree_widget.clear_widgets()
      self.skill_tree_widget.canvas.clear()
      #Position and create skill nodes.  This is a *simplified* example.
      #You'll need a more sophisticated layout algorithm for a real skill tree.
      x, y = 100, 500

      #Create nodes:
      nodes = {}
      for skill_id, skill_data in self.skills_data.items():
        can_unlock = self.can_unlock_skill(skill_id)
        node = SkillNodeWidget(skill_id, skill_data, self.player_skills, can_unlock, self.unlock_skill, pos=(x,y))
        self.skill_tree_widget.add_widget(node)
        nodes[skill_id] = node #store for linking
        x += 150
        if x > 800:
          x = 100
          y -= 100

      #Draw lines:
      with self.skill_tree_widget.canvas:
        Color(1,1,1,1) #white
        for skill_id, skill_data in self.skills_data.items():
          if "requires" in skill_data:
            for req_skill_id in skill_data["requires"]:
              if req_skill_id in nodes and skill_id in nodes:
                Line(points=(nodes[req_skill_id].center_x, nodes[req_skill_id].center_y,
                            nodes[skill_id].center_x, nodes[skill_id].center_y), width=2)

    def can_unlock_skill(self, skill_id):
        # Check if the player can unlock a skill (meets prerequisites).
        if skill_id in self.player_skills:
            return False  # Already unlocked

        skill_data = self.skills_data.get(skill_id)
        if not skill_data:
            return False  # Invalid skill ID

        if "requires" in skill_data:
            for req_skill_id in skill_data["requires"]:
                if req_skill_id not in self.player_skills:
                    return False  # A required skill is not unlocked

        # Check for other requirements (level, stats, etc.) as needed.
        # if self.game.player.level < skill_data.get("requirements", {}).get("level", 1):
        #    return False

        return True  # All prerequisites met

    def unlock_skill(self, skill_id):
      if self.can_unlock_skill(skill_id):
        #Unlock Skill
        skill_data = self.skills_data.get(skill_id)
        #TODO: deduct points
        self.game.player.add_skill(skill_id, Skill(skill_data['name'], skill_data['description'], skill_data['cost'], skill_data['effect'])) #add skill
        self.player_skills.add(skill_id) #update the set
        self.create_skill_tree() #refresh tree
        print(f'Unlocked skill {skill_id}')
      else:
        print("Cannot unlock") #display message


    def go_back(self, instance):
        self.manager.current = "game"