import subprocess

# Command to run the data visualization server
command = "npm start"
working_directory = "./js"

process = subprocess.Popen(command, cwd=working_directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Read the outputs of the process
for line in process.stdout:
    print(line, end='')

# Wait for the process to finish
return_code = process.wait()

# Check if the process was successful
if return_code == 0:
    print("Command executed successfully")
else:
    print("Command execution failed with return code", return_code)
