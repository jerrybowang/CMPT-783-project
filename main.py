#!/usr/bin/python3
import argparse
import host_discovery as hd
import port_scanning as ps
import directory_enumeration as de
import result_generator as rg

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
    args = parser.parse_args()

    # argument validation
    if args.enumeration:
        if len(args.enumeration) > 2:
            parser.error("Invalid number of arguments for Directory Enumeration module, at most 2 arguments are allowed")

    # result variables
    host_discovery_result = None
    port_scanning_result = None
    directory_enumeration_result = None
    # main logic
    if args.discovery:
        print(f"Host Discovery module with argument: {args.discovery[0]}")
        # run host discovery module
        host_discovery_result = hd.host_discovery(args.discovery[0])
        print(host_discovery_result)
    if args.scanning:
        print(f"Port Scanning module with argument: {args.scanning[0]}")
    if args.enumeration:
        print(f"Directory Enumeration module with argument: {args.enumeration[0]} and wordlist: {args.enumeration[1] if len(args.enumeration) > 1 else 'default'}")
    if not any(vars(args).values()):
        # display help message when no argument is passed
        parser.print_help()
        parser.exit()
    
    # result generation
    
    

