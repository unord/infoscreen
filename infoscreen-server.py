import socket
import time
import configparser
from configparser import MissingSectionHeaderError



server_port = 3125




def start_server(port:int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    print(f'Socket binded to port {port}')
    s.listen(3)
    print('socket is listening')

    while True:
        c, addr = s.accept()
        print('Got connection from ', addr)
        client_message = str(c.recv(1024))
        client_message = client_message.replace("b'", "")
        client_message = client_message.replace("'", "")
        url = get_infoscreen_url(client_message)
        reboot_scheduel = get_reboot_scheduel()
        reboot_next = get_reboot_next()
        c.send(url.encode())
        time.sleep(1)
        c.send(reboot_scheduel.encode())
        time.sleep(1)
        c.send(reboot_next.encode())

        c.close()


def get_infoscreen_url(computer_name):
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read('config.ini')
    except MissingSectionHeaderError:
        return 'https://historyofyesterday.com/the-history-behind-the-404-error-missing-link-4f8824d63154'

    try:
        this_computer = config['DEFAULT'][computer_name]
    except:
        this_computer = 'https://historyofyesterday.com/the-history-behind-the-404-error-missing-link-4f8824d63154'
    return this_computer

def get_reboot_scheduel():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    try:
        this_scheduel = config['DEFAULT']['REBOOT_SCHEDULE']
    except:
        this_scheduel = 'No reboot time found'
    return this_scheduel

def get_reboot_next():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    this_scheduel = 'ups'
    try:
        this_scheduel = config['DEFAULT']['REBOOT_NEXT']
    except:
        this_scheduel = 'No reboot time found'
    return this_scheduel

def main():
    start_server(server_port)
    #print(get_infoscreen_url(socket.gethostname()))

if __name__ == "__main__":
    main()