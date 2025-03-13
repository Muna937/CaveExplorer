# quests.py

# Goals:
#   - Define Quest and Objective classes to represent quests and their objectives.
#   - Load quest data from a JSON file (quests.json).
#   - Track quest progress (active, completed, objective status).
#   - Check for quest and objective completion.
#   - Handle quest rewards (giving items, gold, experience to the player).
#   - Provide methods to start and complete quests.

# Interactions:
#   - game.py:
#       - Loads quest data during initialization.
#       - Calls update() on active quests in the game loop.
#       - Calls start_quest() and complete_quest() based on game events (dialogue, etc.).
#       - Accesses player.inventory and player attributes to check objectives and give rewards.
#       - Maintains a dictionary of all quests, keyed by quest ID.
#   - player.py:  (Indirectly, via game.py) Rewards are given to the player.
#   - ui/screens/quest_log_screen.py:  Displays quest information (name, description, objectives, progress).
#   - inventory.py: Used to check for collected items (for "collect" objectives).
#   - data/quests.json:  Contains the quest definitions (loaded by load_quests()).
#   - utils.py: Uses load_json_data to load the quest data.
#   - dialogue_screen.py: Dialogue choices can trigger quest actions via game.handle_dialogue_action().
#   - save_load.py:  Needs to save and load the status of all quests (active, completed, objective progress).

#quests.py
import json
from utils import load_json_data #import load json data
class Quest:
    def __init__(self, quest_id, name, description, objectives, rewards):
        self.quest_id = quest_id #Added ID
        self.name = name
        self.description = description
        self.objectives = objectives  # List of Objective objects (see below).
        self.rewards = rewards  # Dictionary of rewards.
        self.is_complete = False
        self.is_active = False

    def check_completion(self):
        #Relevant to dialogue if quest completion is a dialogue condition.
        for objective in self.objectives:
            if not objective.is_complete:
                return False
        self.is_complete = True
        return True

    def complete_quest(self, game): # Added game parameter
        if self.is_complete:
            print(f"Quest '{self.name}' completed!")
            #Removed reward logic

    def start_quest(self):
        self.is_active = True
        print(f'Quest: "{self.name}" started!')

    def update(self, game):
        #Indirectly relevant, as dialogue may trigger quest updates
        if self.is_active:
            for objective in self.objectives:
                objective.update(game)
            self.check_completion()


class Objective:
    def __init__(self, type, target, amount):
        self.type = type
        self.target = target
        self.amount = amount
        self.current_amount = 0
        self.is_complete = False

    def update(self, game):
        #Indirectly related as this updates quest status
        if self.type == "kill":
            self.current_amount = game.get_kill_count(self.target)

        elif self.type == "collect":
            self.current_amount = game.player.inventory.count_item(self.target)

        elif self.type == "reach":
            if game.player.x == self.target[0] and game.player.y == self.target[1]:
                self.current_amount = self.amount

        if self.current_amount >= self.amount:
            self.is_complete = True

def load_quests(filepath, items_data):
    #Relevant as dialogue triggers quest start/completion.
    quests_data, error_msg = load_json_data(filepath)
    if error_msg:
        print(error_msg)
        return {}

    quests = {}
    for quest_id, quest_data in quests_data.get("quests", {}).items():
        objectives_data = quest_data.get("objectives", [])
        objectives = []
        for obj_data in objectives_data:
            objective = Objective(
                type=obj_data["type"],
                target=obj_data["target"],
                amount=obj_data["amount"],
            )
            objectives.append(objective)

        rewards_data = quest_data.get("rewards", {})
        # Ensure "items" is a dictionary where keys are item IDs and values are quantities.
        rewards = {
            "gold": rewards_data.get("gold", 0),
            "experience": rewards_data.get("experience", 0),
            "items": rewards_data.get("items", {})  # Ensure this is a dictionary
        }


        quest = Quest(
            quest_id = quest_id, #pass in ID
            name=quest_data["name"],
            description=quest_data["description"],
            objectives=objectives,
            rewards=rewards,
        )
        quests[quest_id] = quest

    return quests