#!/usr/bin/env python
#-*- coding:utf-8 -*-
import struct
import socket
import os
import sys
"""
@function:采用tcp/epoll方式进行文件上传,并可以指定文件上传路径,指定目标存储路径.
@此处采用struct方式进行序列化编码,然后再svr端进行解码处理

@次序为 filename,filesize,file_destpath
"""

INFO_STRUCT = '128s1I128s'

#创建客户端socket对象
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#服务端IP地址和端口号元组
server_address = ('127.0.0.1',18888)
#客户端连接指定的IP地址和端口号

#filename = "protobuf-2.5.0.tar.gz"
FILEINFO_SIZE = struct.calcsize(INFO_STRUCT)
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
    
dest_path ="/tmp"
#retry connection
clientsocket.connect(server_address)

fhead = struct.pack(INFO_STRUCT,filename,os.stat(filename).st_size,dest_path)
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
