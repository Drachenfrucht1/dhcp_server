import json
import argparse

from defaultserver import DefaultDHCPServer

if __name__ == '__main__':
    f = None
    cnf = {}
    try:
        f = open('config.json')
        cnf = json.load(f)
    except:
        pass

    parser = argparse.ArgumentParser(description="DHCP Server with minimal configuration options")
    parser.add_argument('--server', '-s', help='IP address of this computer')
    parser.add_argument('--subnet', '-sn', help='Subnet mask of the local subnet')
    parser.add_argument('--router', '-r', help='IP address of the router')
    parser.add_argument('-ip', help='IP address of this computer. Either given as a range (e.g. 192-168.100-192.168.2.255) or as a comma separated list of Ip addresses')

    args = parser.parse_args()

    if args.server is not None:
        cnf['server_ip'] = args.server

    if args.subnet is not None:
        cnf['subnet'] = args.subnet

    if args.router is not None:
        cnf['router'] = args.router

    if args.ip is not None:
        if '-' in args.ip:
            s = args.ip.split('-')

            cnf['ip'] = {}
            cnf['ip']['start'] = s[0]
            cnf['ip']['end'] = s[1]
        else:
            cnf['ip'] = args.ip.split(',')

    dhcp_server = DefaultDHCPServer(cnf['ip'], cnf['server_ip'], cnf['subnet'], cnf['router'], cnf['leasetime'])
    dhcp_server.start()