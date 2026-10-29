#!/usr/bin/env python3
"""中文 네트워크 예제용 宿主 TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 回顯服務器列:
    def __init__(自身值,TCP埠=0,UDP埠=0):
        自身值.擁有已接收=[];自身值.執行緒集=[]
        擁有已接收=自身值.擁有已接收
        class 句柄連接狀態申請(socketserver.BaseRequestHandler):
            def handle(自身值):
                自身值.request.settimeout(5);資料=bytearray()
                while b'\n' not in 資料 and len(資料)<=512:
                    片段值=自身值.request.recv(512)
                    if not 片段值:return
                    資料.extend(片段值)
                擁有已接收.append(('tcp',bytes(資料)));自身值.request.sendall(資料)
        class 數據報句柄申請(socketserver.BaseRequestHandler):
            def handle(自身值):
                資料,通訊端值=自身值.request;擁有已接收.append(('udp',資料));通訊端值.sendto(資料,自身值.client_address)
        自身值.連接狀態控制=socketserver.ThreadingTCPServer(('127.0.0.1',TCP埠),句柄連接狀態申請)
        try:自身值.數據報控制=socketserver.ThreadingUDPServer(('127.0.0.1',UDP埠),數據報句柄申請)
        except Exception:自身值.連接狀態控制.server_close();raise
        自身值.連接狀態控制.daemon_threads=自身值.數據報控制.daemon_threads=True
        自身值.TCP埠=自身值.連接狀態控制.server_address[1];自身值.UDP埠=自身值.數據報控制.server_address[1]

    def __enter__(自身值):
        for 服務器值 in (自身值.連接狀態控制,自身值.數據報控制):
            後臺任務=threading.Thread(target=服務器值.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            後臺任務.start();自身值.執行緒集.append(後臺任務)
        return 自身值

    def __exit__(自身值,*實際參數陣列):
        for 服務器值 in (自身值.連接狀態控制,自身值.數據報控制):服務器值.shutdown();服務器值.server_close()
        for 後臺任務 in 自身值.執行緒集:後臺任務.join(timeout=1)


if __name__=='__main__':
    參數解析器=argparse.ArgumentParser(description=__doc__)
    參數解析器.add_argument('--tcp-port',type=int,default=9000);參數解析器.add_argument('--udp-port',type=int,default=9001)
    實際參數陣列=參數解析器.parse_args()
    with 回顯服務器列(實際參數陣列.tcp_port,實際參數陣列.udp_port) as 回顯服務器條目:
        print('宿主 TCP {}, UDP {} 準備. 게스트 地址: 10.0.2.2. 退出程式: Ctrl+C'.format(回顯服務器條目.TCP埠,回顯服務器條目.UDP埠),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
