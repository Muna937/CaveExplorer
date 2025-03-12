from server.entity import ServerEntity

class ServerGame:
  def __init__(self, server):
    self.entities = {}
    self.server = server

  def update(self, delta_time):
    for entity_id in list(self.entities.keys()):
        entity = self.entities[entity_id]
        entity.update(delta_time)
            # Example of removing an entity.
        if not entity.is_alive:
            del self.entities[entity_id]
            print(f'Removed entity {entity_id}')
            #TODO: broadcast entity removal to players

  def add_entity(self, entity_data):
    entity_id = entity_data['id']
    if entity_id not in self.entities:
      self.entities[entity_id] = ServerEntity(entity_data)
      print(f'Added entity {entity_id}')

  def update_entity(self, entity_data):
    entity_id = entity_data['id']
    if entity_id in self.entities:
       self.entities[entity_id].update_data(entity_data)
    else:
       self.add_entity(entity_data)

  def move_player(self, player_id, x, y):
    if player_id in self.entities:
       self.entities[player_id].x = x
       self.entities[player_id].y = y
       print(f'Player {player_id} moved to ({x}, {y})')
       self.server.broadcast({'action':'updateEntity', 'id':player_id, 'x':x, 'y':y})
