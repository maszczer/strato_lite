"""
For local testing purposes
Opens a socket that listens for TCP packets
IP Address = localhost
    Port # = 6001
Strings sent to (localhost, 6001) will be printed to the terminal
"""
import socket

''' Listen for TCP packets on port 6001 '''
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 6001))
    sock.listen(5)
    print("Now listening on port 6001\n")
    client_sock = sock.accept()[0]
    while True:
        data = client_sock.recv(1024)
        if bool(data):
            data = data.decode('utf-8')
            print(data)

if (__name__ == "__main__"):
    main()