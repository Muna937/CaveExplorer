class Entity:
    def __init__(self, entity_data):
      self.id = entity_data.get('id')
      self.x = entity_data.get('x', 0)
      self.y = entity_data.get('y', 0)
      self.is_alive = True # Example. Could come from server.

    def update(self, delta_time):
      #Client side prediction here.
      pass
    def update_data(self, entity_data):
      # Update the entity's data with new data from the server.
      self.x = entity_data.get('x', self.x)
      self.y = entity_data.get('y', self.y)
