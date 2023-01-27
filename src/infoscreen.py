import json
import os
import datetime

infoscreen_jsonfile = 'H:\infoscreen\src\infoscreens.json'


def get_computer_name() -> str:
    # Get computer name
    return os.environ['COMPUTERNAME']


def reboot_computer(seconds:int) -> None:
    # Reboot computer
    print('!!!!!!!!! We are rebooting now !!!!!!!!!!!!!!')
    os.system(f"shutdown /r /t {seconds}")


def int_less_than_10(number: int) -> str:
    # If number is less than 10, add a 0 in front of it
    if number < 10:
        return f'0{number}'
    else:
        return str(number)


def reboot_scheduel(list_of_times: list) -> None:
    # Reboot computer at a specific time
    now = datetime.datetime.now()
    current_time = f'{int_less_than_10(now.hour)}:{int_less_than_10(now.minute)}'
    # print(f'Current time: {current_time}, Reboot schedule: {list_of_times}')
    for item in list_of_times:
        if item == current_time:
            reboot_computer(10)


def search_jsonfile_for_computer_name(computer_name: str) -> tuple:
    # Search json file for computer name
    with open(infoscreen_jsonfile, 'r') as f:
        data = json.load(f)
    infoscreens = data['infoscreens']
    for computer in infoscreens:
        if computer['computer_name'] == computer_name:
            return computer['infoscreen_url'], computer['reboot_schedule'], computer['restart_browser_every_minutes'], computer['uptime_kuma_url']


def main():
    while True:
        # Get correct infoscreen url and reboot schedule and restart browser every x minutes info
        try:
            url, reboot_scheduel, restart_browser_every_minutes  = search_jsonfile_for_computer_name('UN-HDV-INFO-02')
        except:
            url = 'https://unord.dk'
            reboot_scheduel = '01:00'
            restart_browser_every_minutes = 60









        print(url, reboot_scheduel, restart_browser_every_minutes)



if __name__ == '__main__':
    main()
