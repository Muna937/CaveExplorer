# ai.py

# Goals:
#   - Implement AI behaviors for monsters and (potentially) NPCs.
#   - Provide different AI types (e.g., aggressive, passive, ranged).
#   - Control monster movement, target selection, and actions.
#   - Make the AI adaptable to different situations and environments.

# Interactions:
#   - monster.py:  Monster instances will use AI functions to determine their actions.
#   - game.py: The game loop will call the AI update functions.
#   - world.py:  The AI might need to access world data (e.g., for pathfinding, checking line of sight).
#   - player.py: The AI will often need to know the player's position.
#   - combat.py (potentially):  AI might be integrated with the combat system.

# --- Basic Utility Functions (Could be in utils.py, but here for now) ---

def distance(x1, y1, x2, y2):
    """Calculates the Euclidean distance between two points."""
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# --- AI Functions ---

def basic_melee_ai(monster, game):
    """Simple melee AI: Move towards the player and attack if in range."""
    if not game.player.is_alive: #don't do anything if player is dead.
      return

    player_x = game.player.x
    player_y = game.player.y
    dist = distance(monster.x, monster.y, player_x, player_y)

    if dist <= 1:  # Assuming 1 tile is melee range
        # Attack the player (you'd call a combat function here)
        print(f"{monster.name} attacks the player!") # Placeholder
        # game.start_combat()  # Or something similar
    elif dist <= 5:  # Move towards the player if within a certain range
        # Basic movement (replace with pathfinding for more complex AI)
        dx = 0
        dy = 0
        if player_x > monster.x:
            dx = 1
        elif player_x < monster.x:
            dx = -1
        if player_y > monster.y:
            dy = 1
        elif player_y < monster.y:
            dy = -1

        #Check for collisions before moving.
        if game.world.is_tile_walkable((monster.x + dx) * game.world.tile_size, (monster.y + dy) * game.world.tile_size):
          monster.move(dx, dy)
    else:
      #Idle or patrol
      pass

def ranged_fire_ai(monster, game):
    """Ranged AI: Stay at a distance and attack."""
    if not game.player.is_alive:
      return
    player_x = game.player.x
    player_y = game.player.y
    dist = distance(monster.x, monster.y, player_x, player_y)

    if 2 <= dist <= 5 :  # Example: Attack if within range 2-5
        # Attack the player (you'd call a combat function here)
        print(f"{monster.name} attacks the player from range!")  # Placeholder
        # game.start_combat()  # Or something similar, perhaps a ranged attack function
    elif dist < 2:
      #move away
      dx = 0
      dy = 0
      if player_x > monster.x:
          dx = -1
      elif player_x < monster.x:
          dx = 1
      if player_y > monster.y:
          dy = -1
      elif player_y < monster.y:
          dy = 1
       #Check for collisions before moving.
      if game.world.is_tile_walkable((monster.x + dx) * game.world.tile_size, (monster.y + dy) * game.world.tile_size):
        monster.move(dx, dy)
    elif dist > 5:
       #Move closer
        dx = 0
        dy = 0
        if player_x > monster.x:
            dx = 1
        elif player_x < monster.x:
            dx = -1
        if player_y > monster.y:
            dy = 1
        elif player_y < monster.y:
            dy = -1
         #Check for collisions before moving.
        if game.world.is_tile_walkable((monster.x + dx) * game.world.tile_size, (monster.y + dy) * game.world.tile_size):
          monster.move(dx, dy)
    else:
      #Idle
      pass

def update_ai(monster, game, dt):
  #Update the ai
  if monster.ai == "basic_melee":
    basic_melee_ai(monster, game)
  elif monster.ai == "ranged_fire":
    ranged_fire_ai(monster, game)
# --- Example Usage (in monster.py or game.py) ---
# In monster.py's Monster.update() method:
#    ai.update_ai(self, game, dt)

# --- Add more AI behaviors as needed ---