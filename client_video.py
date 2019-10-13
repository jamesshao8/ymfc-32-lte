import socket
import cv2
import threading
import struct
import numpy

addr_port=("139.9.115.114",8003)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(addr_port)

name = addr_port[0]+" Camera"

while True:
    info = struct.unpack("f", sock.recv(4))
    print int(info[0])
    buf_size=int(info[0])
    if buf_size:
        try:
            buf=b""
            temp_buf=buf
            while(buf_size):
                temp_buf=sock.recv(buf_size)
                buf_size-=len(temp_buf)
                buf+=temp_buf
            data = numpy.fromstring(buf, dtype='uint8')
            image = cv2.imdecode(data, 1) 
            cv2.imshow(name, image)  
        except:
            pass
        finally:
            if(cv2.waitKey(10)==27):
                sock.close()
                cv2.destroyAllWindows()
                break
