#!/usr/bin/env python3
"""தமிழ் 네트워크 예제용 ஓம்பு TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class நடத்தி_இணைப்பு_HTTP_வேண்டுதல்(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);தரவு=bytearray()
                while b'\n' not in தரவு and len(தரவு)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    தரவு.extend(조각)
                수신됨.append(('tcp',bytes(தரவு)));자신.request.sendall(தரவு)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                தரவு,소켓=자신.request;수신됨.append(('udp',தரவு));소켓.sendto(தரவு,자신.client_address)
        자신.இணைப்பு_கட்டுப்பாடு=socketserver.ThreadingTCPServer(('127.0.0.1',டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்),நடத்தி_இணைப்பு_HTTP_வேண்டுதல்)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.இணைப்பு_கட்டுப்பாடு.server_close();raise
        자신.இணைப்பு_கட்டுப்பாடு.daemon_threads=자신.전문제어.daemon_threads=True
        자신.டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்=자신.இணைப்பு_கட்டுப்பாடு.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for சேவையகம்_மதிப்பு in (자신.இணைப்பு_கட்டுப்பாடு,자신.전문제어):
            작업가닥=threading.Thread(target=சேவையகம்_மதிப்பு.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*மதிப்புரு_கோவை):
        for சேவையகம்_மதிப்பு in (자신.இணைப்பு_கட்டுப்பாடு,자신.전문제어):சேவையகம்_மதிப்பு.shutdown();சேவையகம்_மதிப்பு.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    பார்சர்=argparse.ArgumentParser(description=__doc__)
    பார்சர்.add_argument('--tcp-port',type=int,default=9000);பார்சர்.add_argument('--udp-port',type=int,default=9001)
    மதிப்புரு_கோவை=பார்சர்.parse_args()
    with 되돌림서버(மதிப்புரு_கோவை.tcp_port,மதிப்புரு_கோவை.udp_port) as 되돌림서버항목:
        print('ஓம்பு TCP {}, UDP {} தயார்படுத்த. 게스트 முகவரி: 10.0.2.2. முடிவு_நிரல்: Ctrl+C'.format(되돌림서버항목.டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
