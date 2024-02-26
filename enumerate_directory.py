import requests
import sys
import os
import threading
import time

def read_names(names_file):
    names = []

    try:

        with open(names_file, 'r') as f:
            for line in f:
                names.append(line.strip())

        return names
    except FileNotFoundError:
        print("Loading default dictionaries: files not found")
    except Exception as e:
        print("Loading default dictionaries error:", str(e))
        
        
def enumerate_directory(url):
    """
    Enumerate files and directories within the specified URL.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            current_time = time.localtime()
            formatted_time = time.strftime("%H:%M:%S", current_time)
            print("("+formatted_time+")", url, "- (" + str(response.status_code) + " | " + str(len(response.content)) + ")")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Initialize:
    url = sys.argv[1]
    dir_names = []
    file_names = []
    dir_names = read_names("dictionary/dir_name_dictionary.txt")
    file_names = read_names("dictionary/file_name_dictionary.txt")
    
    # Enumerate Start:
    print("== Directory Enumeration Start ==")
    print("(Time) url (status | size)")
    for dirs in dir_names:
        temp_url = url+ "/" + dirs
        enumerate_directory(temp_url)
    print("\n== File Enumeration Start ==")
    for files in file_names:
        temp_url = url+ "/" + files
        enumerate_directory(temp_url)
    
        
