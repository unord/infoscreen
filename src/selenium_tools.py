from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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

def check_if_text_is_in_page(driver: webdriver, text: str) -> bool:
    try:
        driver.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        return True
    except Exception as e:
        return False


def main():
    pass


if __name__ == '__main__':
    main()
