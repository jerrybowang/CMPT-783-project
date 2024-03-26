import requests
import concurrent.futures
# import time
import typing

# ===========================================================
# ====================== Auther's NOTE ======================
# ===========================================================
#
# return value is an list of tuples(url, HTTP_status_code, size)
# Enmuerated directory will not show the size
# HTTP_status_code == 404 / 0 will be dropped
# HTTP_status_code == -1 means the url is unavailable (not applicable any more)
# HTTP_status_code == 0  means there is an error accessing the url
#
# ===========================================================


def read_names(names_file):
    names = []

    try:
        with open(names_file, 'r') as f:
            for line in f:
                names.append(line.strip())

        if len(names) == 0:
            print(f"Wordlist \"{names_file}\" is empty.")

        return names
    except FileNotFoundError:
        print("Loading wordlist: files not found")
        return []
    except Exception as e:
        print("Loading wordlist error:", str(e))
        return []
        
        
def get_url_file(url):
    try:
        response = requests.get(url)
        return (url, response.status_code, len(response.content))
        #if response.status_code == 200:
        #   current_time = time.localtime()
        #   formatted_time = time.strftime("%H:%M:%S", current_time)
        #   print("("+formatted_time+")", url, "- (" + str(response.status_code) + " | " + str(len(response.content)) + ")")

    except Exception as e:
        print("An error occurred in ", url)
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
        print("An error occurred When accessing", url)
        return ("error", 0, 0)        


def enumerate_directory(url: str, wordlist: str) -> typing.List[tuple[str, int, int]]:
    """
    Enumerate files and directories within the specified URL.
    """
    # check if server is online
    if get_url_dir(url)[0] == "error":
        print(f"\n{url} is unavailable\n")
        # return [(url, -1, 0)]
        return []


    # Initialize:
    results = []
    dir_names = []
    file_names = []
    if wordlist:
        wordlist_input = read_names(wordlist)
        if len(wordlist_input) == 0:
            # check if no names are read
            print("Enumeration Stop")
            return []
        
        for name in wordlist_input:
            if name[-1] == "/":
                dir_names.append(name)
            else:
                file_names.append(name)
    else:
        dir_names = read_names("wordlist/dir_name_wordlist.txt")
        file_names = read_names("wordlist/file_name_wordlist.txt")
    

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
    
    
    print("== File Enumeration Start ==")
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
        

    print("== Enumeration Complete ==")

    return results


# if __name__ == "__main__":
#     url = sys.argv[1]
#     print(enumerate_directory(url, "wordlist/test_name_wordlist.txt"))
