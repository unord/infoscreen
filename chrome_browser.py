import time
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import urllib
from urllib import request
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import platform
import sys
import datetime
from decouple import config



currentSite = "https://unord.dk"
win_path = "c:/Chrome"
chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"


def win_download_and_unzip(chromedriver_version_url:str, extract_to='.'):
    download_url:str

    file = urllib.request.urlopen(chromedriver_version_url)
    for line in file:
        decoded_line = line.decode("utf-8")
        download_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(decoded_line)

    http_response = urlopen(download_url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

def start_browser():
    # Loading webdriver

    osDetect = platform.system() #Check to see if system is windows or osx
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('--kiosk')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('disable-infobars')
    if osDetect == "Darwin": #osx

        browser = webdriver.Chrome(executable_path="/Applications/Chromedriver", options=options)

    else: #windows

        try:
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
        except SessionNotCreatedException:
            win_download_and_unzip(chromedriver_version_url, win_path)
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
        except WebDriverException:
            win_download_and_unzip(chromedriver_version_url, win_path)
            browser = webdriver.Chrome(executable_path="C:\\Chrome\\Chromedriver.exe", options=options)
    time.sleep(3)
    browser.get('https://unord.dk')
    return browser

def check_office365_login_window(browser):
    time.sleep(5)
    try:
        input_username = browser.find_element_by_name("loginfmt")
        input_username.send_keys(Keys.F11)
        input_username = browser.find_element_by_name("loginfmt")
        input_username.send_keys(config('OFFICE365_USER'))
    except NoSuchElementException as e:
        return e

    next_button = browser.find_element_by_id('idSIButton9')
    next_button.click()
    time.sleep(5)
    try:
        input_username = browser.find_element_by_name("passwd")
        input_username.send_keys(config('OFFICE365_PASSWORD'))
    except NoSuchElementException as e:
        return e

    next_button = browser.find_element_by_id('idSIButton9')
    next_button.click()
    time.sleep(5)
    try:
        next_button = browser.find_element_by_id('idSIButton9')
        next_button.click()
    except NoSuchElementException as e:
        return e


    return browser




if __name__ == "__main__":
    # execute only if run as a script

    try:
        browser = start_browser()
        browser.get(currentSite)
        print("Browser connection worked")
        time.sleep(10)
        browser.close()
    except:
        print("Something went wrong")