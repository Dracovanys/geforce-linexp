from functions.check_update import *

# Check network connection
ping_nvidia_website()

# Start Firefox browser
browser = start_browser()

# Search for new drivers
if os.path.exists(get_rootFolder() + "/data/gCard.json"):
    gCard = find_graphicCardDriver(browser)

else:
    gCard = find_graphicCardDriver_noSaveData(browser)

if gCard == "no-linux-driver":
    log("There isn't drivers of your NVIDIA Graphic Card available for Linux OS.")
elif gCard == "up-to-date":
    log("Your NVIDIA Graphic Card is up-to-date.")
elif gCard == "no-support":
    log("Unfortunately, this tool can't work with your NVIDIA Graphic Card yet.")
elif gCard == "unknown-error":
    log("An unknown error occurred, please restart execution.\nNOTE: If error persists, please give the details on GitHub repository: https://github.com/Dracovanys/geforce-linexp")
elif gCard == "NVMLError":
    log("NVIDIA Graphic Card verification failed, follow this instructions to solve: https://www.murhabazi.com/install-nvidia-driver")
else:
    log(f"New driver available (Current: {gCard.curVersion} / New: {gCard.newVersion}) for your {gCard.family}!")

    # Request to download
    invalid_option = True
    while invalid_option:
        download_option = input("Do you want to download it [y/n]? ")
        if download_option == "y":
                driverFile = download_graphicCardDriver(gCard)
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

