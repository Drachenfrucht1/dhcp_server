import time

from dhcpoptions import DHCPOption
from server import DHCPServer
from dhcpmessage import Offer, Acknowledgement
from utils import ip_str_or_b_to_b

class DefaultDHCPServer():
    _ip: bytes
    _server: DHCPServer
    leases = dict()

    ip_range = True
    ips: list[bytes] = []
    subnet: bytes
    router: bytes
    leasetime: int

    def __init__(self, lease_ip_config: (dict | list[bytes | str]), server_ip: (bytes | str),  subnet: (bytes | str), router: (bytes | str), leasetime: int):
        self._ip = ip_str_or_b_to_b(server_ip)
        self.subnet = ip_str_or_b_to_b(subnet)
        self.router = ip_str_or_b_to_b(router)
        self.leasetime = leasetime

        if isinstance(lease_ip_config, dict):
            self.ip_range = True
            self.ips = [ip_str_or_b_to_b(lease_ip_config['start']), ip_str_or_b_to_b(lease_ip_config['end'])]
        else:
            self.ip_range = False
            self.ips = [ip_str_or_b_to_b(a) for a in lease_ip_config]

        self._server = DHCPServer(self.discoveryHandler, self.requestHandler, self.declineHandler, self.releaseHandler, self._ip)

    def start(self):
        self._server.run()

    def discoveryHandler(self, offer: Offer, msg) -> (None | Offer):
        if msg['mac'].hex() in self.leases:
            return

        ip = self.getFreeIp()
        if ip == bytes([255,255,255,255]): return None
        if DHCPOption.REQUESTED_IP in msg and True not in [a['ip'] == msg[DHCPOption.REQUESTED_IP] for a in self.leases.values()] == 0:
            ip = msg[DHCPOption.REQUESTED_IP]

        self.leases[msg['mac'].hex()] = {'ip': ip, 'time': time.time()}

        return (offer.setIP(ip)
                .setIPOption(DHCPOption.SUBNET, self.subnet)
                .setIPOption(DHCPOption.ROUTER, self.router)
                .setOption(DHCPOption.LEASE_TIME, self.leasetime))

    def requestHandler(self, ack: Acknowledgement, msg) -> (None | Acknowledgement):
        if DHCPOption.DHCP_SERVER in msg and msg[DHCPOption.DHCP_SERVER] != self._ip:
            del self.leases[msg['mac'].hex()]
            return
        
        self.leases[msg['mac'].hex()]['commited'] = True
        return (ack.setIP(self.leases[msg['mac'].hex()]['ip'])
                .setIPOption(DHCPOption.SUBNET, self.subnet)
                .setIPOption(DHCPOption.ROUTER, self.router)
                .setOption(DHCPOption.LEASE_TIME, self.leasetime))

    def declineHandler(self, msg):
        del self.leases[msg['mac'].hex()]

    def releaseHandler(self, msg):
        del self.leases[msg['mac'].hex()]

    def getFreeIp(self) -> bytes:
        leased_ips = [a['ip'] for a in self.leases.values()]
        if self.ip_range:
            for ip in range(int.from_bytes(self.ips[0], self.ips[1])):
                if int.to_bytes(ip, length=4) not in leased_ips:
                    return int.to_bytes(ip, length=4)
        else:
            for ip in self.ips:
                if ip not in leased_ips:
                    return ip
        return bytes([255,255,255,255])