
class DefaultDHCPServer():
    _server
    def __init__(self):
        self._server = DHCPServer('192.168.2.1', self.discoveryHandler, self.requestHandler)

    def start(self):
        self._server.run()

    def discoveryHandler(self):
        pass

    def requestHandler(self):
        pass

if __name__ == '__main__':
    dhcp_server = DefaultDHCPServer('192.168.2.1')
    dhcp_server.start()