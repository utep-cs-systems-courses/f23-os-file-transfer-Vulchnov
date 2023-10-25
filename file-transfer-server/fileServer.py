#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)

read = conn.recv(1).decode()
while read != "":
    fNameSize = ""
    fSize = ""
    while read != ":":
        fNameSize = fNameSize + read
        read = conn.recv(1).decode()
    fName = conn.recv(int(fNameSize)).decode()
    outputFile = os.open(fName, os.O_WRONLY | os.O_CREAT)
    read = conn.recv(1).decode()
    while read != ":":
        fSize = fSize + read
        read = conn.recv(1).decode()
    os.write(outputFile, conn.recv(int(fSize)))
    read = conn.recv(1).decode()

conn.shutdown(socket.SHUT_WR)
conn.close()