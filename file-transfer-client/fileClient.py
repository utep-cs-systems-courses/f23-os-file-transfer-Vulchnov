#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

while 1:
    print("Enter command followed by file name, send or pull")
    line = input()
    split = line.split()
    if(split[0]=="send"):
        for fileName in split:
            if(fileName != "send"):
                inputFile = os.open(fileName, os.O_RDONLY)
                file_size = os.path.getsize(fileName)
                byte = str(len(fileName))+":"+fileName
                byte = byte.encode()
                while len(byte):
                    print("sending '%s'" % byte.decode())
                    bytesSent = os.write(s.fileno(), byte)
                    byte = byte[bytesSent:]
                byte = str(file_size)+":"
                byte = byte.encode()
                while len(byte):
                    print("sending '%s'" % byte.decode())
                    bytesSent = os.write(s.fileno(), byte)
                    byte = byte[bytesSent:]
                print("Recived confirmation")
                os.write(s.fileno(), os.read(inputFile, file_size))
                os.write(s.fileno(), b"")
                os.close(inputFile)
    if(split[0]=="stop"):
        break


s.shutdown(socket.SHUT_WR) 
s.close()