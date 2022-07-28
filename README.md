Usage
=====
DHCP Server for simply configuration of Cisco Small Business Devices (SG300,350,550, CBS350..) 
You have to create JSONs with DHCP Options per device and assign them to a device Type per Vendor Class (will be added soon) or 
assign them to defined MacAdress (easier for verifaction after config time)
add Firmware Updates to DHCP Option if wished 
configure an external TFTP Server for File Management
Next start the dhcp server using `python server.py <ip-adress>` where ip-adress is the ip of the local computer. You need to run the server with privileged right because it uses port 67.\
The server will currently crash after all all configs have been served once. After making an offer it will accept any message as a DHCP request message regardless of the content (will be fixed later).


The code is based on [this](https://github.com/playma/simple_dhcp) project
