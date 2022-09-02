from logging.config import valid_ident
from check_update import *

def get_platforms():
    browser = webdriver.Firefox()
    browser.get(get_driverDownloadPage())

    # Available Platforms
    avl_platforms = []

    # Navigating through GC Series Type
    productSeriesType_list = browser.find_element(By.XPATH, "//select[@name='selProductSeriesType']").find_elements(By.TAG_NAME, "option")
    for pST_option in productSeriesType_list:                
        pST_option.click()

        # Navigating through GC Series
        productSeries_list = browser.find_element(By.XPATH, "//select[@name='selProductSeries']").find_elements(By.TAG_NAME, "option")
        for pS_option in productSeries_list:
            if pS_option.get_attribute("class") != "psLess" and pS_option.get_attribute("class") != "psBothHead" and pS_option.get_attribute("class") != "psAll":
                pS_option.click()

                # Navigating through Available Platforms
                platforms_list = browser.find_element(By.XPATH, "//select[@id='selOperatingSystem']").find_elements(By.TAG_NAME, "option")
                for pl_option in platforms_list:
                    if pl_option.get_attribute("text").find("peraciona") == -1:
                        pl_exists = False
                        for pl in avl_platforms:
                            if pl_option.get_attribute("text") == pl:
                                pl_exists = True
                                break
                        if not pl_exists:
                            print(pl_option.get_attribute("text"))
                            avl_platforms.append(pl_option.get_attribute("text"))
    browser.close()
