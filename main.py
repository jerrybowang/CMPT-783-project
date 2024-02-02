#!/usr/bin/python3
import argparse


if __name__ == "__main__":
    # initialize parser
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument(
        "--hd",
        help="Run the Host Discovery module and let the program prompt you",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--ps",
        help="Run the Port Scanning module and let the program prompt you",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--de",
        help="Run the Directory Enumeration module and let the program prompt you",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-d",
        type=str,
        help="Run Host Discovery module with IP range argument. \
                \nThe format should be: {x.x.x.x/n}  \
                \nIf /n is not provided, the program will simply check the host availability with the provided address.",
        default=None,
        metavar="IP",
        nargs=1
    )
    parser.add_argument(
        "-s",
        type=str,
        help="Run Port Scanning module with IP argument",
        default=None,
        metavar="IP",
        nargs=1
    )
    parser.add_argument(
        "-e",
        type=str,
        help="Run Directory Enumeration module with URL argument and an optional wordlist file. \
                \nIf wordlist file is not provided, the program will use the default wordlist.",
        default=None,
        metavar=("URL", "WORDLIST"),
        nargs="+"
    )
    args = parser.parse_args()

    # argument validation
    if args.e:
        if len(args.e) > 2:
            parser.error("Invalid number of arguments for Directory Enumeration module, at most 2 arguments are allowed")

    # main logic
    if args.hd:
        print("Host Discovery module")
    elif args.ps:
        print("Port Scanning module")
    elif args.de:
        print("Directory Enumeration module")
    elif args.d:
        print(f"Host Discovery module with argument: {args.d}")
    elif args.s:
        print(f"Port Scanning module with argument: {args.s}")
    elif args.e:
        print(f"Directory Enumeration module with argument: {args.e}")
    else:
        # display help message when no argument is passed
        parser.print_help()
