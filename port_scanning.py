import socket
import time
import typing



def port_scanning(ip: str, port: int, open_ports: list) -> None:    
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the timeout
    s.settimeout(0.5)
    # connect to the server
    try:
        s.connect((ip, port))
        server_name = socket.gethostbyaddr(ip)[0]     
        server_port= f"{server_name}:{port}"
        open_ports.append(server_port)
    except:
        return None
    # close the socket
    s.close()

def scan_all_ports(ip: str) -> tuple[typing.List[str], float]:
    startTime = time.time()
    ports_info = []

    for port in range(1, 65536):
        # Call the port_scanning function directly
        port_scanning(ip, port, ports_info)

    print('Time taken:', time.time() - startTime)
    print('Open ports:', ports_info)
    return ports_info, time.time() - startTime