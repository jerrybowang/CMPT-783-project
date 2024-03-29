import socket
import pickle
import time
import concurrent.futures



def port_scanning(ip: str, port: int) -> str:    
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the timeout
    s.settimeout(0.5)
    # connect to the server
    try:
        s.connect((ip, port))   
        try:
            service = socket.getservbyport(port)
        except socket.error:
            service = "unknown"
        server_port= f"{port}:{service}"
        return server_port
    except:
        return ""
    # close the socket
    # s.close()

def scan_all_ports(ip: str, port_range: list[str]) -> list[str]:
    startTime = time.time()
    ports_info = []

    if port_range:
        scan_range = range(int(port_range[0]), int(port_range[1]) + 1)
    else:
        # load the ports list from the file
        with open('common_ports.pickle', 'rb') as f:
            scan_range = pickle.load(f)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_port = {executor.submit(port_scanning, ip, port): port for port in scan_range}
        concurrent.futures.wait(future_to_port)
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                ports_info.append(result)


    print('Time taken:', time.time() - startTime)
    print('Open ports:', ports_info)
    return ports_info





# port scanning module without threading

# def port_scanning(ip: str, port: int,open_ports) -> None:    
#     # create a socket object
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # set the timeout
#     s.settimeout(0.5)
#     # connect to the server
#     try:
#         s.connect((ip, port))   
#         try:
#             service = socket.getservbyport(port)
#         except socket.error:
#             service = "unknown"
#         server_port= f"{port}:{service}"
#         open_ports.append(server_port)
#     except:
#         return None
#     # close the socket
#     s.close()

# def scan_all_ports(ip: str) -> tuple[typing.List[str], float]:
#     startTime = time.time()
#     ports_info = []

#     for port in range(1, 65536):
#         # Call the port_scanning function directly
#         port_scanning(ip, port, ports_info)

#     print('Time taken:', time.time() - startTime)
#     print('Open ports:', ports_info)
#     return ports_info, time.time() - startTime