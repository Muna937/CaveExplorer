from server.network import GameServer
from server.config import SERVER_HOST, SERVER_PORT
import argparse

class GameServerApp:
    def __init__(self):
        self.parse_arguments()
        self.server = GameServer(localaddr=(self.host, self.port))

    def run(self):
        print(f'Starting server on {self.host}:{self.port}')
        self.server.launch()
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Run the RPG game server.')
        parser.add_argument('--host', type=str, default=SERVER_HOST,
                            help='The hostname to run the server on.')
        parser.add_argument('--port', type=int, default=SERVER_PORT,
                            help='The port to run the server on.')
        args = parser.parse_args()
        self.host = args.host
        self.port = args.port
