from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule,time
import yaml,os

path = r'.'

def kudos_to_all(username,passowd):
    driver = webdriver.Chrome("chromedriver.exe")  # Path to chrome webdriver
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
    time.sleep(60)
    driver.close()


with open('strava.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

username = data['mail']
password = data['password']

schedule.every().hour.do(kudos_to_all,username,password)
while True:
    schedule.run_pending()
    time.sleep(1)