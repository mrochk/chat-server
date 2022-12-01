import sys
import server

if __name__ == '__main__':
    ADDR = ""
    try:
        PORT = int(sys.argv[1])
    except:
        PORT = 7777
    s = server.New(ADDR, PORT)
    server.Start(s, 5)