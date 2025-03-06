# terminal chat

## what is terminal chat?

a custom TCP/IP-based protocol with multi-client-connectivity and server for a chat application.

## learning goals

I wanted to learn basic concepts of network programming:

    * ISO/OSI, endianess+bitwise operations, addressing/routing, ARP, NAT etc.
    * but especially the TCP/IP layer
    * socket programming (in python, for starters)
    * concurrency and buffer management in a networked application

I did not try to encapsulate socket states and operations with object-oriented approaches and just went for utility functions to do the job. 

## properties

* the protocol has the following properties (for now):
    - message format definition and framing using length-prefixed JSON payloads
    - message type system to handle different packet contents
    - defined connection semantics and state management
* client properties:
    - TUI using ANSI
    - multi-threaded I/O (inherently thread-safe)
* server properties:
    - non-blocking sockets using select module
    - multiple network buffers for clients
    - real-time message broadcasting
   
## contributing
