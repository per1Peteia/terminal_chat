# multi user chat client and server

## TODO

* this is a chronological stepthrough of the process

* first i need to set up a basic client-server connectivity
    - this means:
        - [x]non-blocking sockets using select, serverside
        - [x] OS i/o to parse commandline arguments

* client-side 
    - then i need to make sure the hello paket gets sent
        - every client that connects needs to send this first always
    - the provided TUI handles double-threaded I/O
        - every line the user types gets send to the server as chat paket
        - every paket (chat, connect, disconnect) the client gets is shown in OUT
    - client input starting with '/' has special meaning and needs to be parsed further
        - '/q' should mean the client exits --> client sends empty bstr to server (b'')
            - this leads to the server removing the client from the select set
            - which means it will no longer have an open connection

* server-side
    - then i can look at sending a first message to the server
        - and make sure it arrives and is complete
            - question: do i need to do tcp validation?
    - the server needs to handle multi-client streams with multiple buffers
        - use a dict that maps client sockets to client network buffers
    - if the server recieves a message, it needs to rebroadcast it to all the other clients
        - the select set is the indicator for what clients are currently connected
    - when a new client (dis-)connects the server broadcasts that to all clients as well


