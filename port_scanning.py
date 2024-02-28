import socket
import time
import threading
import queue



def port_scanning(ip, port, open_ports):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the timeout
    s.settimeout(0.5)
    # connect to the server
    try:
        s.connect((ip, port))
        open_ports.append(port)
    except:
        return None
    # close the socket
    s.close()

def scan_all_ports(ip):
    startTime = time.time()
    open_ports = []

    for port in range(1, 65536):
        # Call the port_scanning function directly
        port_scanning(ip, port, open_ports)

    print('Time taken:', time.time() - startTime)
    print('Open ports:', open_ports)
    return open_ports, time.time() - startTime