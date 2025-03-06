# multi user chat client and server

## TODO

this is a stepthrough of the process.

* first i need to set up a basic client-server connectivity
    - this means:
        - [x]   non-blocking sockets using select, serverside
        - [x]   OS i/o to parse commandline arguments

* client-side 
    - [x] then i need to make sure the hello paket gets sent
        - [x] make a build_hello_packet util
        - [x] send it to server
        - [x] write a get_next_packet() util function to recv data streams server-side
            - i opted out of te get_next_packet() architecture
            - i now use process_socket_buffer(), which will not block and
            will round-robin process other buffers when they have complete packets
    - [x] the provided TUI handles double-threaded I/O
        - this is threading in a nutshell:
        - main threat is prompting (sending messages to the server)
        - worker threat is receiving server data (join, leave, messages)

        ```python
        import threading

        # I need a runner function, it will be the 'target' of a spawned thread
        
        THREAD_COUNT = n    # how many threads maximum
        
        threads = []        # keep track of existing threads      
        
        for i in range(THREAD_COUNT):
            # spawn threads with:
            t = threading.Thread(target=some_function, args=(func_arg, ...))

            t.start()           # this starts the thread
            threads.append(t)   # keep track of existing threads

        for t in threads:
            t.join()            # joins the existing threads to the calling (main) thread
        ```
    
    - sending messages will require a send_message() utility function
        - [] the sending client needs to also print this message to it's own TUI
    - [x] client input starting with '/' has special meaning and needs to be parsed further
        - [x] '/q' should mean the client exits --> client sends empty bstr to server (b'')
            - this leads to the server removing the client from the select set
            - which means it will no longer have an open connection
    - packet-handling logic:
        - [x] is the same as the server-side packet handling and parsing
        - I modified the process_socket_buffer() function to handle both:
            - server multi network buffer (as a dict)
            - client single network buffer (as a bytestr)

* server-side
    - then i can look at sending a first packet to the server
    - [x] the server needs to handle multi-client streams with multiple buffers
        - [x] use a dict that maps client sockets to client network buffers
    - packet-handling logic:
        - when a client connects to the server, the server needs to broadcast this to the clients
            - [x] use a broadcast_connect() function 
        - if the server recieves a message from a client, it needs to rebroadcast it to all the other clients
            - the select set is the indicator for what clients are currently connected
            - [] use a broadcast_message() function
        - when a new client (dis-)connects the server broadcasts that to all clients as well
            - [x] ise a broadcast_disconnect() function
            - [] this dc broadcast needs to be represented in the client-side TUI


