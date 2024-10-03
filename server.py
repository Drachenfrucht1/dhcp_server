import socket
import json

MAX_BYTES = 1024

serverPort = 67
clientPort = 68

class DHCPServer():
    __ip = bytes(4)
    __counter = 1
    __discoveryHandler
    __requestHandler
    def __init__(self, ip: str, discoveryHandler, requestHandler):
        self.__ip = socket.inet_aton(ip)
        self.__discoveryHandler = discoveryHandler
        self.__requestHandler = requestHandler

    def run(self):
        print("DHCP server is starting...\n")
        
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        s.bind(('', serverPort))
        dest = ('255.255.255.255', clientPort)

        while 1:
            try:
                print("Wait DHCP discovery.")
                data, address = s.recvfrom(MAX_BYTES)
                print("Receive DHCP discovery.")

                discovery = dict()
                discovery['mac'] = data[16:32]
        
                print("Send DHCP offer.")
                data = self.__discoveryHandler()
                # data = self.__get_offer(data[4:8])
                s.sendto(data, dest)
                
                ####
                # Only for testing purposes
                # self.__counter += 1
                ####

                while 1:
                    try:
                        print("Wait DHCP request.")
                        data, address = s.recvfrom(MAX_BYTES)
                        print("Receive DHCP request.")

                        request = dict()
                        request['mac'] = data[16:32]

                        print("Send DHCP pack.\n")
                        data = self.__requestHandler(request)
                        data = self.__get_ack(data[4:8])
                        s.sendto(data, dest)

                        self.__counter += 1
                        break
                    except:
                        raise
            except:
                raise

    def __get_offer(self, transaction_id):
        f = open(str(self.__counter) + ".json")
        options = json.load(f)

        opt_string = bytes([0x63, 0x82, 0x53, 0x63]) #magic cookie
        opt_string += bytes([53 , 1 , 2]) # DHCP offer
        ip = bytes(4)

        for opt in options:
            # if opt["name"] == "dns-server":
            #     opt_string += bytes([6, 4*len(opt["value"])])
            #     for s in opt["value"]:
            #         opt_string += socket.inet_aton(s)
            # if opt["name"] == "router":
            #     opt_string += bytes([3, 4*len(opt["value"])])
            #     for s in opt["value"]:
            #         opt_string += socket.inet_aton(s)
            # if opt["name"] == "time-server":
            #     opt_string += bytes([4, 4*len(opt["value"])])
            #     for s in opt["value"]:
            #         opt_string += socket.inet_aton(s)
            # if opt["name"] == "dhcp-server":
            #     opt_string += bytes([54, 4]) + socket.inet_aton(opt["value"])
            # if opt["name"] == "domain-name":
            #     opt_string += bytes([15, len(opt["value"])]) + str.encode(opt["value"])
            # if opt["name"] == "subnet":
            #     opt_string += bytes([1, 4]) + socket.inet_aton(opt["value"])
            # if opt["name"] == "lease-time":
            #     opt_string += bytes([51, 4]) + opt["value"].to_bytes(4, byteorder='big')
            # if opt["name"] == "ip":
            #     ip = socket.inet_aton(opt["value"])

        f.close()

        opt_string += bytes([0xff])

        return self.__construct_offer(transaction_id, ip, opt_string)

    def __construct_offer(self, XID, ip, options):
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
        
        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + ip + self.__ip + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + options

        return package
	
    def __get_ack(self, transaction_id):
        f = open(str(self.__counter) + ".json")
        options = json.load(f)

        opt_string = bytes([0x63, 0x82, 0x53, 0x63]) #magic cookie
        opt_string += bytes([53 , 1 , 5]) # DHCP ACK
        ip = bytes(4)

        for opt in options:
            if opt["name"] == "dns-server":
                opt_string += bytes([6, 4*len(opt["value"])])
                for s in opt["value"]:
                    opt_string += socket.inet_aton(s)
            if opt["name"] == "router":
                opt_string += bytes([3, 4*len(opt["value"])])
                for s in opt["value"]:
                    opt_string += socket.inet_aton(s)
            if opt["name"] == "time-server":
                opt_string += bytes([4, 4*len(opt["value"])])
                for s in opt["value"]:
                    opt_string += socket.inet_aton(s)
            if opt["name"] == "dhcp-server":
                opt_string += bytes([54, 4]) + socket.inet_aton(opt["value"])
            if opt["name"] == "domain-name":
                opt_string += bytes([15, len(opt["value"])]) + str.encode(opt["value"])
            if opt["name"] == "subnet":
                opt_string += bytes([1, 4]) + socket.inet_aton(opt["value"])
            if opt["name"] == "lease-time":
                opt_string += bytes([51, 4]) + opt["value"].to_bytes(4, byteorder='big')
            if opt["name"] == "ip":
                ip = socket.inet_aton(opt["value"])

        f.close()

        opt_string += bytes([0xff])

        return self.__construct_ack(transaction_id, ip, opt_string)

    def __construct_ack(self, XID, ip, options):
        OP = bytes([0x02])
        HTYPE = bytes([0x01])
        HLEN = bytes([0x06])
        HOPS = bytes([0x00])
        # XID = bytes([0x39, 0x03, 0xF3, 0x26])
        SECS = bytes([0x00, 0x00])
        FLAGS = bytes([0x00, 0x00])
        CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
        CHADDR1 = bytes([0x00, 0x05, 0x3C, 0x04]) 
        CHADDR2 = bytes([0x8D, 0x59, 0x00, 0x00])
        CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
        CHADDR5 = bytes(192)
	
        package = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + ip + self.__ip + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + options

        return package

class OfferBuilder():
    ctx: DHCPServer
    _IP = bytes(4)
    _options = bytes(0)
    _time_servers = []
    _router = []
    _dns_servers =[]

    def __init__(self, context: DHCPServer, transaction_id):
        ctx = context
        _options = bytes([0x63, 0x82, 0x53, 0x63]) #magic cookie
        _options += bytes([53 , 1 , 2]) # DHCP offer

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

        return OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + self._IP + self.ctx.__ip + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4 + CHADDR5 + self._options

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




if __name__ == '__main__':
    dhcp_server = DHCPServer('192.168.2.1')
    dhcp_server.run()
