import requests
import sys
import os
import concurrent.futures
import time
import typing

def read_names(names_file):
    names = []

    try:
        with open(names_file, 'r') as f:
            for line in f:
                names.append(line.strip())

        return names
    except FileNotFoundError:
        print("Loading dictionaries: files not found")
        return names
    except Exception as e:
        print("Loading dictionaries error:", str(e))
        return names
        
        
def get_url_file(url):
    try:
        response = requests.get(url)
        return (url, response.status_code, len(response.content))
        #if response.status_code == 200:
        #   current_time = time.localtime()
        #   formatted_time = time.strftime("%H:%M:%S", current_time)
        #   print("("+formatted_time+")", url, "- (" + str(response.status_code) + " | " + str(len(response.content)) + ")")

    except Exception as e:
        print("An error occurred:", str(e))
        return ("error", 0, 0)

        
def get_url_dir(url):
    try:
        response = requests.get(url)
        return (url, response.status_code, 0)
        #if response.status_code == 200:
        #   current_time = time.localtime()
        #   formatted_time = time.strftime("%H:%M:%S", current_time)
        #   print("("+formatted_time+")", url, "- (" + str(response.status_code) + " | " + str(len(response.content)) + ")")

    except Exception as e:
        print("An error occurred:", str(e))
        return ("error", 0, 0)        


def enumerate_directory(url: str, dictionary: str) -> typing.List[tuple[str, int, int]]:
    """
    Enumerate files and directories within the specified URL.
    """
    # Initialize:
    results = []
    dir_names = []
    file_names = []
    if dictionary != "default":
        dictionary_input = read_names(dictionary)
        for name in dictionary_input:
            if name[-1] == "/":
                dir_names.append(name)
            else:
                file_names.append(name)
    else:
        dir_names = read_names("dictionary/dir_name_dictionary.txt")
        file_names = read_names("dictionary/file_name_dictionary.txt")
    
    
    
    # Enumerate Start:
    print("== Directory Enumeration Start ==")
    #print("(Time) url (status | size)")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enumerate directories
        futures = []
        for dirs in dir_names:
            temp_url = url + "/" + dirs
            futures.append(executor.submit(get_url_dir, temp_url))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        
        # Save results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result[1] != 404 and result[1] != 0:
                results.append(result)
    
    
    print("\n== File Enumeration Start ==")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Enumerate files
        futures = []
        for files in file_names:
            temp_url = url+ "/" + files
            futures.append(executor.submit(get_url_file, temp_url))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        
        # Save results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result[1] != 404 and result[1] != 0:
                results.append(result)
        

    print("\n== Enumeration Complete ==")

    return results


if __name__ == "__main__":
    url = sys.argv[1]
    print(enumerate_directory(url, "dictionary/test_name_dictionary.txt"))
