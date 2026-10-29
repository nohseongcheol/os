#!/usr/bin/env python3
"""中文 네트워크 예제용 宿主 TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 回显服务器列:
    def __init__(自身值,TCP端口=0,UDP端口=0):
        自身值.拥有已接收=[];自身值.线程集=[]
        拥有已接收=自身值.拥有已接收
        class 句柄连接状态申请(socketserver.BaseRequestHandler):
            def handle(自身值):
                自身值.request.settimeout(5);数据=bytearray()
                while b'\n' not in 数据 and len(数据)<=512:
                    片段值=自身值.request.recv(512)
                    if not 片段值:return
                    数据.extend(片段值)
                拥有已接收.append(('tcp',bytes(数据)));自身值.request.sendall(数据)
        class 数据报句柄申请(socketserver.BaseRequestHandler):
            def handle(自身值):
                数据,套接字值=自身值.request;拥有已接收.append(('udp',数据));套接字值.sendto(数据,自身值.client_address)
        自身值.连接状态控制=socketserver.ThreadingTCPServer(('127.0.0.1',TCP端口),句柄连接状态申请)
        try:自身值.数据报控制=socketserver.ThreadingUDPServer(('127.0.0.1',UDP端口),数据报句柄申请)
        except Exception:自身值.连接状态控制.server_close();raise
        自身值.连接状态控制.daemon_threads=自身值.数据报控制.daemon_threads=True
        自身值.TCP端口=自身值.连接状态控制.server_address[1];自身值.UDP端口=自身值.数据报控制.server_address[1]

    def __enter__(自身值):
        for 服务器值 in (自身值.连接状态控制,自身值.数据报控制):
            后台任务=threading.Thread(target=服务器值.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            后台任务.start();自身值.线程集.append(后台任务)
        return 自身值

    def __exit__(自身值,*参数数组):
        for 服务器值 in (自身值.连接状态控制,自身值.数据报控制):服务器值.shutdown();服务器值.server_close()
        for 后台任务 in 自身值.线程集:后台任务.join(timeout=1)


if __name__=='__main__':
    参数解析器=argparse.ArgumentParser(description=__doc__)
    参数解析器.add_argument('--tcp-port',type=int,default=9000);参数解析器.add_argument('--udp-port',type=int,default=9001)
    参数数组=参数解析器.parse_args()
    with 回显服务器列(参数数组.tcp_port,参数数组.udp_port) as 回显服务器条目:
        print('宿主 TCP {}, UDP {} 准备. 게스트 地址: 10.0.2.2. 退出程序: Ctrl+C'.format(回显服务器条目.TCP端口,回显服务器条目.UDP端口),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
