import socket

def ip_str_or_b_to_b(ip: (str | bytes)) -> bytes:
    if isinstance(ip, str):
        return socket.inet_aton(ip)
    return bytes