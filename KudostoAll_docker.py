from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule,time
# import time
f= open("log.txt","w+")

def kudos_to_all(username,passowd):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.strava.com/dashboard/following/140")
    elem = driver.find_element_by_name("email")
    elem.send_keys(str(username))
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(str(passowd))
    elem.send_keys(Keys.RETURN)
    time.sleep(8)
    javaScript = "document.querySelectorAll('button.js-add-kudo').forEach(node => node.click())"
    driver.execute_script(javaScript)
    time.sleep(10)
    t = time.localtime()
    current_time = time.strftime("%d/%m/%Y %H:%M:%S", t)
    print("kudos given at "+ current_time)
    pr = "kudos given at "+ current_time
    f.write("kudos given at %s\r\n" %pr)
    driver.close()

username = "" # Strava Username
password = "" # Password
# kudos_to_all(username,password)

# schedule.every().day.at("06:00").do(kudos_to_all,username,password)
schedule.every(3).hours.do(kudos_to_all,username,password)
while True:
    schedule.run_pending()
    time.sleep(1)


