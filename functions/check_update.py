import igpu
import os
import json
import requests
import wget
from ping3 import ping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class graphicCard:
    def __init__(self):
        gpu = igpu.get_device(0)
        self.family = gpu.name.strip().strip("NVIDIA ")
        self.curVersion = ""
        self.newVersion = ""
        self.newDriverPath = ""

        for num in igpu.nvidia_driver_version():
            if len(self.curVersion) < 1:
                self.curVersion += str(num)
            else: self.curVersion += f".{str(num)}"

def ping_nvidia_website():
    pingResult = ping("www.nvidia.com")
    if pingResult == None or pingResult == False:
        print("ERROR")
    else:
        print("OK")

def get_driverDownloadPage():
    graphicCard_website = BeautifulSoup(requests.get("https://www.nvidia.com/").text, "html.parser")            

    # Find path to download driver page
    for link in graphicCard_website.find_all("a"):
        if str(link).find("/Download/") != -1:
            return str(link.get("href"))
        elif link == graphicCard_website.find_all("a")[-1]:
            print("ERROR")

def find_graphicCardDriver():
    root = os.getcwd()[:os.getcwd().find("/geforce") + 15]

    gCard = graphicCard()

    with open(root + "/data/gCard.json", "r") as gCard_jsonFile:
        gCard_json = json.load(gCard_jsonFile)
    
    browser = webdriver.Firefox()
    browser.get(get_driverDownloadPage())

    # Selecting GC Series Type
    for pST_option in browser.find_element(By.XPATH, "//select[@name='selProductSeriesType']").find_elements(By.TAG_NAME, "option"):
        if pST_option.get_attribute("text") == gCard_json["seriesType"]:
            pST_option.click()
            break
    
    # Selecting GC Series
    for pS_option in browser.find_element(By.XPATH, "//select[@name='selProductSeries']").find_elements(By.TAG_NAME, "option"):
        if pS_option.get_attribute("text") == gCard_json["series"]:
            pS_option.click()
            break
    
    # Selecting GC Family
    for pF_option in browser.find_element(By.XPATH, "//select[@name='selProductFamily']").find_elements(By.TAG_NAME, "option"):
        if pF_option.get_attribute("text") == gCard_json["family"]:
            pF_option.click()
            break
    
    driver_availableToLinux = False
    for operationSys in browser.find_element(By.XPATH, "//select[@id='selOperatingSystem']").find_elements(By.TAG_NAME, "option"):
        if operationSys.get_attribute("text").strip() == "Linux 64-bit":
            driver_availableToLinux = True
            operationSys.click()
    if driver_availableToLinux:
        browser.find_element(By.XPATH, "//a[@href='javascript: GetDriver();']").click()
        driverVersion = browser.find_element(By.XPATH, "//td[@id='tdVersion']").text        
        browser.find_element(By.XPATH, "//a[@id='lnkDwnldBtn']").click()
        for a in browser.find_elements(By.TAG_NAME, "a"):
            if a.get_attribute("href") != None:
                if a.get_attribute("href").find("download.nvidia") != -1:
                    newDriver_path = a.get_attribute("href")
        browser.close()

        # Comparing installed NVIDIA driver version with website's NVIDIA driver version
        if driverVersion[:7] == gCard.curVersion:
            return "up-to-date"
        else:
            gCard.newDriverPath = newDriver_path
            gCard.newVersion = driverVersion[:7]
            return gCard
    else:
        browser.close()
        return "no-linux-driver"

def find_graphicCardDriver_noSaveData():
    gCard = graphicCard()
    
    browser = webdriver.Firefox()
    browser.get(get_driverDownloadPage())

    # Navigating through GC Series Type
    productSeriesType_list = browser.find_element(By.XPATH, "//select[@name='selProductSeriesType']").find_elements(By.TAG_NAME, "option")
    for pST_option in productSeriesType_list:                
        pST_option.click()

        # Navigating through GC Series
        productSeries_list = browser.find_element(By.XPATH, "//select[@name='selProductSeries']").find_elements(By.TAG_NAME, "option")
        for pS_option in productSeries_list:
            if pS_option.get_attribute("class") != "psLess" and pS_option.get_attribute("class") != "psBothHead" and pS_option.get_attribute("class") != "psAll":
                pS_option.click()

                # Navigating through GC Family
                if browser.find_element(By.XPATH, "//tr[@id='trProductFamily']").is_displayed():
                    productFamily_list = browser.find_element(By.XPATH, "//select[@name='selProductFamily']").find_elements(By.TAG_NAME, "option")
                    for pF_option in productFamily_list:

                        # Specific graphic card
                        if pF_option.get_attribute("text").strip() == gCard.family:
                            pF_option.click()

                            # Saving Graphic Card path
                            saveGraphicCard_path(pST_option.get_attribute("text"), pS_option.get_attribute("text"), pF_option.get_attribute("text"))

                            driver_availableToLinux = False
                            for operationSys in browser.find_element(By.XPATH, "//select[@id='selOperatingSystem']").find_elements(By.TAG_NAME, "option"):
                                if operationSys.get_attribute("text").strip() == "Linux 64-bit":
                                    driver_availableToLinux = True
                                    operationSys.click()
                            if driver_availableToLinux:
                                browser.find_element(By.XPATH, "//a[@href='javascript: GetDriver();']").click()
                                driverVersion = browser.find_element(By.XPATH, "//td[@id='tdVersion']").text
                                browser.find_element(By.XPATH, "//a[@id='lnkDwnldBtn']").click()
                                for a in browser.find_elements(By.TAG_NAME, "a"):
                                    if a.get_attribute("href") != None:
                                        if a.get_attribute("href").find("download.nvidia") != -1:
                                            newDriver_path = "https:" + a.get_attribute("href")
                                browser.close()

                                # Comparing installed NVIDIA driver version with website's NVIDIA driver version
                                if driverVersion[:7] == gCard.curVersion:
                                    return "up-to-date"
                                else:
                                    gCard.newDriverPath = newDriver_path
                                    gCard.newVersion = driverVersion[:7]
                                    return gCard
                            else:
                                browser.close()
                                return "no-linux-driver"

def saveGraphicCard_path(pSeriesType, pSeries, pFamily):
    root = os.getcwd()[:os.getcwd().find("/geforce") + 15]

    if not os.path.exists(root + "/data"):
        os.mkdir(root + "/data")

    graphicCard_info = {
        "seriesType" : pSeriesType,
        "series" : pSeries,
        "family" : pFamily
    }

    graphicCard_info_json = json.dumps(graphicCard_info, indent=3)


    with open(root + "/data/gCard.json", "w") as jsonFile:
        jsonFile.write(graphicCard_info_json)

def download_graphicCardDriver(gCard: graphicCard):
    root = os.getcwd()[:os.getcwd().find("/geforce") + 15]

    if not os.path.exists(root + "/downloads"):
        os.mkdir(root + "/downloads")        
    
    gCard_downloadedFileName = gCard.family.replace(" ", "-") + "_" + gCard.newVersion.replace(".", "-") + ".run"

    if os.path.exists(root + "/downloads/" + gCard_downloadedFileName):
        print("\nYou have already downloaded new graphic driver!")
        return gCard_downloadedFileName
    else:
        wget.download(gCard.newDriverPath, root + "/downloads/" + gCard_downloadedFileName)

        if os.path.exists(root + "/downloads/" + gCard_downloadedFileName):
            return gCard_downloadedFileName
        else:
            return "download-fail"

def install_graphicCardDriver(driverFile):
    root = os.getcwd()[:os.getcwd().find("/geforce") + 15]

    os.system(f"sudo ./downloads/{driverFile}")

