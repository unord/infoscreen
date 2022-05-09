# Import socket module
import socket

# Create a socket object
import time

s = socket.socket()

# Define ip

ip = '127.0.0.1'

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
while True:
    try:
        s.connect((ip, port))
        # receive data from the server and decoding to get the string.
        print('trying to connect')
        print(s.recv(1024).decode())
    except:
        time.sleep(60)
        print('Sleeping....')


# close the connection
s.close()
