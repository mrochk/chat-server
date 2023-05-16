# Chat Server
Simple chat server I did for an assignment.

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
*Runs on port 7777 if not argument provided.*