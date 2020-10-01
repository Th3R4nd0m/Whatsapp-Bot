from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pickle
import time
import os
import requests, json
print("[*] Bot Initialization")

api_key=" 4e01595d6a2a03cb33dae3e416ae0044"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
chromeOptions = Options()
# firefoxOptions.add_argument("--headless") # this is to be enabled after scanning the QR code
check = False
chromeOptions.add_argument("--user-data-dir={0}".format(os.path.expanduser("~/Whatsapp-Bot/data")))

# Initiate GeckoDrivers
while(check == False):
        try:
                driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=chromeOptions)
                print("[*] ChromeDriver has been loaded")
                driver.get("https://web.whatsapp.com/")
                print("[*] Whatsapp Web has been loaded")
                check = True
        except Exception as e:
                print(e)
                print("[*] Error....trying again in 5 seconds....")
                time.sleep(5)


def ClassSelect(obj, name):
        return driver.execute_script("return " + obj + ".getElementsByClassName(\"" + name + "\")")

def InitWhatsapp():
        init = False

        while (True):
            try:
                msgSide = driver.find_element_by_id("side") # Here we check if the side is there ( the chats)
                if (msgSide != None): # if it is, that means the the QR code was scanned
                        return
            except NoSuchElementException:
                    print("Please scan the QR code")
            time.sleep(4)

def SendMsg(mess):
        txtbox = driver.find_element_by_class_name("_3u328")
        txtbox.send_keys(mess)
        txtbox.send_keys(Keys.RETURN)
def CSSselect(obj, what):
        return driver.execute_script("return " + obj + ".querySelectorAll(\"" + what + "\")")

lastMes = ""
def ParseChat(chat):
        # First of all, we need to click on the chat in order to get the messages
        global lastMes
        chat.get_property("offsetParent").click()
        message = driver.execute_script("ms = document.getElementsByClassName(\"message-in\"); return ms[ms.length-1]")
        if (("!ba" in message.text) & (message.text != lastMes)):
                lastMes = message.text
                if ("ora" in message.text):
                        SendMsg("Ora este " + time.strftime("%H:%M:%S", time.gmtime()))
                if("vreme" in message.text):
                        city_name = message.text.split("vreme ")[1] #!ba vreme Barlad
                        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                        response = request.get(complete_url)
                        x = response.json()
                        y = x['main']
                        temperature = y['temp']
                        humidity = y['humidity']
                        SendMsg("Temperatura este " + temperature + " iar umiditatea este de " + humidity)
                else:
                        SendMsg("shhhh......taci")
                
def MessagesListener():
        # So <div class="_2WP9Q"> is where the names are.
        # This "_19RFN _1ovWX _F7Vk" is the name of the chat
        # This "span.P6z4j" is the unread message check
        while (True):
            unreadChats = CSSselect("side", "span.P6z4j")
            global activeChat
            if (len(unreadChats)==0):
                continue
            for i in range(0, len(unreadChats)):
                Chat = unreadChats[i].get_property("offsetParent")
                print("[*] Unread messages @ " + Chat.text.split("\n")[0])
                if (Chat.text.split("\n")[0] == "1"):
                    activeChat = Chat
                    ParseChat(Chat)
            ParseChat(activeChat)
            time.sleep(5)

InitWhatsapp()
MessagesListener()

#content = driver.find_element_by_class_name('content')
