#!/usr/bin/env python3
"""한국어 네트워크 예제용 హోస్ట్ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);డేటా=bytearray()
                while b'\n' not in డేటా and len(డేటా)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    డేటా.extend(조각)
                수신됨.append(('tcp',bytes(డేటా)));자신.request.sendall(డేటా)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                డేటా,소켓=자신.request;수신됨.append(('udp',డేటా));소켓.sendto(డేటా,자신.client_address)
        자신.కనెక్షన్_నియంత్రణ=socketserver.ThreadingTCPServer(('127.0.0.1',ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.కనెక్షన్_నియంత్రణ.server_close();raise
        자신.కనెక్షన్_నియంత్రణ.daemon_threads=자신.전문제어.daemon_threads=True
        자신.ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు=자신.కనెక్షన్_నియంత్రణ.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for సర్వర్_మూల్యం in (자신.కనెక్షన్_నియంత్రణ,자신.전문제어):
            작업가닥=threading.Thread(target=సర్వర్_మూల్యం.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*కారకం_శ్రేణి):
        for సర్వర్_మూల్యం in (자신.కనెక్షన్_నియంత్రణ,자신.전문제어):సర్వర్_మూల్యం.shutdown();సర్వర్_మూల్యం.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    పార్సర్=argparse.ArgumentParser(description=__doc__)
    పార్సర్.add_argument('--tcp-port',type=int,default=9000);పార్సర్.add_argument('--udp-port',type=int,default=9001)
    కారకం_శ్రేణి=పార్సర్.parse_args()
    with 되돌림서버(కారకం_శ్రేణి.tcp_port,కారకం_శ్రేణి.udp_port) as 되돌림서버항목:
        print('హోస్ట్ TCP {}, UDP {} సిద్ధం_చేయు. 게스트 ఇమెయిల్: 10.0.2.2. నిష్క్రమణ_అనువర్తనం: Ctrl+C'.format(되돌림서버항목.ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
