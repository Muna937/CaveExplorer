from client.entity import Entity
from client.world import ClientWorld

class ClientGame:
   def __init__(self, client):
        self.entities = {}
        self.client = client
        self.world = ClientWorld(self)
        self.local_player = None

   def update(self, delta_time):
     if self.local_player is not None:
       self.local_player.update(delta_time)
     self.world.update(delta_time)

     for entity_id in list(self.entities.keys()):
       entity = self.entities[entity_id]
       entity.update(delta_time)
       #Example of removing an entitiy
       if not entity.is_alive:
           del self.entities[entity_id]
           print(f'Removed entity {entity_id}')

   def add_entity(self, entity_data):
     #Should also check if the entity is the player entity and assign it to self.local_player
     entity_id = entity_data['id']
     if entity_id not in self.entities:
       self.entities[entity_id] = Entity(entity_data)
       print(f'Added entity {entity_id}')

   def update_entity(self, entity_data):
       entity_id = entity_data['id']
       if entity_id in self.entities:
           self.entities[entity_id].update_data(entity_data)
       else:
         self.add_entity(entity_data)
