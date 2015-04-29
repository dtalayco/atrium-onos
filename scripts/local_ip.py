#!/usr/bin/env python
# Display the local IP address to stdout

import socket

def get_onos_ip_addr():
    """
    Get the local IP address

    Hack from stack overflow.
    """
    full_list = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) \
                 for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]]
    return full_list[0][1]

print get_onos_ip_addr()
