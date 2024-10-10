import socket

class AckBuilder():
    _server_ip: bytes
    _ip: bytes
    _options: bytes
    _time_servers = []
    _router = []
    _dns_servers =[]
    _transaction_id: bytes
    _mac: bytes
    _ack: bool = True

    def __init__(self, server_ip: bytes, transaction_id: bytes, mac: bytes):
        self._server_ip = server_ip
        self._options = bytes([0x63, 0x82, 0x53, 0x63]) #magic cookie
        self._transaction_id = transaction_id
        self._mac = mac

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


        if self._ack:
            self._options += bytes([53 , 1 , 5]) # DHCP ack
        else:
            self._options += bytes([53 , 1 , 6]) # DHCP nack

        OP = bytes([0x02])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        OFFSET = bytes(192)

        return OP + HTYPE + HLEN + HOPS + self._transaction_id + SECS + FLAGS + CIADDR + self._ip + self._server_ip + GIADDR + self._mac + OFFSET + self._options + bytes(0xff)

    def ack(self):
        self._ack = True

    def nack(self):
        self._ack = False

    def ip(self, ip: str):
        self._ip = socket.inet_aton(ip)
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
