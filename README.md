# CMPT-783-project

## Group menber
- Jerry Wang: [@jerrybowang](https://github.com/jerrybowang)
- Roy Zhong: [@royroyzhong](https://github.com/royroyzhong)
- Barry Zhao: [@Barry7043](https://github.com/Barry7043)

## Problem Definition
During penetration testing and security audits of web applications and websites, discovering the hidden or unauthorized access directories of the target system is a crucial task. The current state-of-the-art tools (Nmap, Dirb, Dirbuster, Gobuster) don’t have a built-in scheduled scanning feature, and they cannot detect changes in the state (eg. IP availability, Web Directory file addition/delete).

## Initial Idea
To simplify this process, we intend to develop a Web Directory Enumeration Tool that aims to provide fast and accurate directory and file structure identification functionality. In addition, we also want to include a scheduled scanning feature to automate the process and a mechanism to detect changes in the target system's state, such as alterations in IP availability or the addition/deletion of web directory files.

## Functional Requirements (Scope)
1. Scheduled Scanning: Implementing a scheduling feature allows users to set specific times for automatic scans, ensuring regular and timely assessments without manual intervention.
2. State Change Detection: Building a mechanism to detect changes in the target system's state provides an added layer of security. This includes monitoring IP availability changes and modifications to the web directory, ensuring that any unauthorized alterations are promptly identified.
3. Directory Enumeration: Implement directory structure enumeration for the target web application, including common directories and potential hidden directories.
4. Dictionary Attack: Provide dictionary attack functionality, allowing users to customize dictionary files to extend or adjust the guessing of directory and file names.
5. Multithreading Support: Enhance the speed of directory enumeration by utilizing multi-threading techniques for more efficient scanning of the target system.
6. HTTP Response Analysis: Analyze the HTTP responses of the target system to determine which directories are valid, which ones do not exist, or which have unauthorized access.
7. Results Reporting: Generate a clear and readable results report displaying the discovered directory and file structure for users to identify potential security risks quickly.
8. User Interface: Provide a simple and intuitive user interface to make the tool accessible to non-expert users.
9. TCP Port Scanning: Scan the open ports given IP 
10. Host Discovery: Discover active hosts' IPs in the network
11. Configuration Options: Allow users to configure scanning options, including timeout settings, thread count, and other relevant parameters.


