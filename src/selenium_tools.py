from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import time


def get_webdriver() -> webdriver:
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--kiosk')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except:
        driver_path = ChromeDriverManager("114.0.5735.90").install()
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
    return driver

def scroll_to_bottom(driver: webdriver) -> dict:

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

    return {'msg': 'Scrolled to bottom', 'success': True}


def check_office365_login_window(driver, office_user: str, office_password: str) -> None:
    time.sleep(5)  # sleep for 5 seconds
    try:
        input_username = driver.find_element("name", "loginfmt")
        try:
            input_username.send_keys(Keys.F11)
        except Exception as e:
            driver.refesh()
            print(f'Detected exception: {e}')
            print('Waiting 30 seconds and trying again')
            time.sleep(30)
            print('Trying to send keys again')
            input_username.send_keys(Keys.F11)
        input_username = driver.find_element("name", "loginfmt")
        input_username.send_keys(office_user)
    except NoSuchElementException as e:
        print(f'No such element: {e}')
        return e
    except StaleElementReferenceException as e:
        print(f'Stale element: {e}')
        return e

    next_button = driver.find_element("id", 'idSIButton9')
    next_button.click()
    time.sleep(5)
    try:
        input_username = driver.find_element("name", "passwd")
        input_username.send_keys(office_password)
    except NoSuchElementException as e:
        return e

    next_button = driver.find_element("id", 'idSIButton9')
    next_button.click()
    time.sleep(5)
    try:
        next_button = driver.find_element("id", 'idSIButton9')
        next_button.click()
    except NoSuchElementException as e:
        return e

def check_if_text_is_in_page(driver: webdriver, text_to_search: str) -> bool:

    # Get the HTML of the page
    html = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Search for the desired text
    text = soup.find(text=text_to_search)

    # Check if the text was found
    result = True if text else False

    return result


def main():
    pass


if __name__ == '__main__':
    main()
