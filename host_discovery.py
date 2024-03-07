import subprocess
import ipaddress
import concurrent.futures
import platform



def check_host(pin: str, live_hosts: list[str]) -> str:
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "1", pin]
    else:
        command = ["ping", "-c", "1", pin]
    
    # don't care about the ping output
    result = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        return pin
    else:
        return ''



def host_discovery(cidr: str) -> tuple[list[str], str, int]:
    live_hosts = []
    logical_range = 0
    try:
        # try to parse the CIDR
        ip_network = ipaddress.ip_network(cidr)
        # ping it use concurrent.futures.ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=256) as executor:
            futures = []
            for ip in ip_network.hosts():
                logical_range += 1
                futures.append(executor.submit(check_host, str(ip), live_hosts))

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

            # Save results
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result != '':
                    live_hosts.append(result)
        
    except ValueError:
        print(f"Invalid CIDR: {cidr}")
        return ([], "", 0)

    return live_hosts, cidr, logical_range
