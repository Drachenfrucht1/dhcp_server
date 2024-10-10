from ackbuilder import AckBuilder
from offerbuilder import OfferBuilder
from server import DHCPServer

class DefaultDHCPServer():
    _server: DHCPServer
    leases = dict()
    def __init__(self, ip='192.168.2.1'):
        self._server = DHCPServer(self.discoveryHandler, self.requestHandler, self.declineHandler, self.releaseHandler, ip)

    def start(self):
        self._server.run()

    def discoveryHandler(self, offerbuilder: OfferBuilder, msg):
        return offerbuilder.ip('192.168.2.51').subnet('255.255.255.0').router('192.168.2.50').build()

    def requestHandler(self, ackbuilder: AckBuilder, msg):
        pass

    def declineHandler(self, msg):
        del self.leases[msg['mac']]

    def releaseHandler(self, msg):
        del self.leases[msg['mac']]

if __name__ == '__main__':
    dhcp_server = DefaultDHCPServer(ip='192.168.2.50')
    dhcp_server.start()