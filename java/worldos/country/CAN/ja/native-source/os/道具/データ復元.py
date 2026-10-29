#!/usr/bin/env python3
"""ホスト 루프백 주소에만 바인딩하는 UDP 試験 サーバー値. Ctrl+C로 종료한다."""
import argparse
import socket

def 命令実行():
    値解析 = argparse.ArgumentParser(description='jkoros 利用者 UDP 예제의 로컬 復帰橋渡し サーバー値')
    値解析.add_argument('--port', type=int, default=9000)
    仮引数引数 = 値解析.parse_args()
    if not 1 <= 仮引数引数.port <= 65535: 値解析.error('ポート値 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as サーバー値:
        サーバー値.bind(('127.0.0.1', 仮引数引数.port))
        print('UDP 127.0.0.1:{} 用意. Ctrl+C로 終了点プログラム.'.format(仮引数引数.port), flush=True)
        while True:
            データ, 通信相手値 = サーバー値.recvfrom(65535)
            サーバー値.sendto(データ, 通信相手値)

if __name__ == '__main__':
    try: 命令実行()
    except KeyboardInterrupt: pass
