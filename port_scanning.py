import socket
import time
import threading
import queue

startTime = time.time()

def port_scanning(ip, port,open_ports_queue):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the timeout
    s.settimeout(0.5)
    # connect to the server
    try:
        s.connect((ip, port))
        open_ports_queue.put(port)

    except:
        return None
    # close the socket
    s.close()

def scan_all_ports(ip):
    # Create a list to hold all the threads
    threads = []
    open_ports_queue = queue.Queue()

    for port in range(1, 65536):
        # Create a new thread for each port scan
        thread = threading.Thread(target=port_scanning, args=(ip, port,open_ports_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
        

    print('Time taken:', time.time() - startTime)
    # Collect all open ports
    open_ports = []
    while not open_ports_queue.empty():
        open_ports.append(open_ports_queue.get())
    print('Open ports:', open_ports)
    return open_ports, time.time() - startTime