import subprocess
import threading
import ipaddress
import typing

mutex = threading.Lock()

def check_host(pin: str, live_hosts: typing.List[str]):
  command = ["ping", pin, "-c", "1"]
  # don't care about the ping output
  result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  
  if result.returncode == 0:
    # critical section, need to lock
    with mutex:
        # critical section
        live_hosts.append(pin)
    


def get_live_hosts(ips: typing.Iterator, live_hosts: typing.List[str]):
  threads = []
  for i in ips:
    thread = threading.Thread(target=check_host, args=[str(i), live_hosts])
    thread.start()
    threads.append(thread)

  # wait for all the threads to finish
  for thread in threads:
    thread.join()

  return

def host_discovery(cidr: str) -> typing.List[str]:
    live_hosts = []
    try:
        # try to parse the CIDR
        ip_network = ipaddress.ip_network(cidr)
        # ping it
        get_live_hosts(ip_network.hosts(), live_hosts)
    except ValueError:
        print(f"Invalid CIDR: {cidr}")

    return live_hosts
    
