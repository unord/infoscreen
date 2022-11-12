from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--kiosk')


    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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
    time.sleep(5)
    try:
        input_username = driver.find_element("name", "loginfmt")
        input_username.send_keys(Keys.F11)
        input_username = driver.find_element("name", "loginfmt")
        input_username.send_keys(office_user)
    except NoSuchElementException as e:
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


def main():
    pass


if __name__ == '__main__':
    main()
