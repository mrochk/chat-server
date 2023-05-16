import socket
import select

class Server:
    __CMD_MSG = "MSG"
    __CMD_NICK = "NICK"
    __CMD_NAMES = "NAMES"
    __CMD_KILL = "KILL"
    __CMD_QUIT = "QUIT"

    def __init__(self, address, port):
        """
        Attributes:
            socket: The server socket.
            sockets: List of client's sockets.
            sockets_to_addr: Dict matching sockets to a string "addr:port".
        """
        self.__socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.__socket.bind((address, port))

    def __accept(self):
        clientsocket, clientaddr = self.__socket.accept()
        address = f"{clientaddr[0]}:{str(clientaddr[1])}"
        self.__sockets.append(clientsocket)
        self.__sockets_to_addr[clientsocket] = address
        return clientsocket, address

    def __disconnect(self, client):
        self.__sockets_to_addr.pop(client)
        self.__sockets.remove(client)
        client.close()

    def __get_names(self):
        names = ""
        for socket in self.__sockets_to_addr:
            names += f"{self.__sockets_to_addr[socket]} "
        return names

    def __send(self, client, data):
        client.sendall(data)

    def __send_all(self, excluded, data):
        for socket in self.__sockets:
            met = False
            for ex in excluded:
                if socket == ex:
                    met = True
            if not met:
                socket.sendall(data)

    def __handle_new(self):
        clientsock, clientaddr = self.__accept()
        log = f'client connected "{clientaddr}"\n'
        self.__send_all([clientsock, self.__socket], log.encode())
        print(log, end="")

    def __handle_message(self, client, request):
        msg = f"[{self.__sockets_to_addr[client]}] "
        msg += request.removeprefix(f"{self.__CMD_MSG} ")
        self.__send_all([client, self.__socket], msg.encode())

    def __handle_names(self, client):
        msg = f"[{self.__sockets_to_addr[self.__socket]}] {self.__get_names()}\n"
        self.__send(client, msg.encode("utf-8"))

    def __handle_nickname(self, client, request):
        nick = request.removeprefix(f"{self.__CMD_NICK} ").removesuffix("\n")
        log = f'client "{self.__sockets_to_addr[client]}" => "{nick}"'
        self.__sockets_to_addr[client] = nick
        print(log)

    def __handle_kill(self, client, request):
        tokill = request.split()[1]
        msg = f"[{self.__sockets_to_addr[client]}] "
        msg += request.removeprefix(f"{self.__CMD_KILL} {tokill} ")
        for socket in self.__sockets_to_addr:
            if self.__sockets_to_addr[socket] == tokill:
                sock_to_kill = socket
                break
        log = f'client disconnected "{self.__sockets_to_addr[sock_to_kill]}"\n'
        self.__send(sock_to_kill, msg.encode())
        self.__disconnect(sock_to_kill)
        self.__send_all([client, self.__socket], log.encode())
        print(log, end="")

    def __handle_quit(self, client, request):
        msg = f"[{self.__sockets_to_addr[client]}] {request.removeprefix('QUIT ')}"
        log = f'client disconnected "{self.__sockets_to_addr[client]}"'
        self.__send_all([client, self.__socket], msg.encode())
        self.__disconnect(client)
        print(log)

    def __handle_lostconn(self, client):
        log = f'client disconnected "{self.__sockets_to_addr[client]}"\n'
        self.__send_all([client, self.__socket], log.encode())
        self.__disconnect(client)
        print(log, end="")

    def start(self, backlog):
        print("((( Starting Server )))")

        self.__socket.listen(backlog)
        self.__sockets = [self.__socket]
        self.__sockets_to_addr = {self.__socket: "server"}

        while True:
            ready_sockets = select.select(self.__sockets, [], [])[0]
            for socket in ready_sockets:
                if socket == self.__socket:
                    self.__handle_new()
                else:
                    raw_request = socket.recv(1500)
                    request = raw_request.decode("utf-8")
                    if len(raw_request) > 0:
                        if self.__CMD_MSG in request:
                            self.__handle_message(socket, request)
                        elif self.__CMD_NAMES in request:
                            self.__handle_names(socket)
                        elif self.__CMD_NICK in request:
                            self.__handle_nickname(socket, request)
                        elif self.__CMD_KILL in request:
                            self.__handle_kill(socket, request)
                        elif self.__CMD_QUIT in request:
                            self.__handle_quit(socket, request)
                    else:
                        self.__handle_lostconn(socket)
