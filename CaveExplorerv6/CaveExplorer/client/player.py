from client.entity import Entity

class ClientPlayer(Entity):
 def __init__(self, player_data):
   super().__init__(player_data)
   #Client specific attributes
