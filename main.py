import sys
from server import Server

if __name__ == '__main__':
    backlog = 5
    addr    = ''

    try: port    = int(sys.argv[1])
    except: port = 7777

    server = Server(addr, port)
    server.start(backlog)