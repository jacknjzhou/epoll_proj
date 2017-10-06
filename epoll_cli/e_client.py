#!/usr/bin/env python
#-*- coding:utf-8 -*-
import struct
import socket
import os
import sys
import getopt
"""
@function:采用tcp/epoll方式进行文件上传,并可以指定文件上传路径,指定目标存储路径.
@此处采用struct方式进行序列化编码,然后再svr端进行解码处理

@次序为 filename,filesize,file_destpath
"""
#add local info file
import confs

conf_obj = confs.Config('server.ini')

ip = conf_obj.get("SERVER","server.ip","127.0.0.1")
port = conf_obj.get("SERVER","server.port",18888)
if not isinstance(port,int):
  port = int(port)

print "ip:",ip," port:",port


INFO_STRUCT = '128s1I128s'

#创建客户端socket对象
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#服务端IP地址和端口号元组
server_address = (ip,port)
#客户端连接指定的IP地址和端口号

#filename = "protobuf-2.5.0.tar.gz"
FILEINFO_SIZE = struct.calcsize(INFO_STRUCT)
BUFSIZE =1024*4

#采用支持的命令行方法进行输入参数(采用命令参数的方式进行输入上传的文件+路径)
r_argv = sys.argv[1:]

if not r_argv:
    print "输入的参数为空."
    sys.exit(1)
try:
    opts, args = getopt.getopt(r_argv,"hu:p:",["uploadfile","destpath"])
    print "***"*10
    print opts
    print "***"*10
    print args
except getopt.GetoptError as e:
    print e
    print traceback.format_exc()
    print "Error: script.py -u <uploadfile> -p <destpath>"
    print "Error: script.py --uploadfile <uploadfile> --destpath <destpaht>"
    sys.exit(2)

filename = None
dest_path = None

for opt,arg in opts:
    if opt == '-h':
        print "Error: script.py -u <uploadfile> -p <destpaht>"
        print "Error: script.py --uploadfile <uploadfile> --destpath <destpaht>"
        sys.exit(1)
    if opt in ('-u','--uploadfile'):
        filename = arg

    if opt in ('-p','--destpath'):
        dest_path = arg

print "filename:",filename
print "destpath:",dest_path

#输入数据
# filename = raw_input('please input upload filename:')

if os.path.exists(filename):
    pass
else:
    print "input filename [%s] not exist" %(filename,)
    sys.exit(1)

if dest_path is None:
    dest_path ="/tmp"

base_filename = os.path.basename(filename)
print "basename:",base_filename
#retry connection
clientsocket.connect(server_address)

fhead = struct.pack(INFO_STRUCT,base_filename,os.stat(filename).st_size,dest_path)
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
