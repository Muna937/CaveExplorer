from PodSixNet.Connection import ConnectionListener, connection
from shared.constants import *
from time import sleep, time

class GameClient(ConnectionListener):
    def __init__(self, host, port, game_client_app):
        self.Connect((host, port))
        self.player_id = None
        self.game = None  # We'll set this later, after Game is initialized
        self.game_client_app = game_client_app
        self.last_heartbeat_sent = 0

    def Network_connected(self, data):
        print('Connected to server')

    def Network_error(self, data):
        print('Error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Disconnected from server')
        connection.Close()
        self.game_client_app.stop()

    def Network_playerJoined(self, data):
        self.player_id = data['id']
        print(f'My player ID: {self.player_id}')

    def Network_updateEntity(self, data):
        if self.game:
            self.game.update_entity(data)

    def Network_heartbeat(self, data):
        # Respond to server heartbeats immediately
        connection.Send({'action': MSG_HEARTBEAT_ACK})

    def send_move(self, x, y):
        connection.Send({'action': MSG_MOVE, 'x': x, 'y': y, 'id': self.player_id})

    def update(self):
        connection.Pump()
        self.Pump()

        # Send heartbeats every second
        if time() - self.last_heartbeat_sent > 1.0:
            connection.Send({'action': MSG_HEARTBEAT})
            self.last_heartbeat_sent = time()

    def close_connection(self):
        connection.Close()
