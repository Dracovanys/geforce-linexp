from lib2to3.pgen2 import driver
from functions.check_update import *

# Check network connection
print("Checking connection with NVIDIA official website...", end="")
if ping_nvidia_website() == "ERROR":
    quit()

# Search for new drivers
if os.path.exists(os.getcwd()[:os.getcwd().find("/geforce") + 15] + "/data/gCard.json"):
    print("Looking for new drivers to your NVIDIA graphic card...", end="")
    graphicCardDriver = find_graphicCardDriver()

else:
    print("Looking for new drivers to your NVIDIA graphic card...", end="")
    graphicCardDriver = find_graphicCardDriver_noSaveData()

if graphicCardDriver == "no-linux-driver":
    print("OK\n\nThere isn't drivers of your NVIDIA Graphic Card available for Linux OS.")
elif graphicCardDriver == "up-to-date":
    print("OK\n\nYour NVIDIA Graphic Card is up-to-date.")
else:
    print(f"OK\n\nNew driver available (Current: {graphicCardDriver.curVersion} / New: {graphicCardDriver.newVersion}) for your {graphicCardDriver.family}!")

    # Request to download
    invalid_option = True
    while invalid_option:
        download_option = input("Do you want to download it [y/n]? ")
        if download_option == "y":
                driverFile = download_graphicCardDriver(graphicCardDriver)
                invalid_option = False
        elif download_option == "n":
            quit()
        else:
            print("Invalid option. ", end="")
            invalid_option = True

    # Request fo install
    if driverFile != "download-fail":
        invalid_option = True
        while invalid_option:
            install_option = input("Do you want to install it [y/n]? ")
            if install_option == "y":
                    print("")
                    driverFile = install_graphicCardDriver(driverFile)
                    invalid_option = False
            elif install_option == "n":
                quit()
            else:
                print("Invalid option. ", end="")
                invalid_option = True

