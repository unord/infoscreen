import sys
from decouple import config
import time
import selenium_tools
import infoscreen
from selenium import webdriver
from _datetime import datetime

username = config("OFFICE365_USER")
password = config("OFFICE365_PASSWORD")

def refresh_infoscreen_info(driver: webdriver) -> tuple:
    # Get correct infoscreen url and reboot schedule and restart browser every x minutes info
    try:
        url, reboot_schedule, restart_browser_every_minutes = infoscreen.search_jsonfile_for_computer_name(
            infoscreen.get_computer_name())
        print('We are using the infoscreen.json file')
    except:
        url = 'https://unord.dk'
        reboot_schedule = '01:00'
        restart_browser_every_minutes = 60
        print('We are using the default values')

    # Go to infoscreen website
    try:
        driver.get(url)
    except:
        sys.exit()

    return url, reboot_schedule, restart_browser_every_minutes


def main():
    counter = 0

    # start browser
    try:
        driver = selenium_tools.get_webdriver()
    except Exception as e:
        sys.exit()

    url, reboot_schedule, restart_browser_every_minutes = refresh_infoscreen_info(driver)

    while True:


        if counter != restart_browser_every_minutes:
            counter += 1
            infoscreen.reboot_scheduel(reboot_schedule)

            # if counter diveds by 10
            if counter % 10 == 0:
                url, reboot_schedule, restart_browser_every_minutes = refresh_infoscreen_info(driver)

            # Check if we are logged in to Office 365
            selenium_tools.check_office365_login_window(driver, username, password)
            time.sleep(45)
            counter += 1
        elif counter == restart_browser_every_minutes:
            driver.quit()
            main()


if __name__ == '__main__':
    print(f'Infoscreen started at {datetime.now()}')
    main()