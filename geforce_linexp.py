from time import sleep
from functions.check_update import *


print("Checking connection with NVIDIA official website...", end="")

if ping_nvidia_website() == "ERROR":
    quit()

print("Looking for new drivers to your NVIDIA graphic card...", end="")
graphicCardDriver_path = find_graphicCardDriver_noSaveData()

if graphicCardDriver_path == "No Linux driver":
    print("OK\n\nThere isn't new NVIDIA drivers for Linux OS.")
else:
    print(f"OK\n\n{graphicCardDriver_path}")