# epoll_proj
>演示python实现的epoll的简单的文件上传

>增加通过配置的方式进行设置监听的ip和端口
>增加传入文件上传之后的保存路径

>编译成二进制文件方法
>>安装Pyinstaller
>>分别在epoll_cli /epoll_svr目录中执行 pyinstaller e_client.py  / pyinstaller e_svr.py
>>在每个目录中 会生成 dist/build2个目录,
    其中build中有相应名称的执行文件,
    dist中为执行该二进制程序所需要的.so库文件
>>进行发布时需要copy相应的执行文件+so库文件+ini文件,可置于同一目录中,进行启动即可
