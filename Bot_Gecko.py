from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle
import time

print("[*] Bot Initialization")


firefoxOptions = Options()
profile = FirefoxProfile("data/")
# firefoxOptions.add_argument("--headless") # this is to be enabled after scanning the QR code
firefoxOptions.profile = profile
check = False

# Initiate GeckoDrivers
while(check == False):
        try:
                #driver = webdriver.Firefox(executable_path=r'./geckodriver', options = firefoxOptions, firefox_profile=profile)
                driver = webdriver.Firefox(executable_path = r'./geckodriver', firefox_profile = profile)
                print("[*] Geckodriver has been loaded")
                check = True
        except Exception as e:
                print(e)
                print("[*] Error....trying again in 5 seconds....")
                time.sleep(5)


def ClassSelect(obj, name):
        return driver.execute_script("return " + obj + ".getElementsByClassName(\"" + name + "\")")

def InitWhatsapp():
        init = False
        try:
            cookies = pickle.load(open("cookies", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
        except FileNotFoundError:
            print("[*] The cookies file doesn't exist")

        # We initiate Whatsapp Web here in order to get the the cookies right
        driver.get("https://web.whatsapp.com/")
        print("[*] Whatsapp Web has been loaded")
        time.sleep(3)

        while (True):
            try:
                msgSide = driver.find_element_by_id("side") # Here we check if the side is there ( the chats)
                if (msgSide != None): # if it is, that means the the QR code was scanned
                        break
            except NoSuchElementException:
                    print("Please scan the QR code")
            time.sleep(4)
        time.sleep(6)
        pickle.dump(driver.get_cookies(), open("cookies", "wb"))

def SendMsg(mess):
        txtbox = driver.find_element_by_class_name("_3u328")
        txtbox.send_keys(mess)
        txtbox.send_keys(Keys.RETURN)
def CSSselect(obj, what):
        return driver.execute_script("return " + obj + ".querySelectorAll(\"" + what + "\")")


def MessagesListener():
        # So <div class="_2WP9Q"> is where the names are.
        # This "_19RFN _1ovWX _F7Vk" is the name of the chat
        # This "span.P6z4j" is the unread message check
        while (True):
            unreadChats = CSSselect("side", "span.P6z4j")
            if (len(unreadChats)==0):
                continue
            for i in range(0, len(unreadChats)):
                ChatName = unreadChats[i].get_property("offsetParent").text.split("\n")[0]
                print("[*] Unread messages @ " + ChatName)
                time.sleep(5)

InitWhatsapp()
MessagesListener()

#content = driver.find_element_by_class_name('content')
