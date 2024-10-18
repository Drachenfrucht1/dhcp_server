import socket

from dhcpoptions import DHCPOption
from server import DHCPServer
from dhcpmessage import Offer, Acknowledgement

class DefaultDHCPServer():
    _ip: bytes
    _server: DHCPServer
    leases = dict()

    ip_range = True
    ips: list[bytes]
    subnet: bytes
    router: bytes
    leasetime: int

    def __init__(self, server_ip='192.168.2.1',  subnet='255.255.255.0', router='192.168.2.1', leastime=1296000):
        self._ip = socket.inet_aton(server_ip)
        self._server = DHCPServer(self.discoveryHandler, self.requestHandler, self.declineHandler, self.releaseHandler, server_ip)

    def start(self):
        self._server.run()

    def discoveryHandler(self, offer: Offer, msg) -> (None | Offer):
        if msg['mac'].hex() in self.leases:
            return

        ip = self.getFreeIp()
        if DHCPOption.REQUESTED_IP in msg and True not in [a['ip'] == msg[DHCPOption.REQUESTED_IP] for a in self.leases.values()] == 0:
            ip = msg[DHCPOption.REQUESTED_IP]

        return (offer.setIP(ip)
                .setIPOption(DHCPOption.SUBNET, '255.255.255.0')
                .setIPOption(DHCPOption.ROUTER, '192.168.2.50'))

    def requestHandler(self, ack: Acknowledgement, msg) -> (None | Acknowledgement):
        if DHCPOption.DHCP_SERVER in msg and msg[DHCPOption.DHCP_SERVER] != self._ip:
            del self.leases[msg['mac'].hex()]
            return

        self.leases[msg['mac'].hex()]['commited'] = True

    def declineHandler(self, msg):
        del self.leases[msg['mac'].hex()]

    def releaseHandler(self, msg):
        del self.leases[msg['mac'].hex()]

    def getFreeIp(self) -> bytes:
        pass

if __name__ == '__main__':
    dhcp_server = DefaultDHCPServer(ip='192.168.2.50')
    dhcp_server.start()