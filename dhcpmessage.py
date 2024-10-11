import socket

from dhcpoptions import DHCPOption

class DHCPMessage:
    server_ip: bytes
    ip: bytes
    mac: bytes
    xid: bytes
    options: dict

    def __init__(self, server_ip=bytes(0), mac=bytes(0), xid=bytes(0), options=dict()):
        self.mac = mac
        self.xid = xid
        self.options = options
        if isinstance(server_ip, str):
            self.server_ip = socket.inet_aton(server_ip)
        else:
            self.server_ip = server_ip

    def build(self):
        if self.server_ip is None or len(self.server_ip) != 4:
            raise Exception()
        if self.ip is None or len(self.ip) != 4:
            raise Exception()
        if self.mac is None or len(self.mac) != 16:
            raise Exception()
        if self.xid is None or len(self.xid) != 4:
            raise Exception() 
        if self.options is None or DHCPOption.MESSAGE_TYPE not in self.options:
            raise Exception()

        optionbytes = bytes([0x63, 0x82, 0x53, 0x63])
        optionbytes += bytes([DHCPOption.MESSAGE_TYPE , 1 , self.options[DHCPOption.MESSAGE_TYPE]])
        if DHCPOption.SUBNET in self.options:
            optionbytes += bytes([DHCPOption.SUBNET, 4]) + self.options[DHCPOption.SUBNET]  
        
        for opt, value in self.options.items():
            if opt == DHCPOption.SUBNET or opt == DHCPOption.MESSAGE_TYPE:
                continue
            if isinstance(value, list):
                v = bytes()
                i = 0
                for a in value:
                    i += len(a)
                    v += a
                optionbytes += bytes([opt, i]) + v
            else:
                optionbytes += bytes([opt, len(value)]) + value

        OP = bytes([0x02])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        OFFSET = bytes(192)

        return OP + HTYPE + HLEN + HOPS + self.xid + SECS + FLAGS + CIADDR + self.ip + self.server_ip + GIADDR + self.mac + OFFSET + optionbytes + bytes(DHCPOption.END)

    def setIP(self, ip: (bytes | str)):
        if isinstance(ip, str):
            self.ip = socket.inet_aton(ip)
        else:
            self.ip = ip
        return self

    def setOption(self, opt, value: (bytes | int)):
        return self

    def setIPOption(self, opt, value: str):
        return self

    def setStringOption(self, opt, value: str):
        return self

class Acknowledgement(DHCPMessage):

    def __init__(self, server_ip: bytes, transaction_id: bytes, mac: bytes):
        super().__init__(server_ip,  mac, transaction_id)

    def ack(self):
        self.setOption(DHCPOption.MESSAGE_TYPE, 5)

    def nack(self):
        self.setOption(DHCPOption.MESSAGE_TYPE, 6)

class Offer(DHCPMessage):

    def __init__(self, server_ip: bytes, transaction_id: bytes, mac: bytes):
        super().__init__(server_ip,  mac, transaction_id)

        self.setOption(DHCPOption.MESSAGE_TYPE, 2)
        self.setOption(DHCPOption.DHCP_SERVER, server_ip)