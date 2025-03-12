from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from shared.constants import *
from time import sleep, time
from server.game import ServerGame

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None  # Player ID will be assigned by the server

    def Network_move(self, data):
        #data = {'action': 'move', 'x': event.x, 'y': event.y, 'id': self.id}
        if self.id is not None:
            self._server.game.move_player(self.id, data['x'], data['y'])

    def Network_heartbeat(self, data):
      #Client sent a heartbeat.  We don't really need to *do* anything,
      #but we should reset the timeout.
      pass
    def Network_heartbeat_ack(self, data):
      #Client responded to our heartbeat
      pass
    def Close(self):
        print(f'Client {self.id} disconnected')
        if self.id is not None:
          self._server.remove_player(self.id) #tell the server to remove the player

class GameServer(Server):
    channelClass = ClientChannel
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = ServerGame(self)  # Pass the server instance to the game
        self.players = {}  # Dictionary to store connected players {player_id: channel}
        self.next_player_id = 0
        self.last_heartbeat_check = time()

    def Connected(self, channel, addr):
        print(f'New connection: {addr}')
        player_id = self.next_player_id
        self.next_player_id += 1
        channel.id = player_id
        self.players[player_id] = channel
        #Send confirmation of connection to the client
        channel.Send({'action': MSG_PLAYER_JOINED, 'id': player_id})
        #Add an entity for this player
        self.game.add_entity({'id':player_id, 'x':0, 'y':0})
        #TODO: Send existing entities to the new player

    def remove_player(self, player_id):
      if player_id in self.players:
        del self.players[player_id]
      #TODO: broadcast to other players that a player has left.

    def broadcast(self, data):
      for player_id in self.players:
        self.players[player_id].Send(data)

    def check_heartbeats(self):
      #Send heartbeats to all clients, check for timeouts.
      for player_id, channel in list(self.players.items()): #list() to avoid dict size change
        if channel: # Check if the channel is still valid.
            channel.Send({'action': MSG_HEARTBEAT})
            #In a real implementation, check for response timeout here!
        else:
          print(f'Removing inactive player {player_id}')
          self.remove_player(player_id)

    def launch(self):
        while True:
            self.Pump()  # Handles all incoming and outgoing networking events.
            self.game.update(0.01) # Update game state. Pass delta time if needed.
            # Check heartbeats every second
            if time() - self.last_heartbeat_check > 1.0:
                self.check_heartbeats()
                self.last_heartbeat_check = time()
            sleep(0.01)  # Server tick rate
