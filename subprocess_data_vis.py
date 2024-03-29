import subprocess

# Define the command you want to execute
command = "npm start"
working_directory = "./js"

process = subprocess.Popen(command, cwd=working_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Read the output line by line as it is produced
for line in process.stdout:
    print(line, end='')

# Wait for the process to complete and get the exit code
return_code = process.wait()

# Check if the process was successful
if return_code == 0:
    print("Command executed successfully")
else:
    print("Command execution failed with return code", return_code)
