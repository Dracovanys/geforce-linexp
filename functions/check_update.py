from ping3 import ping
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def ping_nvidia_website():
    print("Checking connection with NVIDIA Website...", end="")
    try:
        pingResult = ping("www.nvidia.com")
        if pingResult == None or pingResult == False:
            raise Exception
        else:
            print("OK")
            return "OK"       
    except:
        print("ERROR")
        return "ERROR"

def get_graphicCard_data():
    if ping_nvidia_website() == "OK":
        print("Updating Graphic Cards database...", end="")
        graphicCard_website = BeautifulSoup(requests.get("https://www.nvidia.com/").text, "html.parser")            

        # Find path to download driver page
        for link in graphicCard_website.find_all("a"):
            if str(link).find("/Download/") != -1:
                downloadPath_website = str(link.get("href"))
                break
            elif link == graphicCard_website.find_all("a")[-1]:
                print("ERROR")
        
        browser = webdriver.Firefox()
        browser.get(downloadPath_website)

        productSeriesType_list = browser.find_element(By.XPATH, "//select[@name='selProductSeriesType']").find_elements(By.TAG_NAME, "option")
        for pST_option in productSeriesType_list:                
            pST_option.click()
            productSeries_list = browser.find_element(By.XPATH, "//select[@name='selProductSeries']").find_elements(By.TAG_NAME, "option")
            for pS_option in productSeries_list:
                if pS_option.get_attribute("class") != "psLess" and pS_option.get_attribute("class") != "psBothHead" and pS_option.get_attribute("class") != "psAll":
                    pS_option.click()
                    if browser.find_element(By.XPATH, "//tr[@id='trProductFamily']").get_attribute("style") != "display: none;":
                        productFamily_list = browser.find_element(By.XPATH, "//select[@name='selProductFamily']").find_elements(By.TAG_NAME, "option")
                        for pF_option in productFamily_list:
                            print(pST_option.get_attribute("text").strip() + "/" + pS_option.get_attribute("text").strip() + "/" + pF_option.get_attribute("text").strip())
                    else:
                        print(pST_option.get_attribute("text").strip() + "/" + pS_option.get_attribute("text").strip())
        browser.close()        
    else:
        print("ERROR")

get_graphicCard_data()


