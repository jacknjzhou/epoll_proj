#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import time
import socket
import select
import Queue
import struct
import os
import traceback
#add local info file
import confs

conf_obj = confs.Config('server.ini')

ip = conf_obj.get("SERVER","server.ip","127.0.0.1")
port = conf_obj.get("SERVER","server.port",18888)
if not isinstance(port,int):
  port = int(port)

print "ip:",ip," port:",port

"""
@function:
"""
INFO_STRUCT = '128s1I128s'

#创建socket对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#设置IP地址复用
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#ip地址和端口号
server_address = (ip, port)
#绑定IP地址
serversocket.bind(server_address)
#监听，并设置最大连接数
serversocket.listen(10)
print  "服务器启动成功，监听IP：" , server_address
#服务端设置非阻塞
serversocket.setblocking(False)  
#超时时间
timeout = 100
#创建epoll事件对象，后续要监控的事件添加到其中
epoll = select.epoll()
#注册服务器监听fd到等待读事件集合
epoll.register(serversocket.fileno(), select.EPOLLIN)
#保存连接客户端消息的字典，格式为{}
message_queues = {}
#文件句柄到所对应对象的字典，格式为{句柄：对象}
fd_to_socket = {serversocket.fileno():serversocket}
print "fd socket:",fd_to_socket

#buffer size define
BUFSIZE = 1024*4
filename_queues = {}
while True:
    # time.sleep(1)
    #print "等待活动连接......"
    #轮询注册的事件集合，返回值为[(文件句柄，对应的事件)，(...),....]
    events = epoll.poll(timeout)
    if not events:
        print "epoll超时无活动连接，重新轮询......"
        continue
    #print "有" , len(events), "个新事件，开始处理......"
    #print "events:",events
    for fd, event in events:
        #print 
        socket = fd_to_socket[fd]
        #如果活动socket为当前服务器socket，表示有新连接
        if socket == serversocket:
            connection, address = serversocket.accept()
            print "新连接：" , address
            

            #新连接socket设置为非阻塞
            connection.setblocking(False)
            #注册新连接fd到待读事件集合
            epoll.register(connection.fileno(), select.EPOLLIN)
            #把新连接的文件句柄以及对象保存到字典
            fd_to_socket[connection.fileno()] = connection
            #以新连接的对象为键值，值存储在队列中，保存每个连接的信息
            message_queues[connection]  = Queue.Queue()

            
        #关闭事件
        elif event & select.EPOLLHUP:
            print '连接关闭:',fd
            try:
                print "清理连接信息..."
                #在epoll中注销客户端的文件句柄
                epoll.unregister(fd)
                #关闭客户端的文件句柄
                fd_to_socket[fd].close()
                #在字典中删除与已关闭客户端相关的信息
                del fd_to_socket[fd]
                #del filename_queues[socket]
                #del message_queues[socket]
                filename_queues[socket].close()
            except:
                import traceback
                print traceback.format_exc()
                print "close event error"
                pass
        #可读事件
        elif event & select.EPOLLIN:
            #接收数据
            try:
                if not filename_queues.has_key(socket):
                    FILEINFO_SIZE = struct.calcsize(INFO_STRUCT)
                    data = socket.recv(FILEINFO_SIZE)
                    filename,filesize,destpath = struct.unpack(INFO_STRUCT,data)
                    print filename,":",len(filename)
                    print destpath,":",len(destpath)
                    try:
                        if filename:
                            if destpath and destpath !='.':
                                filename_queues[socket] = open(os.path.join(destpath.strip('\00'),filename.strip('\00')),'wb')
                            else:
                                filename_queues[socket]=open(filename.strip('\00'),'wb')
                        # print "first data"
                        print "ready upload file:",filename," to destpath:",destpath
                    except IOError as e:
                        print "dest path can not write or path not exist,replace destpath to /tmp."
                        destpath = '/tmp'
                        filename_queues[socket] = open(os.path.join(destpath.strip('\00'),filename.strip('\00')),'wb')

                    except Exception as e:
                        print "occure fail."
                        print e
                        try:
                            epoll.unregister(fd)
                            fd_to_socket[fd].close()
                            del fd_to_socket[fd]
                        except:
                            print "clean info error"
                            pass
                        #sys.exit(1)
                    # print len(filename_queues[socket])
                else:
                  pass
                  #print "not first,start recv data."
            except Exception as e:
                print e
                import traceback
                print traceback.format_exc()
                #print "start write data..."
                #print filename_queues[socket]
                #data = socket.recv(1024)
            else:
                try:
                    data = socket.recv(BUFSIZE)
                    if data:
                        print "收到数据长度：" , len(data) , "来自客户端：" , socket.getpeername()
                        #将数据放入对应客户端的字典
                        
                        #filename_queues[socket].write(data)
                        message_queues[socket].put(data)
                        #修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                        epoll.modify(fd, select.EPOLLOUT)
                except Exception as e:
                    print e

        #可写事件
        elif event & select.EPOLLOUT:
            try:
                #从字典中获取对应客户端的信息
                msg = message_queues[socket].get_nowait()
                try:
                    # time.sleep(1)
                    if msg:
                        filename_queues[socket].write(msg)
                        filename_queues[socket].flush()
                    #filename_queues[socket].write(data)
                except:
                    import traceback
                    print traceback.format_exc()

            except Queue.Empty:
                print socket.getpeername() , " queue empty"
                #修改文件句柄为读事件
                epoll.modify(fd, select.EPOLLIN)
            else :
                
                print "发送数据长度：" , len(msg) , "客户端：" , socket.getpeername()
                #发送数据
                # socket.send("over")

#在epoll中注销服务端文件句柄
epoll.unregister(serversocket.fileno())
#关闭epoll
epoll.close()
#关闭服务器socket
serversocket.close()
