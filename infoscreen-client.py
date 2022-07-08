import socket
import os
import datetime
import configparser
from configparser import MissingSectionHeaderError
import time

import chrome_browser

#server_ip = "10.127.195.100"
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 3125
client_name = socket.gethostname()

def reboot_computer(seconds:int):
    print('!!!!!!!!! We are rebooting now !!!!!!!!!!!!!!')
    os.system(f"shutdown /r /t {seconds}")


def send_message_to_server(message:str, ip:str, port:int):
    try:
        print(f'Trying to connect to ip {ip} on {port}')
        s = socket.socket()
        try:
            s.connect((ip, port))
        except TimeoutError as e:
            print('Connection failed')
            print(e)
            return "No Connection"
        print('Connection established')
        print('Atempting to send return message')
        z = message
        s.sendall(z.encode())
        print(f'Message sent: {z}')
        print('Trying to get url')
        try:
            server_message = str(s.recv(1024))
        except ConnectionResetError as e:
            print('Connection failed')
            print(e)
            return "No Connection"
        server_message = server_message.replace("b'", "")
        url = server_message.replace("'", "")
        print(f'url: {url}')
        server_message = str(s.recv(1024))
        server_message = server_message.replace("b'", "")
        reboot_scheduel = server_message.replace("'", "")
        print(f'Reboot Scheduel: {reboot_scheduel.replace(",", ", ")}')
        #print(convert_string_to_list(server_message))
        server_message = str(s.recv(1024))
        server_message = server_message.replace("b'", "")
        reboot_next = server_message.replace("'", "")
        print(f'Reboot next: {reboot_next}')
        s.close()
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'URL': url, 'REBOOT_SCHEDULE': reboot_scheduel,  'REBOOT_NEXT': reboot_next}
        with open('infoscreen.ini', 'w') as configfile:
            config.write(configfile)
        return server_message
    except ConnectionRefusedError as e:
        print('Connection failed')
        print(e)
        return "No Connection"

def read_server_commands():
    f = open('infoscreen.txt', 'r')
    if f.mode == 'r':
        contents = f.read()

def save_server_commands(this_url:str, this_reboot_scheduel:list, this_next_reboot):
    input_dictionary = {"url": this_url, "reboot_schedule": this_reboot_scheduel, "next_reboot": this_next_reboot}
    file = open("infoscreen.txt", "w")
    str = repr(input_dictionary)
    file.write("input_dictionary = " + str + "\n")
    file.close()

def reboot_scheduel():
    now = datetime.datetime.now()
    current_time = f'{str(now.hour)}:{str(now.minute)}'
    config = configparser.ConfigParser()
    config.sections()
    config.read('infoscreen.ini')

    try:
        this_scheduel = config['DEFAULT']['reboot_schedule']
    except:
        this_scheduel = 'No reboot time found'

    schedule_list = convert_string_to_list(this_scheduel)

    for item in schedule_list:
        if item == current_time:
            reboot_computer(1)

def reboot_next():
    now = datetime.datetime.now()
    current_time = f'{str(now.hour)}:{str(now.minute)} {now.day}/{now.month}-{now.year}'
    config = configparser.ConfigParser()
    config.sections()
    config.read('infoscreen.ini')
    this_scheduel = 'ups'
    try:
        this_scheduel = config['DEFAULT']['REBOOT_NEXT']
    except:
        this_scheduel = 'No reboot time found'
    if this_scheduel == current_time:
        reboot_computer(1)



def convert_string_to_list(string):
    li = list(string.split(","))
    return li

def get_url(computername):
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('infoscreen.ini')
    except MissingSectionHeaderError as e:
        print(e)
        return 'https://historyofyesterday.com/the-history-behind-the-404-error-missing-link-4f8824d63154'
    try:
        this_computer = config['DEFAULT']['url']
    except:
        this_computer = 'https://historyofyesterday.com/the-history-behind-the-404-error-missing-link-4f8824d63154'
    return this_computer




def main():
    browser = chrome_browser.start_browser()
    send_message_to_server(client_name, server_ip, server_port)
    browser.get(get_url(client_name))
    chrome_browser.check_office365_login_window(browser)
    counter = 0
    while True:
        send_message_to_server(client_name, server_ip, server_port)
        reboot_next()
        reboot_scheduel()
        if counter == 15:
            browser.get(get_url(client_name))
            chrome_browser.check_office365_login_window(browser)
            counter = 0
        counter += 1
        time.sleep(45)




if __name__ == "__main__":
    main()

