from enum import IntEnum

class DHCPOption(IntEnum):
    PAD = 0
    SUBNET = 1
    ROUTER = 3
    TIME_SERVER = 4
    DNS_SERVER = 6
    DOMAIN_NAME = 15
    REQUESTED_IP = 50
    LEASE_TIME = 51
    MESSAGE_TYPE = 53
    DHCP_SERVER = 54
    REQUESTED_OPTIONS = 55
    END = 255