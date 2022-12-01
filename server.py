import socket
import select

CMD_MSG   = 'MSG'
CMD_NICK  = 'NICK'
CMD_NAMES = 'NAMES'
CMD_KILL  = 'KILL'
CMD_QUIT  = 'QUIT'

def New(addr : str, port : int):
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
    server_socket.bind((addr, port))
    return server_socket

def Start(server_socket : socket.SocketType, backlog : int):
    print("--Welcome to Chat Server--")
    server_socket.listen(backlog)
    sockets = [server_socket]
    socket_to_nick = {server_socket:"server"}
    while True:
        ready_for_reading_sockets = select.select(sockets, [], [])[0]
        for client_socket in ready_for_reading_sockets:
            if client_socket == server_socket:
                csock, caddr = accept(client_socket, sockets, socket_to_nick)
                log = f"client connected \"{caddr}\"\n"
                send_all([csock, server_socket], log.encode(), sockets)
                print(log, end='')
            else:
                raw_request = client_socket.recv(1500)
                request = raw_request.decode('utf-8')
                if len(raw_request) > 0:
                    if CMD_MSG in request:
                        msg = f"[{socket_to_nick[client_socket]}] "
                        msg += request.removeprefix(f"{CMD_MSG} ")
                        send_all([client_socket, server_socket], msg.encode(), sockets)
                    elif CMD_NAMES in request:
                        msg = f"[{socket_to_nick[server_socket]}] {get_names(socket_to_nick)}\n"
                        send(client_socket, msg.encode())
                    elif CMD_NICK in request:
                        nick = request.removeprefix(f"{CMD_NICK} ").removesuffix('\n')
                        log = f"client \"{socket_to_nick[client_socket]}\" => \"{nick}\""
                        socket_to_nick[client_socket] = nick
                        print(log)
                    elif CMD_KILL in request:
                        to_kill = request.split()[1]
                        msg = f"[{socket_to_nick[client_socket]}] "
                        msg += request.removeprefix(f"{CMD_KILL} {to_kill} ")
                        for i in socket_to_nick:
                            if socket_to_nick[i] == to_kill:
                                sock_to_kill = i
                                break
                        log = f"client disconnected \"{socket_to_nick[sock_to_kill]}\"\n"
                        send(sock_to_kill, msg.encode())
                        disconnect(sock_to_kill, sockets, socket_to_nick)
                        send_all([client_socket, server_socket], log.encode(), sockets)
                        print(log, end='')
                    elif CMD_QUIT in request:
                        msg = f"[{socket_to_nick[client_socket]}] {request.removeprefix('QUIT ')}"
                        log = f"client disconnected \"{socket_to_nick[client_socket]}\""
                        send_all([client_socket, server_socket], msg.encode(), sockets)
                        disconnect(client_socket, sockets, socket_to_nick)
                        print(log)
                else:
                    log = f"client disconnected \"{socket_to_nick[client_socket]}\"\n"
                    send_all([client_socket, server_socket], log.encode(), sockets)
                    disconnect(client_socket, sockets, socket_to_nick)
                    print(log, end='')

def accept(server : socket.SocketType, l : list[socket.SocketType], d : dict[socket.SocketType]):
    new_client = server.accept()
    csock = new_client[0]
    caddr = f"{new_client[1][0]}:{str(new_client[1][1])}"
    l.append(csock)
    d[csock] = caddr
    return csock, caddr

def disconnect(s : socket.SocketType, l : list[socket.SocketType], d : dict[socket.SocketType]):
    d.pop(s)
    l.remove(s)
    s.close()

def get_names(d : dict[socket.SocketType]):
    names = ""
    for s in d:
        names += f"{d[s]} "
    return names

def send(s : socket.SocketType, data : bytes):
    s.sendall(data)

def send_all(ex : list[socket.SocketType], data : bytes, l : list[socket.SocketType]):
    for socket in l:
        met = False
        for e in ex:
            if socket == e:
                met = True
        if not met:
            socket.sendall(data)