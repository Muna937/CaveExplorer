class ServerEntity:
 def __init__(self, entity_data):
   self.id = entity_data.get('id')
   self.x = entity_data.get('x', 0)
   self.y = entity_data.get('y', 0)
   self.is_alive = True

 def update(self, delta_time):
   #Server side updates.
   pass
 def update_data(self, entity_data):
   self.x = entity_data.get('x', self.x)
   self.y = entity_data.get('y', self.y)
