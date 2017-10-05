#!/usr/bin/env python
#-*- coding:utf-8 -*-
import struct
import socket
import os
import sys

#创建客户端socket对象
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#服务端IP地址和端口号元组
server_address = ('127.0.0.1',18888)
#客户端连接指定的IP地址和端口号

#filename = "protobuf-2.5.0.tar.gz"
FILEINFO_SIZE = struct.calcsize('128s1I')
BUFSIZE =1024

#输入数据
filename = raw_input('please input upload filename:')

if os.path.exists(filename):
    pass
else:
    print "input filename [%s] not exist" %(filename,)
    if clientsocket:
        clientsocket.close()
    sys.exit(1)
    
#retry connection
clientsocket.connect(server_address)

fhead = struct.pack('128s1I',filename,os.stat(filename).st_size)
clientsocket.send(fhead)
#print type(fhead)

fp = open(filename,'rb')

while 1:
    data = fp.read(BUFSIZE)
    # data  = "dafaf"
    if not data:
        break
    #客户端发送数据
    clientsocket.send(data)
fp.close()
#客户端接收数据
#server_data = clientsocket.recv(1024)


#print '客户端收到的数据长度：',len(server_data)
    #关闭客户端socket
clientsocket.close() 
