#!/usr/bin/env python3
"""한국어 네트워크 예제용 ධාරකය TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);දත්ත=bytearray()
                while b'\n' not in දත්ත and len(දත්ත)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    දත්ත.extend(조각)
                수신됨.append(('tcp',bytes(දත්ත)));자신.request.sendall(දත්ත)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                දත්ත,소켓=자신.request;수신됨.append(('udp',දත්ත));소켓.sendto(දත්ත,자신.client_address)
        자신.සබැඳුම_පාලකය=socketserver.ThreadingTCPServer(('127.0.0.1',සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.සබැඳුම_පාලකය.server_close();raise
        자신.සබැඳුම_පාලකය.daemon_threads=자신.전문제어.daemon_threads=True
        자신.සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට=자신.සබැඳුම_පාලකය.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for සේවාදායකය_අගය in (자신.සබැඳුම_පාලකය,자신.전문제어):
            작업가닥=threading.Thread(target=සේවාදායකය_අගය.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*විස්තාරකය_ආරා_ව):
        for සේවාදායකය_අගය in (자신.සබැඳුම_පාලකය,자신.전문제어):සේවාදායකය_අගය.shutdown();සේවාදායකය_අගය.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    විස්තාරකය_ආරා_ව=인수해석기.parse_args()
    with 되돌림서버(විස්තාරකය_ආරා_ව.tcp_port,විස්තාරකය_ආරා_ව.udp_port) as 되돌림서버항목:
        print('ධාරකය TCP {}, UDP {} පිළියෙල_කරන්න. 게스트 යොමුව: 10.0.2.2. පිටවීම_යෙදු: Ctrl+C'.format(되돌림서버항목.සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
