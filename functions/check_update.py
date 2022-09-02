from ping3 import ping
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import igpu

class graphicCard:
    def __init__(self):
        gpu = igpu.get_device(0)
        self.family = gpu.name.strip().strip("NVIDIA ")
        self.curVersion = ""

        for num in igpu.nvidia_driver_version():
            self.curVersion += str(num)

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
                            driver_availableToLinux = False
                            for operationSys in browser.find_element(By.XPATH, "//select[@id='selOperatingSystem']").find_elements(By.TAG_NAME, "option"):
                                if operationSys.get_attribute("text").strip() == "Linux 64-bit":
                                    driver_availableToLinux = True
                                    operationSys.click()
                            if driver_availableToLinux:
                                browser.find_element(By.XPATH, "//a[@href='javascript: GetDriver();']").click()
                                driverVersion = browser.find_element(By.XPATH, "//td[@id='tdVersion']").text.strip(" .")
                                browser.find_element(By.XPATH, "//a[@id='lnkDwnldBtn']").click()
                                newDriver_path = browser.current_url
                                browser.close()
                                return newDriver_path + " " + driverVersion[:6] + " " + gCard.curVersion
                            else:
                                browser.close()
                                return "No Linux driver"
