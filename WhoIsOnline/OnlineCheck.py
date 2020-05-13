from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time

def get_driver_handle():
    driver = webdriver.Chrome("..\\chromedriver.exe")
    driver.get("https://web.whatsapp.com")

    return driver

def open_chat(driver, name = "Gayatri Suslade", delay = 3):
    # Clicking on new chat button
    # Single Element of chat button
    new_chat_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
        By.XPATH, "//div[@class='_3Kxus ba6sz']//span//div[@class = 'rAUz7'][2]//div")))
    new_chat_button.click()

    #Click on Serach ( To search by name )
    search_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
        By.XPATH, "//div[@class='_2S1VP copyable-text selectable-text']")))
    search_element.click()
    search_element.send_keys(name)

    while True:
        try:
            user_element = driver.find_elements_by_xpath(
                '//div[@class="_1vDUw _2sNbV"]//div//div//div[@class="_21sW0 _1ecJY"]//div[@class = "_2wP_Y"]//div[@class="_2EXPL"]')[0]
            time.sleep(1)
            user_element.click()
            break
        except Exception as e:
            pass


def check_online_status(driver, delay=3):
    #status_element = driver.find_elements_by_xpath('//span[@class="O90ur _3FXB1"]')[0]
    while True:
        try:
            status_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                (By.XPATH, '//span[@class="O90ur _3FXB1"]')))
            if "online" in status_element.text:
                return True
            elif "click here" in status_element.text:
                pass
            else:
                return False
        except TimeoutException:
            return False
        except:
            return False


def write_a_message(message, delay = 3):
    print("write function is called")
    message_element = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, '//footer//div[@class = "_2S1VP copyable-text selectable-text"]')))
    message_element.click()
    message_element.send_keys(message)
    message_element.send_keys(Keys.ENTER)


chats_to_checks = list(filter(None,open("accountToCheck.txt").read().split("\n")))

print("All Chats to check -->")
print(chats_to_checks)

log_files_path = "OnlineLog\\"
log_files_handle = {}
current_online_status = {}
for c in chats_to_checks:
    log_files_handle[c] = log_files_path + c + ".txt"
    current_online_status[c] = False

driver = get_driver_handle()
print("Scan QR Code, And then Enter")
input()
print("Logged In")
while True:
    for k, v in log_files_handle.items():
        try:
            open_chat(driver, k)
            online_status = check_online_status(driver, delay = 1)
            print(k, online_status)
            t = time.localtime()
            current_time = time.strftime("%d-%m-%Y %H:%M:%S", t)
            f = open(v, 'a')
            if online_status:
                f.write(current_time + " online\n")
            else:
                f.write(current_time + " offline\n")
                current_online_status[k] = False
            f.close()

            if (k == 'Gayatri Suslade') and online_status:
                if current_online_status[k] == False:
                    write_a_message(k + ":: online activity detected at your account")
                    current_online_status[k] = True
        except:
            print("Some Error with window")
