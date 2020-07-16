import socket
import ipget

# AF = IPv4
# TCP/IP SOCK_STREAM

def main():    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # IP adress and port number
        ip = socket.gethostbyname(socket.gethostname() + '.local')
        s.bind((ip, 55555))
        print("Wait Connection")
        # 1 connect
        s.listen(1)
        # Waiting for connection
        while True:
            # When someone comes in, enter the connection and address
            conn, addr = s.accept()
            with conn:
                while True:
                    # receive data
                    data = conn.recv(1024)
                    
                    if not data:
                        break

                    print('data : {}, addr: {}'.format(data, addr))
                    conn.sendall(b'Received: ' + data)

if __name__ == "__main__":

    main()