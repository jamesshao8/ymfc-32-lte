import socket
import threading
import struct
import time
import cv2
import numpy

cap=cv2.VideoCapture(0)
ret=cap.set(3,640)
ret=cap.set(4,480)
img_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]

#sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#sock.bind(("0.0.0.0", 8880))
#sock.listen(2)

#dst, dst_addr = sock.accept()
HOST, PORT = "139.9.115.114", 8002
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


while True:
    ret,img=cap.read()

    img=cv2.resize(img,(640,480))  
    ret,img_encode=cv2.imencode('.jpg',img,img_param) 
    img_code=numpy.array(img_encode)
    img_data=img_code.tostring()
    try:
        print len(img_data)
        sock.sendall(struct.pack("f",len(img_data)))
        sock.sendall(img_data)
    except:
        cap.release()
        break
