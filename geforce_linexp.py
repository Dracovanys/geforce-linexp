from functions.check_update import *

# Check network connection
print("Checking connection with NVIDIA official website...", end="")
if ping_nvidia_website() == "ERROR":
    quit()

# Search for new drivers
print("Looking for new drivers to your NVIDIA graphic card...", end="")
graphicCardDriver = find_graphicCardDriver_noSaveData()

if graphicCardDriver == "no-linux-driver":
    print(f"OK\n\nThere isn't drivers of your NVIDIA Graphic Card available for Linux OS.")
elif graphicCardDriver == "up-to-date":
    print("OK\n\nYour NVIDIA Graphic Card is up-to-date.")
else:
    print(f"OK\n\n")

# Request to download

# Start download via wget