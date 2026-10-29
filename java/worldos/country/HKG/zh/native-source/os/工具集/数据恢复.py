#!/usr/bin/env python3
"""宿主 루프백 주소에만 바인딩하는 UDP 测试 服务器值. Ctrl+C로 종료한다."""
import argparse
import socket

def 执行命令():
    解析值 = argparse.ArgumentParser(description='jkoros 用户 UDP 예제의 로컬 发回桥接 服务器值')
    解析值.add_argument('--port', type=int, default=9000)
    形参参数 = 解析值.parse_args()
    if not 1 <= 形参参数.port <= 65535: 解析值.error('端口值 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 服务器值:
        服务器值.bind(('127.0.0.1', 形参参数.port))
        print('UDP 127.0.0.1:{} 准备. Ctrl+C로 退出程序.'.format(形参参数.port), flush=True)
        while True:
            数据, 对端值 = 服务器值.recvfrom(65535)
            服务器值.sendto(数据, 对端值)

if __name__ == '__main__':
    try: 执行命令()
    except KeyboardInterrupt: pass
