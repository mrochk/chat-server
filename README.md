# Chat Server
Simple chat server i did for a college homework.

Runs by default on port 7777.

There is a list of commands that can be used by connected clients :

- **MSG** `<msg>` : Send a message to all connected clients.
- **NICK** `<nick>` : Change client own nickname.
- **NAMES** : Returns the list of all connected clients nicknames if set (otherwise their addr).
- **KILL** `<nick> <msg>` : Disconnect any client from the server by his nickname, after sending them a message.
- **QUIT** : Properly disconnect from the server.
