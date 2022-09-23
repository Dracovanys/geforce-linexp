from src.check_update import *
import sys

def get_platforms():

    '''
    This function is used to get all platforms
    that NVIDIA have created drivers.
    '''

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

if len(sys.argv) < 2:    
    try:
        ping_nvidia_website("dev")
        print("[SUCCESS] ping_nvidia_website")
    except:
        print("[FAILURE] ping_nvidia_website")
    
    try:
        browser = start_browser("dev")
        print("[SUCCESS] start_browser")
    except:
        print("[FAILURE] start_browser")

    try:
        gCard = find_graphicCardDriver(browser, "dev")
        print("[SUCCESS] find_graphicCardDriver")
    except:
        print("[FAILURE] find_graphicCardDriver")

    try:
        gCard = find_graphicCardDriver_noSaveData(browser, "dev")
        print("[SUCCESS] find_graphicCardDriver_noSaveData")
    except:
        print("[FAILURE] find_graphicCardDriver_noSaveData")
else:
    if sys.argv[1] == "ping_nvidia_website":
        ping_nvidia_website()
    elif sys.argv[1] == "start_browser":
        browser = start_browser()
    elif sys.argv[1] == "find_graphicCardDriver":
        gCard = find_graphicCardDriver(start_browser(), "dev")
    elif sys.argv[1] == "find_graphicCardDriver_noSaveData":
        gCard = find_graphicCardDriver_noSaveData(start_browser())
    elif sys.argv[1] == "get_platforms":
        get_platforms()


    

    



