import subprocess
import threading
import ipaddress
import typing

mutex = threading.Lock()


def check_host(pin: str, live_hosts: typing.List[str]) -> None:
    command = ["ping", pin, "-c", "1"]
    # don't care about the ping output
    result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        # critical section, need to lock
        with mutex:
            # critical section
            live_hosts.append(pin)
    return


def get_live_hosts(ips: typing.Iterator, live_hosts: typing.List[str]) -> int:
    threads = []
    count = 0
    for i in ips:
        count += 1
        thread = threading.Thread(target=check_host, args=[str(i), live_hosts])
        thread.start()
        threads.append(thread)

    # wait for all the threads to finish
    for thread in threads:
        thread.join()

    return count


def host_discovery(cidr: str) -> tuple[typing.List[str], str, int]:
    live_hosts = []
    logical_range = 0
    try:
        # try to parse the CIDR
        ip_network = ipaddress.ip_network(cidr)
        # ping it
        logical_range = get_live_hosts(ip_network.hosts(), live_hosts)
    except ValueError:
        print(f"Invalid CIDR: {cidr}")
        return [], "", 0

    return live_hosts, cidr, logical_range
