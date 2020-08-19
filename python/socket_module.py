from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
PORT = 51000
MAX_MESSAGE = 2048
NUM_THREAD = 4
 
CHR_CAN = '\18'
CHR_EOT = '\04'

def com_receive():
    #global sock
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind ((HOST, PORT))
    sock.listen (NUM_THREAD)
 　
    while True:
        try:
            conn,addr = sock.accept()
            mess = conn.recv(MAX_MESSAGE).decode('utf-8')
            conn.close()
            if(mess == CHR_EOT):
                break
            
            if(mess == CHR_CAN):
                continue
　　　　　　　
            message('MESSAGE:' + mess)
　　　　
        except:
            print('Error')
　　
    sock.close()