import sys
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from loguru import logger

class GameClient(DatagramProtocol):
    def startProtocol(self):
        # Send a 'ready' message to the server
        self.transport.write(b'ready', ('127.0.0.1', 7777))

    def datagramReceived(self, data, addr):
        logger.info(f"Received packet from {addr}: {data}")

if __name__ == "__main__":
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.info(f"Starting client on 127.0.0.1:49413")

    game_client = GameClient()
    reactor.listenUDP(49413, game_client)
    reactor.run()
