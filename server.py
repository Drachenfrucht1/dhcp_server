import socket
from typing import Callable

from dhcpmessage import Acknowledgement, Offer
from dhcpoptions import DHCPOption

MAX_BYTES = 1024

serverPort = 67
clientPort = 68

class DHCPServer():
    _ip = bytes(4)
    _discoveryHandler: Callable[[Offer, dict], (None | Offer)]
    _requestHandler: Callable[[Acknowledgement, dict], (None | Acknowledgement)]
    _declineHandler: Callable[[dict], None]
    _releaseHandler: Callable[[dict], None]

    def __init__(self, discoveryHandler, requestHandler, declineHandler, releaseHandler, ip: str):
        self._ip = socket.inet_aton(ip)
        self._discoveryHandler = discoveryHandler
        self._requestHandler = requestHandler
        self._declineHandler = declineHandler
        self._releaseHandler = releaseHandler

    def parseMessage(self, data: bytes) -> dict:
        msg = dict()
        msg['xid'] = data[4:8]
        msg['mac'] = data[28:44]
        msg['type'] = data[242]
        options = dict()
        i = 242
        while i < len(data)-1:
            if data[i] == DHCPOption.END:
                break
            elif data[i] == 0:
                i = i+1
            elif data[i] == DHCPOption.REQUESTED_IP:
                options[50] = data[(i+2):(i+6)]
                i = i+6
            elif data[i] == DHCPOption.LEASE_TIME:
                options[51] = int.from_bytes(data[(i+2):(i+6)], signed=False)
                i = i+6
            elif data[i] == DHCPOption.REQUESTED_OPTIONS:
                options[55] = [int.from_bytes(data[(i+2+(n*2)):(i+4+(n*2))]) for n in range(0, data[i+1])]
                i = i+2+data[i+1]
            else:
                # skip this options, not implemented
                i = i+2+data[i+1]
            
        msg['options'] = options
        return msg

    def run(self) -> None:
        print("DHCP server is starting...\n", flush=True)
        
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        s.bind(('', serverPort))
        dest = ('255.255.255.255', clientPort)

        while 1:
            try:
                data, address = s.recvfrom(MAX_BYTES)

                if (len(data) < 243 
                    # no magic cookie
                    or data[236:240] != bytes([0x63, 0x82, 0x53, 0x63]) 
                    # no msg type option
                    or data[240] != 53 
                    or data[241] != 1
                    # not ethernet as type
                    or data[1] != 1
                    or data[2] != 6):
                    continue
                    
                msg = self.parseMessage(data)
                if msg['type'] == 1:
                    data = self._discoveryHandler(Offer(self._ip, msg['xid'], msg['mac']), msg)
                    if data is not None:
                        s.sendto(data.build(), dest)

                if msg['type'] == 3:
                    data = self._requestHandler(Acknowledgement(self._ip, msg['xid'], msg['mac']), msg)
                    if data is not None:
                        s.sendto(data.build(), dest)

                if msg['type'] == 4:
                    self._declineHandler(msg)

                if msg['type'] == 7:
                    self._releaseHandler(msg)
            except:
                raise