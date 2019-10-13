#!/usr/bin/python
# coding=UTF-8
 
import socket, time, threading, sys
 
sock_quadcopter = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_quadcopter.bind(("0.0.0.0", 8000))
sock_quadcopter.listen(2)
 
sock_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_client.bind(("0.0.0.0", 8001))
sock_client.listen(2)
 
sock_quadcopter.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

src = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
dst = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

quadcopter = 0
client = 0


class quadcopter_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global src, quadcopter
        while self.running:
            try:
                src, src_addr = sock_quadcopter.accept()
                print "Source Connected by", src_addr
                quadcopter = quadcopter + 1
            except Exception as ex:
                    print "1: ", sys.exc_info()
                    print ex

    def stop(self):
        self.running = False
  

class client_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global dst, client
        while self.running:
            try:
                dst, dst_addr = sock_client.accept()
                print "Destination Connected by", dst_addr
                client = client + 1
            except Exception as ex:
                    print "2: ", sys.exc_info()
                    print ex

    def stop(self):
        self.running = False

class transfer_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def run(self):
        global src, quadcopter
        global dst, client
        while self.running:
            if quadcopter >= 1 and client >= 1:
                try:
                    msg = src.recv(50)
                    if not msg:
                        print "lost quad signal"
                        quadcopter = quadcopter - 1
                    dst.sendall(msg)
                except Exception as ex:
                    print "lost client "
                    #print "3: lost client ", sys.exc_info()
                    client = client - 1
                    print ex

    def stop(self):
        self.running = False

if __name__ == "__main__":
    quad_t = quadcopter_thread()
    quad_t.start()
    client_t = client_thread()
    client_t.start()
    transfer_t = transfer_thread()
    transfer_t.start()

    while True:
        try:
            print quadcopter, client
            time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted"
            quad_t.stop()
            client_t.stop()
            transfer_t.stop()  
            src.close()
            dst.close()
            sock_quadcopter.close()
            sock_client.close()
            quad_t.join()
            client_t.join()
            transfer_t.join()
            break
 

