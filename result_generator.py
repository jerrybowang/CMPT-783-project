

# helper function to generate result file
def ip_sort_key(ip: str) -> tuple[int, ...]:
    # convert the ip address to a tuple of integers
    parts = [int(part) for part in ip.split('.')]
    return tuple(parts)


def result_generator(host_discovery_result: tuple[list[str], str, int, float], 
                     port_scanning_result: tuple[list[str], float], 
                     directory_enumeration_result
                     ) -> None:
    with open("result.txt", "w") as result_file:
        result_file.write("Host Discovery Result:\n")
        if host_discovery_result[0] == []:
            result_file.write("No result")
        else:
            live_hosts = sorted(host_discovery_result[0], key=ip_sort_key)
            cidr = host_discovery_result[1]
            logical_range = host_discovery_result[2]
            result_file.write(f"{logical_range} hosts in CIDR: {cidr}, {len(live_hosts)} are up. Time taken: {format(host_discovery_result[3], '.4f')} s\n")
            result_file.write("Live hosts:\n")
            for host in live_hosts:
                result_file.write(f"{host}\n")
        
        result_file.write("\n\nPort Scanning Result:\n")
        if port_scanning_result is None or port_scanning_result[0] == []:
            result_file.write("No result")
        else:
            result_file.write(f"{len(port_scanning_result[0])} ports are open. Time taken: {format(port_scanning_result[1], '.4f')} s\n")
            for port in port_scanning_result[0]:
                result_file.write(f"{port}\n")

        result_file.write("\n\nDirectory Enumeration Result:\n")
        if directory_enumeration_result is None:
            result_file.write("No result")
        else:
            result_file.write(str(directory_enumeration_result))
    print("Result file generated successfully")
    return

