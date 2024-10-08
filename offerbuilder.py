import DHCPConfig from './dhcpconfig.py'

class OfferBuilder():
    ctx: DHCPConfig
    _IP = bytes(4)
    _options = bytes(0)
    _time_servers = []
    _router = []
    _dns_servers =[]
    _transaction_id

    def __init__(self, context: DHCPServer, transaction_id):
        ctx = context
        _options = bytes([0x63, 0x82, 0x53, 0x63]) #magic cookie
        _options += bytes([53 , 1 , 2]) # DHCP offer
        _transaction_id = transaction_id

    def build(self) -> bytes:
        if len(self._time_servers) > 0:
            self._options += bytes([4, 4*len(self._time_servers)])
            for s in self._time_servers:
                self._options += s

        if len(self._dns_servers) > 0:
            self._options += bytes([6, 4*len(self._dns_servers)])
            for s in self._dns_servers:
                self._options += s

        if len(self._router) > 0:
            self._options += bytes([3, 4*len(self._router)])
            for s in self._router:
                self._options += s

        OP = bytes([0x02])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00])
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)

        return OP + HTYPE + HLEN + HOPS + self._transaction_id + SECS + FLAGS + CIADDR + self._IP + self.ctx.__ip + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + self._options

    def ip(self, ip: str):
        self._IP = socket.inet_aton(ip)
        return self

    def subnet(self, subnet: str):
        self._options += bytes([1, 4]) + socket.inet_aton(subnet)
        return self

    def lease_time(self, lease_time: int):
        self._options += bytes([51, 4]) + lease_time.to_bytes(4, byteorder='big')
        return self

    def domain_name(self, domain_name: str):
        self._options += bytes([15, len(domain_name)]) + str.encode(domain_name)
        return self

    def dhcp_server(self, dhcp_server: str):
        self._options += bytes([54, 4]) + socket.inet_aton(dhcp_server)
        return self

    def time_server(self, time_server: str):
        self._time_servers.append(socket.inet_aton(time_server))
        return self

    def dns_server(self, dns_server: str):
        self._dns_servers.append(socket.inet_aton(dns_server))
        return self

    def router(self, router: str):
        self._router.append(socket.inet_aton(router))
        return self
