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
    try:
        if ping_nvidia_website() == "OK":
            print("Updating Graphic Cards database...", end="")
            graphicCard_website = BeautifulSoup(requests.get("https://www.nvidia.com/").text, "html.parser")            

            # Find path to download driver page
            for link in graphicCard_website.find_all("a"):
                if str(link).find("/Download/") != -1:
                    downloadPath_website = str(link.get("href"))
                    break
                elif link == graphicCard_website.find_all("a")[-1]:
                    raise Exception
            
            browser = webdriver.Firefox()
            browser.get(downloadPath_website)

            productSeriesType_list = browser.find_element(By.XPATH, "//select[@name='selProductSeriesType']").find_elements(By.TAG_NAME, "option")
            for pST_option in productSeriesType_list:            
                pST_option.click()
                productSeries_list = browser.find_element(By.XPATH, "//select[@name='selProductSeries']").find_elements(By.TAG_NAME, "option")
                for pS_option in productSeries_list:
                    print(pST_option.get_attribute("text") + "/" + pS_option.get_attribute("text"))
                

            
            browser.close()

            
        else:
            raise Exception
    except:
        print("ERROR")
        return "ERROR"
        
        

get_graphicCard_data()


