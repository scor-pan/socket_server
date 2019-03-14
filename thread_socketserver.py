# coding:utf-8


import errno
import socket
import threading
import time


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> from the5fire 《Django 企业开发实战》 </h1> - form {thread_name}'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sun, 27 may 2018 01:01:01 GMT',
    'Content-Type: text/plain: charset=utf-8',
    'Content-Length: {length} \r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    request = b''
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)  

    print(request)
    current_thread = threading.currentThread()
    content_length = len(body.format(thread_name=current_thread.name).encode())
    print(current_thread.name)
    conn.send(response.format(thread_name=current_thread.name,\
              length=content_length).encode())
    conn.close()


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(10)
    print('http://127.0.0.1:8000')
    serversocket.setblocking(0)     # 设置 socket 为非阻塞模式
    '''
    s.setblocking(flag)
    如果flag为0,则将套接字设为非阻塞模式，否则江涛戒子设为阻塞模式（默认值）。
    非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起sockent.error异常
    '''

    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise
                continue
            '''
            在非阻塞模式下，当没有连接可以被接受时，就会抛出EAGAIN错误。
            可以简单理解为此时没有资源（连接）可以使用，所以会抛出错误，这个错误是合理的
            '''
            i += 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address), name='thread-%s'% i)
            t.start()
            '''
            多线程的使用：
            	当通过accept 接受连接之后，就开启一个新的线程来处理这个连接，
            	主程序可以继续在while True循环中处理其他连接
            '''
            '''
            在Web 框架中，异步阻塞是一种很常见的模式
            另外还有一种Web模型，每次接受新请求是，就会产生一个子进程来处理，它跟多线程编程的模式类似
            '''
    finally:
        serversocket.close()

if __name__ == '__main__':
    main()
