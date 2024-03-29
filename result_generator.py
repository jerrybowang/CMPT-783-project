from datetime import datetime
import os


# helper function to generate result file
def ip_sort_key(ip: str) -> tuple[int, ...]:
    # convert the ip address to a tuple of integers
    parts = [int(part) for part in ip.split('.')]
    return tuple(parts)


def txt_result_generator(host_discovery_result: tuple[list[str], str, int], 
                     port_scanning_result: list[str], 
                     directory_enumeration_result: list[tuple[str, int, int]]
                     ) -> None:
    with open("result.txt", "w") as result_file:
        result_file.write("Host Discovery Result:\n")
        if host_discovery_result[0] == []:
            result_file.write("No result")
        else:
            live_hosts = sorted(host_discovery_result[0], key=ip_sort_key)
            cidr = host_discovery_result[1]
            logical_range = host_discovery_result[2]
            result_file.write(f"{logical_range} hosts in CIDR: {cidr}, {len(live_hosts)} are up.\n")
            result_file.write("Live hosts:\n")
            for host in live_hosts:
                result_file.write(f"{host}\n")
        
        result_file.write("\n\nPort Scanning Result:\n")
        if port_scanning_result == []:
            result_file.write("No result")
        else:
            result_file.write(f"{len(port_scanning_result)} ports are open.\n")
            for port in port_scanning_result:
                result_file.write(f"{port}\n")

        result_file.write("\n\nDirectory Enumeration Result:\n")
        if directory_enumeration_result == []:
            result_file.write("No result")
        else:
            result_file.write(f"{len(directory_enumeration_result)} files and directories found\n")
            for result in directory_enumeration_result:
                result_file.write(f"{result[0]} (status: {result[1]}, size: {result[2]})\n")
    print("Result file generated successfully")
    return



def imm_file(host_discovery_result: tuple[list[str], str, int], 
                     port_scanning_result: list[str], 
                     directory_enumeration_result: list[tuple[str, int, int]]
                     ) -> None:

    # create a new folder for the result
    folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.mkdir(f"imm_result/{folder_name}")

    # update the summary and save the result as csv to the folder
    if host_discovery_result[0] != []:
        live_hosts = sorted(host_discovery_result[0], key=ip_sort_key)
        with open(f"imm_result/{folder_name}/host_discovery.csv", "w") as f:
            f.write("Live Hosts\n")
            for ip in live_hosts:
                f.write(f"{ip}\n")
        
    if port_scanning_result != []:
        with open(f"imm_result/{folder_name}/port_scanning.csv", "w") as f:
            f.write("Open Ports,Name\n")
            for port in port_scanning_result:
                component = port.split(":")
                f.write(f"{component[0]}, {component[1]}\n")

    if directory_enumeration_result != []:
        with open(f"imm_result/{folder_name}/directory_enumeration.csv", "w") as f:
            f.write("URL,Status,Size\n")
            for result in directory_enumeration_result:
                f.write(f"{result[0]},{result[1]},{result[2]}\n")

    
    

