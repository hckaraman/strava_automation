from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import schedule,time
import requests
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.mime.application
import datetime
import yaml,os

path = r'.'

with open('strava.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)


activity_time = []
# activity_time.append('2019-11-07 07:55:13 UTC')
activity_time.append('2019-11-09 04:26:54 UTC')
# yapma dur
yapma_dur = "https://www.strava.com/athletes/164421"
# doos abi
doos_abi = "https://www.strava.com/athletes/2196185"

def commnet(url,activity_time):
    # response = requests.get('https://api.chucknorris.io/jokes/random')
    response = requests.get('http://api.icndb.com/jokes/random?firstName=Yapma&amp;lastName=Dur')
    # response = requests.get('http://api.icndb.com/jokes/random?firstName=Doos')
    text = response.json()['value']['joke']

    # text = response.json()['value']

    username = data['mail']  # Strava Username
    password = data['password']  # Password
    driver = webdriver.Chrome("chromedriver.exe")  # Path to chrome webdriver
    driver.get("https://www.strava.com/dashboard/following/140")
    elem = driver.find_element_by_name("email")
    elem.send_keys(str(username))
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(str(password))
    elem.send_keys(Keys.RETURN)
    time.sleep(15)

    driver.get(url)
    activity_control,activity_time = gettime(activity_time,driver)

    if activity_control == False:
        try:
            driver.find_element_by_xpath("//button[@class='add-comment btn btn-default btn-xs empty']").click()
            e = driver.find_element_by_xpath("//textarea")
            e.send_keys(text)
            time.sleep(15)
            driver.find_element_by_xpath("//button[@class='text-footnote btn btn-default btn-xs compact']").click()
        except NoSuchElementException:
            e = driver.find_element_by_xpath("//textarea")
            e.send_keys(text)
            time.sleep(15)
            driver.find_element_by_xpath("//button[@class='text-footnote btn btn-default btn-xs compact']").click()
        print("new activity found at " + activity_time[-1] + " commented",activity_time)
        mail(activity_time[-1])
    else:
        print("No new activity",activity_time)
    driver.close()

def gettime(activity_time,driver):
    e = driver.find_elements_by_xpath("//time[@class='timestamp']")

    time = []
    for i in range(e.__len__()):
        if e[i].get_attribute("datetime") != None:
            time.append(e[i].get_attribute("datetime"))

    time.sort()
    new_activity_time = time[-1]
    last_activity_time = activity_time[-1]
    compare = last_activity_time == new_activity_time
    if compare == True:
        pass
    else:
        activity_time.append(new_activity_time)

    return compare,activity_time

    first_time = time[-2]
    last_time = time[-1]


def mail(time):
    smtp_server = data['mail_server']
    port = 587  # For starttls
    sender_email = data['mail_user']
    password = data['mail_passwd']

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(data['mail_user'], data['mail_passwd'])

        msg = MIMEMultipart()
        msg['Subject'] = "New activity from Yapma Dur abi at " + time
        msg['From'] = data['mail_from']
        msg['To'] = data['mail']
        text = "Yapma Dur abi uploaded new activity at " + time
        txt = MIMEText(text)
        msg.attach(txt)
        server.send_message(msg, data['mail_from'], [data['mail'],data['mail_to']])
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        print("Mail sent")
        server.quit()

# commnet(yapma_dur,activity_time)

# schedule.every(1).minutes.do(commnet,doos_abi,activity_time)
schedule.every().hour.do(commnet,yapma_dur,activity_time)

while True:
    schedule.run_pending()
    time.sleep(1)
