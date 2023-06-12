# Chat Server
A simple IRC-like chat server I made for a college assignment.

List of commands that can be used:
- **MSG** `<msg>`: Send a message to all connected clients.
- **NICK** `<name>`: Change nickname.
- **NAMES**: Return the list of all connected client's nickname (if set, otherwise their address).
- **KILL** `<name> <msg>`: Disconnect a client from the server by his nickname, after sending him a message.
- **QUIT**: Quit the server.

Usage:
```
python3 main.py <port>
```