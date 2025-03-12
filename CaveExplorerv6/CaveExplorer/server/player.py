from server.entity import ServerEntity

class ServerPlayer(ServerEntity):
  def __init__(self, player_data):
     super().__init__(player_data)
     #Server specific player data.
