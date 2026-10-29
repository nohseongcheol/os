#!/usr/bin/env python3
"""日本語 네트워크 예제용 ホスト TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 復唱サーバー一覧:
    def __init__(自身値,TCPポート=0,UDPポート=0):
        自身値.保有受信済み=[];自身値.スレッド群=[]
        保有受信済み=自身値.保有受信済み
        class 取扱い接続状態要求(socketserver.BaseRequestHandler):
            def handle(自身値):
                自身値.request.settimeout(5);データ=bytearray()
                while b'\n' not in データ and len(データ)<=512:
                    断片値=自身値.request.recv(512)
                    if not 断片値:return
                    データ.extend(断片値)
                保有受信済み.append(('tcp',bytes(データ)));自身値.request.sendall(データ)
        class データグラム取扱い要求(socketserver.BaseRequestHandler):
            def handle(自身値):
                データ,ソケット値=自身値.request;保有受信済み.append(('udp',データ));ソケット値.sendto(データ,自身値.client_address)
        自身値.接続状態制御=socketserver.ThreadingTCPServer(('127.0.0.1',TCPポート),取扱い接続状態要求)
        try:自身値.データグラム制御=socketserver.ThreadingUDPServer(('127.0.0.1',UDPポート),データグラム取扱い要求)
        except Exception:自身値.接続状態制御.server_close();raise
        自身値.接続状態制御.daemon_threads=自身値.データグラム制御.daemon_threads=True
        自身値.TCPポート=自身値.接続状態制御.server_address[1];自身値.UDPポート=自身値.データグラム制御.server_address[1]

    def __enter__(自身値):
        for サーバー値 in (自身値.接続状態制御,自身値.データグラム制御):
            作業担当=threading.Thread(target=サーバー値.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            作業担当.start();自身値.スレッド群.append(作業担当)
        return 自身値

    def __exit__(自身値,*引数配列):
        for サーバー値 in (自身値.接続状態制御,自身値.データグラム制御):サーバー値.shutdown();サーバー値.server_close()
        for 作業担当 in 自身値.スレッド群:作業担当.join(timeout=1)


if __name__=='__main__':
    引数解析器=argparse.ArgumentParser(description=__doc__)
    引数解析器.add_argument('--tcp-port',type=int,default=9000);引数解析器.add_argument('--udp-port',type=int,default=9001)
    引数配列=引数解析器.parse_args()
    with 復唱サーバー一覧(引数配列.tcp_port,引数配列.udp_port) as 復唱サーバー入口:
        print('ホスト TCP {}, UDP {} 用意. 게스트 番地: 10.0.2.2. 終了点プログラム: Ctrl+C'.format(復唱サーバー入口.TCPポート,復唱サーバー入口.UDPポート),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
