import socket
import ipget
import argparse
import irrp

# AF = IPv4
# TCP/IP SOCK_STREAM

def main():
    ir_remote_control = irrp.IrRemoteControl(args)
    
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
                    ir_remote_control.ir_playback(args)
                    if not data:
                        break

                    print('data : {}, addr: {}'.format(data, addr))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("-p", "--play",   help="play keys",   action="store_true")
    g.add_argument("-r", "--record", help="record keys", action="store_true")
    p.add_argument("-g", "--gpio", help="GPIO for RX/TX", required=True, type=int)
    p.add_argument("-f", "--file", help="Filename",       required=True)
    p.add_argument('-id', nargs='+', type=str, help='IR codes')
    p.add_argument("--freq",      help="frequency kHz",   type=float, default=38.0)
    p.add_argument("--gap",       help="key gap ms",        type=int, default=100)
    p.add_argument("--glitch",    help="glitch us",         type=int, default=100)
    p.add_argument("--post",      help="postamble ms",      type=int, default=15)
    p.add_argument("--pre",       help="preamble ms",       type=int, default=200)
    p.add_argument("--short",     help="short code length", type=int, default=10)
    p.add_argument("--tolerance", help="tolerance percent", type=int, default=15)
    p.add_argument("-v", "--verbose", help="Be verbose",     action="store_true")
    p.add_argument("--no-confirm", help="No confirm needed", action="store_true")

    args = p.parse_args()

    main()