#!/usr/bin/env python3
"""宿主 루프백 주소에만 바인딩하는 UDP 測試 服務器值. Ctrl+C로 종료한다."""
import argparse
import socket

def 執行命令():
    解析值 = argparse.ArgumentParser(description='jkoros 使用者 UDP 예제의 로컬 發回橋接 服務器值')
    解析值.add_argument('--port', type=int, default=9000)
    形式參數實際參數 = 解析值.parse_args()
    if not 1 <= 形式參數實際參數.port <= 65535: 解析值.error('埠值 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 服務器值:
        服務器值.bind(('127.0.0.1', 形式參數實際參數.port))
        print('UDP 127.0.0.1:{} 準備. Ctrl+C로 退出程式.'.format(形式參數實際參數.port), flush=True)
        while True:
            資料, 對端值 = 服務器值.recvfrom(65535)
            服務器值.sendto(資料, 對端值)

if __name__ == '__main__':
    try: 執行命令()
    except KeyboardInterrupt: pass
