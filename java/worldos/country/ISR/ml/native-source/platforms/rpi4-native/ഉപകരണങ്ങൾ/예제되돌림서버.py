#!/usr/bin/env python3
"""한국어 네트워크 예제용 ഹോസ്റ്റ് TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class കൈകാര്യംചെയ്യല്_കണക്ഷൻ_HTTP_അപേക്ഷ(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ഡാറ്റാ=bytearray()
                while b'\n' not in ഡാറ്റാ and len(ഡാറ്റാ)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ഡാറ്റാ.extend(조각)
                수신됨.append(('tcp',bytes(ഡാറ്റാ)));자신.request.sendall(ഡാറ്റാ)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ഡാറ്റാ,소켓=자신.request;수신됨.append(('udp',ഡാറ്റാ));소켓.sendto(ഡാറ്റാ,자신.client_address)
        자신.കണക്ഷൻ_നിയന്ത്രണം=socketserver.ThreadingTCPServer(('127.0.0.1',ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്),കൈകാര്യംചെയ്യല്_കണക്ഷൻ_HTTP_അപേക്ഷ)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.കണക്ഷൻ_നിയന്ത്രണം.server_close();raise
        자신.കണക്ഷൻ_നിയന്ത്രണം.daemon_threads=자신.전문제어.daemon_threads=True
        자신.ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്=자신.കണക്ഷൻ_നിയന്ത്രണം.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for സെര്_വര്_മൂല്യം in (자신.കണക്ഷൻ_നിയന്ത്രണം,자신.전문제어):
            작업가닥=threading.Thread(target=സെര്_വര്_മൂല്യം.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*ആര്_ഗ്യുമെന്_റ്_അരേ):
        for സെര്_വര്_മൂല്യം in (자신.കണക്ഷൻ_നിയന്ത്രണം,자신.전문제어):സെര്_വര്_മൂല്യം.shutdown();സെര്_വര്_മൂല്യം.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    പാഴ്_സർ=argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ.add_argument('--tcp-port',type=int,default=9000);പാഴ്_സർ.add_argument('--udp-port',type=int,default=9001)
    ആര്_ഗ്യുമെന്_റ്_അരേ=പാഴ്_സർ.parse_args()
    with 되돌림서버(ആര്_ഗ്യുമെന്_റ്_അരേ.tcp_port,ആര്_ഗ്യുമെന്_റ്_അരേ.udp_port) as 되돌림서버항목:
        print('ഹോസ്റ്റ് TCP {}, UDP {} തയ്യാറാക്കുക. 게스트 ഇമെയിൽ: 10.0.2.2. പുറത്തുകടക്കൽ_പ്രോഗ്രാം: Ctrl+C'.format(되돌림서버항목.ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
