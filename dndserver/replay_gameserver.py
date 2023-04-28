from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer
import binascii
import yaml
from loguru import logger

class DungeonServer(DatagramProtocol):
    def __init__(self, yaml_file):
        self.clients = set()
        self.yaml_file = yaml_file
        self.replaying = False

    def start_replay(self):
        with open(self.yaml_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            packets = data['packets']
            peers = data['peers']
            self.replay_packets(packets, peers)

    def replay_packets(self, packets, peers):
        prev_ts = 0
        for packet in packets:
            curr_ts = packet['timestamp']
            delay = 0
            if prev_ts > 0:
                delay = curr_ts - prev_ts

            peer = peers[packet['peer']]
            address = (peer['host'], peer['port'])
            reactor.callLater(delay, self.send_packet, packet['data'], address)
            prev_ts = curr_ts

    def send_packet(self, data, address):
        try:
            logger.info(f"Sent packet to {address}: {data}")
            self.transport.write(data, address)
        except Exception as e:
            logger.error(f"Error sending packet data: {e}")

    def datagramReceived(self, data, address):
        if not self.replaying and data == b'ready':
            self.replaying = True
            self.start_replay()

if __name__ == "__main__":
    port = 7777
    yaml_file = 'replaydndfull.yml'
    logger.info(f"Starting server on port {port}")
    dungeon_server = DungeonServer(yaml_file)
    reactor.listenUDP(port, dungeon_server)
    reactor.run()
