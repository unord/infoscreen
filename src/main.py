import sys
from decouple import config
import time
import selenium_tools
import infoscreen
from selenium import webdriver
from _datetime import datetime
import os
import unord_mail
import traceback
from selenium.common.exceptions import WebDriverException
import wmi
import requests

username = config("OFFICE365_USER")
password = config("OFFICE365_PASSWORD")

def call_uptime_kuma(web_address: str):

    try:
        response = requests.get(web_address, verify=False)

        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(e)


def mail_error(e, t):
    mail_subject = f'{infoscreen.get_computer_name()} (Infoscreen Exception): {e}'
    mail_msg = f'traceback.format_exc():\n {t}'

    unord_mail.send_email_with_attachments(config('EMAIL_USER'),
                                   [f'gore@unord.dk'],
                                   mail_subject,
                                   mail_msg,
                                   [],
                                   [],
                                   [])




def refresh_infoscreen_info(driver: webdriver) -> tuple:
    # Get correct infoscreen url and reboot schedule and restart browser every x minutes info
    try:
        url, reboot_schedule, restart_browser_every_minutes, uptime_kuma_url = infoscreen.search_jsonfile_for_computer_name(
            infoscreen.get_computer_name())
        print('We are using the infoscreen.json file')



    except Exception as e:
        url = 'https://unord.dk'
        reboot_schedule = '01:00'
        restart_browser_every_minutes = 60
        uptime_kuma_url = url
        print('We are using the default values')
        print(f'Error: {e}')

    # Try to go infoscreen website
    try:
        driver.get(url)
    except:
        sys.exit()

    return url, reboot_schedule, restart_browser_every_minutes, uptime_kuma_url


def main():

    try:
        counter = 0

        # start browser
        driver = selenium_tools.get_webdriver()

        url, reboot_schedule, restart_browser_every_minutes, uptime_kuma_url = refresh_infoscreen_info(driver)

        while True:

            if not counter == restart_browser_every_minutes:
                counter += 1
                infoscreen.reboot_scheduel(reboot_schedule)

                # if counter diveds by 10
                #if counter % 10 == 0:
                url, reboot_schedule, restart_browser_every_minutes, uptime_kuma_url = refresh_infoscreen_info(driver)

                # Check if we are logged in to Office 365
                selenium_tools.check_office365_login_window(driver, username, password)
                call_uptime_kuma(uptime_kuma_url)
                time.sleep(45)
                counter += 1
            elif counter == restart_browser_every_minutes:
                driver.quit()
                main()

    except WebDriverException as e:
        f = wmi.WMI()
        for process in f.Win32_Process(name="chrome.exe"):
            process.Terminate()
        mail_error(e, traceback.format_exc())
        sys.exit()

    except Exception as e:
        t = traceback.format_exc()
        mail_error(e, t)
        sys.exit()


if __name__ == '__main__':
    print(f'Infoscreen started at {datetime.now()}')
    main()