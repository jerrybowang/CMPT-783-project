#!/usr/bin/python3
import argparse
import host_discovery as hd
import port_scanning as ps
import directory_enumeration as de
import result_generator as rg
import concurrent.futures
import time
import os

def dump_function():
    dump = 0

def remove_directory(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(path)


if __name__ == "__main__":
    # ================================================================================== #
    # ================================== Initialization ================================ #
    # initialize parser
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument(
        "-d","--discovery",
        type=str,
        help="Run Host Discovery module with CIDR argument. \
                \nThe format should be: {x.x.x.x/n}  \
                \nIf /n is not provided, the program will simply check the host availability with the provided address.",
        default=None,
        metavar="CIDR",
        nargs=1,
    )
    parser.add_argument(
        "-s", "--scanning",
        type=str,
        help="Run Port Scanning module with IP argument",
        default=None,
        metavar="IP",
        nargs=1
    )
    parser.add_argument(
        "--port-range",
        type=str,
        help="Specify the port range for Port Scanning module. If not provided, the program will scan the most common 1,000 ports.",
        default='',
        metavar="PORT_RANGE",
        nargs=1
    )
    parser.add_argument(
        "-e", "--enumeration",
        type=str,
        help="Run Directory Enumeration module with URL argument and an optional wordlist file. \
                \nIf wordlist file is not provided, the program will use the default wordlist.",
        default=None,
        metavar=("URL", "WORDLIST"),
        nargs="+"
    )
    parser.add_argument(
        "-S", "--schedule",
        help="Run the program in schedule mode",
        default=False,
        action="store_true"
    )
    args = parser.parse_args()

    # argument validation
    if args.enumeration:
        if len(args.enumeration) > 2:
            parser.error("Invalid number of arguments for Directory Enumeration module, at most 2 arguments are allowed")

    # result variables, includes metadata
    # change the default value accordingly
    host_discovery_result = ([], "", 0)
    port_scanning_result = []
    directory_enumeration_result = []

    if not any(vars(args).values()):
        # display help message when no argument is passed
        parser.print_help()
        parser.exit()
    
    # =============================== End of Initialization ============================ #
    # ================================================================================== #
    # =================================== Main Program ================================= #
    
    if args.schedule:
        # =================================== Schedule Module ================================= #
        config = {'Host_Discovery_Module': '', 
                  'Port_Scanning_Module': '', 
                  'Port_Scanning_Range': '',
                  'Directory_Enumeration_Module': '', 
                  'Customized_Wordlist': '', 
                  'Scan_Time_Interval': '0',
                  'Total_Scan_Number':'0'}
        
        print("Schedule mode")
        # read the schedule configuration file, if no file is found, the program will ask for the configuration
        try:
            # load config
            with open("schedule.conf", "r") as f:
                for line in f:
                    key, value = map(str.strip, line.split(':', 1))
                    config[key] = value
            # ============
            # print(config)

        except FileNotFoundError:
            print("No schedule configuration file found, please provide the configuration")
            # ask user for the configuration
            config['Host_Discovery_Module'] = input("\n- Please enter the CIDR for Host Discovery Module\n(Press Enter if NOT Active this module)\nCIDR: ")

            config['Port_Scanning_Module'] = input("\n- Please enter the IP Address for Port Scanning module\n(Press Enter if NOT Active this module)\nIP Address: ")
            if config['Port_Scanning_Module']:
                config['Port_Scanning_Range'] = input("\n- Please enter the Port Range for Port Scanning module\n(Input 1-100 if scan port 1 to 100)\n(Press Enter to use the most common 1,000 ports)\nPort Range: ")

                verified = not config['Port_Scanning_Range']
                while not verified:
                    try:
                        ver = config['Port_Scanning_Range'].split('-')
                        if len(ver) != 2:
                            raise ValueError
                        if int(ver[0]) > int(ver[1]):
                            raise ValueError
                        if int(ver[0]) < 0 or int(ver[1]) > 65535:
                            raise ValueError
                        verified = True
                    except (ValueError, IndexError):
                        print("Invalid port range, please provide the range in the format of '1-100'")
                        config['Port_Scanning_Range'] = input("\n- Please enter the Port Range for Port Scanning module\n(Input 1-100 if scan port 1 to 100)\n(Press Enter to use the most common 1,000 ports)\nPort Range: ")
                        verified = not config['Port_Scanning_Range']

            config['Directory_Enumeration_Module'] = input("\n- Please enter the URL for Directory Enumeration Module\n(Press Enter if NOT Active this module)\nURL: ")
            if config['Directory_Enumeration_Module']:
                config['Customized_Wordlist'] = input("\n- Please enter the wordlist for Directory Enumeration Module\n(Press Enter if use Default)\nThe file path of wordlist: ")
            
            config['Scan_Time_Interval'] = input("\n- Please enter the Scan Time Interval for scanning\n(Input 5 if scan every 5 minutes)\nThe Scan Time Interval: ")
            if not config['Scan_Time_Interval']:
                config['Scan_Time_Interval'] = '0'
            elif int(config['Scan_Time_Interval']) < 1:
                config['Scan_Time_Interval'] = '0'
            
            config['Total_Scan_Number'] = input("\n- Please enter the Total Scan Number\n(Input 5 if scan 5 times)\nTotal Scan Number: ")
            if not config['Total_Scan_Number']:
                config['Total_Scan_Number'] = '1'
            elif int(config['Total_Scan_Number']) < 1:
                config['Total_Scan_Number'] = '1'
            
            # save the configuration to the file and exit
            data_str = "\n".join([f"{key}: {value}" for key, value in config.items()])
            with open("schedule.conf", 'w') as f:
                f.write(data_str)
            print("\nNew config file is created, restart the program to run the scan.")
            parser.exit()
        
        # remove the result folder if it exists, for a clean start
        try:
            remove_directory("imm_result")
        except FileNotFoundError:
            pass
        os.mkdir("imm_result")
        
        # validate configuration
        if not config['Host_Discovery_Module'] and not config['Port_Scanning_Module'] and not config['Directory_Enumeration_Module']:
            print("Loaded configure file is invaild.")
            parser.exit()
        
        if config['Port_Scanning_Range']:
            try:
                ver = config['Port_Scanning_Range'].split('-')
                if len(ver) != 2:
                    raise ValueError
                if int(ver[0]) > int(ver[1]):
                    raise ValueError
                if int(ver[0]) < 0 or int(ver[1]) > 65535:
                    raise ValueError
            except (ValueError, IndexError):
                print("Invalid port range, loaded configure file is invaild")
                parser.exit()
            

        # execute the program based on the configuration
        count = int(config['Total_Scan_Number'])
        while count > 0:
            # reset the result
            host_discovery_result = ([], "", 0)
            port_scanning_result = []
            directory_enumeration_result = []
            

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                if config['Host_Discovery_Module']:
                    futures.append(executor.submit(hd.host_discovery, config['Host_Discovery_Module']))
                else:
                    futures.append(executor.submit(dump_function))

                if config['Port_Scanning_Module']:
                    port_range = config['Port_Scanning_Range'].split('-') if config['Port_Scanning_Range'] else []
                    futures.append(executor.submit(ps.scan_all_ports, config['Port_Scanning_Module'], port_range))
                else:
                    futures.append(executor.submit(dump_function))

                if config['Directory_Enumeration_Module']:
                    if not config['Customized_Wordlist']:
                        futures.append(executor.submit(de.enumerate_directory, config['Directory_Enumeration_Module'], 'default'))
                    else:
                        futures.append(executor.submit(de.enumerate_directory, config['Directory_Enumeration_Module'], config['Customized_Wordlist']))
                else:
                    futures.append(executor.submit(dump_function))

                # Wait for all futures to complete
                concurrent.futures.wait(futures)

                

                # Save results
                functions = [hd.host_discovery, ps.scan_all_ports, de.enumerate_directory]
                function_mapping = {future: func for future, func in zip(futures, functions)}

                for future in concurrent.futures.as_completed(futures):
                    func = function_mapping[future]
                    if func == hd.host_discovery:
                        host_discovery_result = future.result()
                        if not host_discovery_result:
                            host_discovery_result = ([], "", 0)
                    elif func == ps.scan_all_ports:
                        port_scanning_result = future.result()
                        if not port_scanning_result:
                            port_scanning_result = []
                    else:
                        directory_enumeration_result = future.result()
                        if not directory_enumeration_result:
                            directory_enumeration_result = []
                
                # print(host_discovery_result,"\n\n", port_scanning_result,"\n\n",directory_enumeration_result)

                rg.imm_file(host_discovery_result, 
                            port_scanning_result, 
                            directory_enumeration_result)
                
            count -= 1
            if count > 0:
                time.sleep(int(config['Scan_Time_Interval'])*60)
        
        print("\nAll scans are completed")
        print("The result files are saved in the 'imm_result' folder")
        print("To use the visualization tool, please run 'python3 subprocess_data_vis.py' in the terminal.")
                   

        
        


    else:
        # =================================== Other Modules ================================= #
        if args.discovery:
            print(f"Host Discovery module with argument: {args.discovery[0]}")
            # run host discovery module
            host_discovery_result = hd.host_discovery(args.discovery[0])
        if args.scanning:
            port_range = []
            if args.port_range:
                try:
                    port_range = args.port_range[0].split('-')
                    if len(port_range) != 2:
                        print("Invalid port range, please provide the range in the format of '1-100'")
                        parser.exit()
                    if int(port_range[0]) > int(port_range[1]):
                        print("Invalid port range, please provide the range in ascending order")
                        parser.exit()
                    if int(port_range[0]) < 0 or int(port_range[1]) > 65535:
                        print("Invalid port range, please provide the range within 0-65535")
                        parser.exit()
                except (ValueError, IndexError):
                    print("Invalid port range, please provide the range in the format of '1-100'")
                    parser.exit()
            print(f"Port Scanning module with argument: {args.scanning[0]}")
            port_scanning_result = ps.scan_all_ports(args.scanning[0], port_range)
        if args.enumeration:
            print(f"Directory Enumeration module with argument: {args.enumeration[0]} and wordlist: {args.enumeration[1] if len(args.enumeration) > 1 else 'default'}")
            if len(args.enumeration) > 1:
                directory_enumeration_result = de.enumerate_directory(args.enumeration[0], args.enumeration[1])
            else:
                directory_enumeration_result = de.enumerate_directory(args.enumeration[0], "") 
        # result generation
        rg.txt_result_generator(host_discovery_result, 
                                port_scanning_result, 
                                directory_enumeration_result)
        print("The result files are generated in result.txt file.")
        
    

