import asyncio
import desktop_notify
from functions.check_update import *

async def notify_user(message: str):
    try:
        notification = desktop_notify.Notify("GeForce Linexp", message)
        notification.set_timeout(10000)
        await notification.show()
        print("[SUCCESS] Send notification to user")
    except:
        print("[ERROR] Send notification to user")

def notifierOptionsJson_create():
    root = os.getcwd()[:os.getcwd().find("/geforce") + 15]

    if not os.path.exists(root + "/data"):
        os.mkdir(root + "/data")

    options = {
        "download-now" : "False",
        "show-no-new-drivers-notification" : "True" 
    }

    options_json = json.dumps(options, indent=2)


    with open(root + "/data/notifierOptions.json", "w") as jsonFile:
        jsonFile.write(options_json)

# Check network connection
ping_nvidia_website()

# Start Firefox browser
browser = start_browser()

# Search for new drivers
if os.path.exists(os.getcwd()[:os.getcwd().find("/geforce") + 15] + "/data/gCard.json"):
    gCard = find_graphicCardDriver(browser)

else:
    gCard = find_graphicCardDriver_noSaveData(browser)

# Check if notification options file exists
if not os.path.exists(os.getcwd()[:os.getcwd().find("/geforce") + 15] + "/data/notifierOptions.json"):
    notifierOptionsJson_create()

# Get notification options
with open(os.getcwd()[:os.getcwd().find("/geforce") + 15] + "/data/notifierOptions.json", "r") as notifierOp_jsonFile:
    notifierOp_json = json.load(notifierOp_jsonFile)

# Start to send notifications based on options
if type(gCard) != str:
    if notifierOp_json["download-now"] == "True":
        driverFile = download_graphicCardDriver(gCard)
        if driverFile != "download-fail":
            asyncio.run(notify_user(f"New driver available and ready to install for your {gCard.family} ({gCard.newVersion})."))
        else:
            asyncio.run(notify_user(f"New driver available for your {gCard.family} ({gCard.newVersion})."))
    else:
        asyncio.run(notify_user(f"New driver available for your {gCard.family} ({gCard.newVersion})."))
elif gCard == "up-to-date" and notifierOp_json["show-no-new-drivers-notification"] == "True":
    asyncio.run(notify_user("No new drivers available for your NVIDIA Graphic Card."))