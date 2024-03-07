#!/usr/bin/python3
import argparse
import host_discovery as hd
import port_scanning as ps
import directory_enumeration as de
import result_generator as rg
import os

if __name__ == "__main__":
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
    

    # main logic
    if args.schedule:
        config = {}
        print("Schedule mode")
        # read the schedule configuration file, if no file is found, the program will ask for the configuration
        try:
            with open("schedule.conf", "r") as f:
                schedule_config = f.readlines()
                print(schedule_config)
                # load the configuration

        except FileNotFoundError:
            print("No schedule configuration file found, please provide the configuration")
            # ask user for the configuration

            # save the configuration to the file and exit
            parser.exit()
        
        # remove the result folder if it exists, for a clean start
        try:
            os.rmdir("imm_result")
        except FileNotFoundError:
            pass
        os.mkdir("imm_result")
        
        # run the program based on the configuration

        # each round, need to call rg.imm_file() at the end
        # rg.imm_file(host_discovery_result, 
        #                     port_scanning_result, 
        #                     directory_enumeration_result)
        
        


    else:
        if args.discovery:
            print(f"Host Discovery module with argument: {args.discovery[0]}")
            # run host discovery module
            host_discovery_result = hd.host_discovery(args.discovery[0])
        if args.scanning:
            print(f"Port Scanning module with argument: {args.scanning[0]}")
            port_scanning_result = ps.scan_all_ports(args.scanning[0])
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
        # rg.imm_file(host_discovery_result, 
        #             port_scanning_result, 
        #             directory_enumeration_result)
        
    

