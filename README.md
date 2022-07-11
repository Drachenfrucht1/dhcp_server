Usage
=====
Create as many configs as you need and Name them 1.json, ..., n.json. The file example.json contains a config.\
Next start the dhcp server using `python server.py <ip-adress>` where ip-adress is the ip of the local computer. You need to run the server with privileged right because it uses port 67.\
The server will currently crash after all all configs have been served once. After making an offer it will accept any message as a DHCP request message regardless of the content (will be fixed later).


The code is based on [this](https://github.com/playma/simple_dhcp) project