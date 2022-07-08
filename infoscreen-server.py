import datetime
import socket
import time
import configparser
from configparser import MissingSectionHeaderError
import psycopg2



server_port = 3125

config = configparser.ConfigParser()
config.sections()
try:
    config.read('db.ini')
except MissingSectionHeaderError:
    print('db.ini not found')

psql_database:str

psql_database = config['DEFAULT']['psql_database']
psql_user = config['DEFAULT']['psql_user']
psql_password = config['DEFAULT']['psql_password']
psql_host = config['DEFAULT']['psql_host']
psql_port = config['DEFAULT']['psql_port']

def psql_test_connection():
    try:
        con = psycopg2.connect(database=psql_database, user=psql_user, password=psql_password, host=psql_host, port=psql_port)
        #print("Database opened successfully")
        con.close()
        return ('success')
    except Exception as e:
        print("Database connection failed, check credentials")
        print(e)
        return ('error')


def start_server(port:int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    print(f'Socket binded to port {port}')
    s.listen(3)
    print('socket is listening')

    while True:
        c, addr = s.accept()
        client_message = str(c.recv(1024))
        client_message = client_message.replace("b'", "")
        client_message = client_message.replace("'", "")
        now = datetime.datetime.now()
        current_time = f'{str(now.hour)}:{str(now.minute)} {now.day}/{now.month}-{now.year}'
        print(f'Got connection from {client_message} ({addr}) at {current_time} and returning info')
        url = get_infoscreen_url(client_message)
        reboot_scheduel = get_reboot_scheduel()
        reboot_next = get_reboot_next()
        c.send(url.encode())
        time.sleep(1)
        c.send(reboot_scheduel.encode())
        time.sleep(1)
        c.send(reboot_next.encode())


        addr = str(addr)
        addr = addr.split(", ")[0]
        addr = addr.replace("'", "")
        addr = addr.replace("(", "")
        vlan = get_vlan(addr)

        if psql_test_connection() == 'success':
            con = psycopg2.connect(database=psql_database, user=psql_user, password=psql_password, host=psql_host,
                                   port=psql_port)
            cursor = con.cursor()
            postgreSQL_select_Query = f"select * from clients where client_name = '{client_message}'"
            cursor.execute(postgreSQL_select_Query)
            client_records = cursor.fetchone()

            if client_records == None:
                try:
                    postgreSQL_insert_Query = f"INSERT INTO clients (client_name, ip_address, last_online, vlan) values ('{client_message}', '{addr}', TIMESTAMP '{datetime.datetime.now()}', {vlan})"
                    cursor.execute(postgreSQL_insert_Query)
                    con.commit()
                except (Exception, psycopg2.Error) as e:
                    print(f'PostgreSQL ({url}): Insert error')
                    print(postgreSQL_insert_Query)
                    print(e)

            elif isinstance(client_records[0], int):
                try:
                    postgreSQL_update_Query = f"UPDATE clients set ip_address = '{addr}', last_online = TIMESTAMP  '{datetime.datetime.now()}', vlan = {vlan} where client_name ='{client_message}'"
                    cursor.execute(postgreSQL_update_Query)
                    con.commit()
                except (Exception, psycopg2.Error) as e:
                    print(f'PostgreSQL({url}): Insert error')
                    print(postgreSQL_update_Query)
                    print(e)
            else:
                print(f"client_records value: {client_records[0]}")
        else:
            print(psql_test_connection())


            cursor.close()
            con.close()
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

def get_vlan(ip_address:str):
    octet_first = int(ip_address.split(".")[0])
    octet_second = int(ip_address.split(".")[1])
    octet_third = int(ip_address.split(".")[2])
    octet_fourth = int(ip_address.split(".")[3])
    location_found = False

    locations = [128,22,19,18,127,126,129,21]

    if octet_first != 10:
        return 405

    for location in locations:
        if octet_second == location:
            location_found = True

    if location_found == False:
        return 406

    vlan = 0
    if 0 <= octet_third < 8:
        vlan = 0
    elif 8 <= octet_third < 16:
        vlan = 8
    elif 16 <= octet_third < 32:
        vlan = 16
    elif 32 <= octet_third < 48:
        vlan = 32
    elif 48 <= octet_third < 64:
        vlan = 48
    elif 64 <= octet_third < 80:
        vlan = 64
    elif 80 <= octet_third < 96:
        vlan = 80
    elif 96 <= octet_third < 104:
        vlan = 96
    elif 104 <= octet_third < 112:
        vlan = 104
    elif 112 <= octet_third < 128:
        vlan = 112
    elif 128 <= octet_third < 144:
        vlan = 128
    elif 144 <= octet_third < 152:
        vlan = 144
    elif 152 <= octet_third < 160:
        vlan = 152
    elif 160 <= octet_third < 176:
        vlan = 160
    elif 176 <= octet_third < 184:
        vlan = 176
    elif 184 <= octet_third < 192:
        vlan = 184
    elif 192 <= octet_third < 208:
        vlan = 192
    elif 208 <= octet_third < 216:
        vlan = 208
    elif 216 <= octet_third < 224:
        vlan = 216
    elif 224 <= octet_third < 240:
        vlan = 224
    elif 240 <= octet_third < 248:
        vlan = 240
    elif 248 <= octet_third < 254:
        vlan = 248
    else:
        vlan = 404

    return vlan


def main():
    psql_test_connection()
    try:
        start_server(server_port)
    except Exception as e:
        print(e)
        time.sleep(6000)
    #print(get_infoscreen_url(socket.gethostname()))

if __name__ == "__main__":
    main()