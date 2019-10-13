#!/usr/bin/python
# coding=UTF-8
 
import serial
import socket, time
 
serial = serial.Serial('/dev/ttyS0', 9600)
print serial
if serial.isOpen():
   print("open success")
else:
   print("open failed")
 
HOST, PORT = "139.9.115.114", 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
 
while True:
    nextByte = serial.read(50)
    try:
        sock.sendall(nextByte)
    except Exception as ex:
        print "trying reconnect to server"
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except KeyboardInterrupt:
        print "Interrupted"
        if serial != None:
            serial.close()
        sock.close()
        break

