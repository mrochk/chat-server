import sys
import server

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 7777
    s = server.New("", port)
    server.Start(s, 5)
