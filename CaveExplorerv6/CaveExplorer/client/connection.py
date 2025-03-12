from client.network import GameClient

class ClientConnection:
 def __init__(self, game_app):
   self.game_app = game_app
   self.client = None #the GameClient instance

 def connect(self, host, port):
   if self.client is None or not self.client.isConnected:
     self.client = GameClient(host, int(port), self.game_app)
     return True, '' #success
   else:
     return False, 'Already connected to the server.'

 def check_connection_loop(self):
     if self.client is not None:
       self.client.update()
