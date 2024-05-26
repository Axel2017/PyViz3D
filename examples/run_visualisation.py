import os
import subprocess
import time

# Define the directory and port
directory = f'{os.getcwd()}/running_visualisation'
port = 6008

# Start the local server
def start_server():
    # Use os.path to ensure the path is correct
    path = os.path.abspath(directory)
    command = f'cd "{path}" && python -m http.server {port}'
    process = subprocess.Popen(command, shell=True)
    return process

# Open a private Safari tab
def open_private_tab():
    script = f'''
    tell application "Safari"
        activate
        delay 0.3
        tell application "System Events"
            keystroke "N" using {{shift down, command down}}
            delay 0.3
            keystroke "http://localhost:{port}"
            delay 0.3
            keystroke return
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', script])

if __name__ == "__main__":
    # Start the server
    server_process = start_server()

    # Wait for the server to start
    time.sleep(0.3)
    # Open the private tab in Safari
    open_private_tab()

    # You can add logic here to keep the Python script running if needed
    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
