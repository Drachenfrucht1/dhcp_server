# DHCP server
A sipmle dhcp server implementation in python.

## Usage as a DHCP server
This project can be run as a dhcp server in your home network.
- Change the parameters in the config file ```config.json```. The ```ip``` field can either contain a dictionary representing a range of IP addresses or a list of single IP addresses to assign.
- Start the server using ```python main.py```. Make sure to run the server with privileged rigths as it uses port 67/68.

## Usage for your own project
You can also use the DHCPServer class to create a dhcp server for your own purpose. An example use could be to configure switches via DHCP with custom parameters. The DHCPServer class takes the server IP address and four functions as arguments.
- ```discoveryHandler```: called when a DHCP discovery message has been received. It is given the dhcp message as a dictionary and a pre-configured DHCPOffer object. Return the DHCPOffer object to send an offer or None to send none.
- ```requestHandler```: Called when a DHCP request message has been received. It is given the dhcp message as a dictionary and a pre-configured DHCPAcknowledgment object. Return the DHCPAcknowledgment object to send a (N)ACK or None to send none.
- ```declineHandler```: Called when a DHCP decline message has been received. It is given the dhcp message as a dictionary.
- ```releaseHandler```: Called when a DHCP release message has been received. It is given the dhcp message as a dictionary.
For inspiration look at the implementation in defaultserver.py

The code is based on [this](https://github.com/playma/simple_dhcp) project