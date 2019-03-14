# coding:utf-8
import socket


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> form the5fire 《Django 企业开发实战》 </h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sum, 27 may 2018 01:01:01 GMT',
    'Content-Type: text/html; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)

def handle_connection(conn, addr):
    request = b''
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
        '''
        socket.recv(bufsize[,flags]) 从socket接收数据，返回值是一个代表所接收的数据的字节对象
            一次性接收的最大数据量由bufsize指定，参数flags 通常忽略
        '''
    print(request)
    conn.send(response.encode())   # response 转为 bytes 后传输
    '''
    socket.send(data[,flags]) 将数据发送到socket
        python3中只能发送bytes类型的数据
    '''
    conn.close()
    '''
    关闭scoket
    注：被调用后，连接断开，socket不能再发送数据，连接另一端也将不再接收数据。
     '''

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    '''
    socket.AF_INET 用于服务器与服务器之间的网络通信，
    socket.SOCK_STREAM 用于基于TCP的流式socket通信，
    socket.socket（[family[, type[, proto]]]） 创建套接字,
        family: 套接字家族可以使AF_UNIX 或者AF_INET
            AF_UNIX ------------------- unix本机之间进行通信
            AF_INET ------------------- 使用IPv4
            AF_INET6 ------------------ 使用IPv6
        type: 套接字类型可以根据是面向连接还是非连接分为 SOCK_STREAM(基于TCP）或者SOCK_DGRAM(基于UDP）
            SOCK_STREAM   -------------- TCP套接字类型
            SOCK_DGRAM  ---------------- UDP套接字类型
            SOCK_RAW  ------------------ 原始套接字类型，这个套接字比较强大，创建这种套接字可以监听网卡上所有数据帧
            SOCK_RDM  ------------------ 一种可靠的UDP形式，即保证交付数据报但不保证顺序。
        protocol: 一般不填默认为0      
    '''
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    '''
    在绑定前调用setsockopt 让套接字允许地址重用
    设置端口可复用，保证我们每次按 Ctrl+C 组合键之后，快速重启
    '''
    serversocket.bind(('127.0.0.1', 8000))
    '''
    socket.bind(adress) 将socket绑定到地址（常用于服务端）
        address 地址的格式取决于地址族，在AF_INET下，以元组（host,port）的形式表示地址
    '''
    serversocket.listen(5)
    '''
    # 设置backlog--socket 连接最大排队数量
    socket.listen([backlog]) 启用服务器以接受连接（常用于服务端）
        backlog >= 0 ,指定系统在拒绝新连接之前将允许的未接受连接的数量。如果未指定，则选择默认的合理值
    '''
    print('http://127.0.0.1:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            '''接受一个连接，但前提是socket必须依据绑定了一个地址，再等待连接。
            返回值是一个(conn, address)的值对，这里的conn是一个socket对象，可以用来该送或接收数据。而address是连接另一端绑定的地址。
            socket.getpeername( )函数也能返回该地址。'''
            handle_connection(conn, address)
    finally:
        serversocket.close()
        '''
        关闭scoket
        注：被调用后，连接断开，socket不能再发送数据，连接另一端也将不再接收数据。
        '''


if __name__ == '__main__':
    main()