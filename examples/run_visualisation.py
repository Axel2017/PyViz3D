import os
import subprocess
import platform
import time

# Add utils directory to the path
import sys
sys.path.append(f"{os.getcwd()}/utils")
import utils

# Define the directory and port
directory = os.path.join(os.getcwd(), "running_visualisation")
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
    if utils.OPERATING_SYSTEM == 'Darwin':  # macOS
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
    elif utils.OPERATING_SYSTEM == 'Windows':  # Windows
        edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        url = f"http://localhost:{port}"
        subprocess.Popen([edge_path, url])
    elif utils.OPERATING_SYSTEM == 'Linux':  # Linux
        firefox_path = '/usr/bin/firefox'
        url = f"http://localhost:{port}"
        subprocess.Popen([firefox_path, '--new-window', url])
    else:
        print(f"Unsupported operating system: {utils.OPERATING_SYSTEM}")

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
