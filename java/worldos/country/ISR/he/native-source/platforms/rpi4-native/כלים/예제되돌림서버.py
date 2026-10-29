#!/usr/bin/env python3
"""עברית 네트워크 예제용 ארח TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class הד_שרתים:
    def __init__(자신,יציאת_TCP=0,פרוטוקול_יחידת_נתונים_של_משתמש_הסב=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class נקודת_אחיזה_קשר_בקשה(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);נתונים=bytearray()
                while b'\n' not in נתונים and len(נתונים)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    נתונים.extend(조각)
                수신됨.append(('tcp',bytes(נתונים)));자신.request.sendall(נתונים)
        class יחידת_נתונים_נקודת_אחיזה_בקשה(socketserver.BaseRequestHandler):
            def handle(자신):
                נתונים,소켓=자신.request;수신됨.append(('udp',נתונים));소켓.sendto(נתונים,자신.client_address)
        자신.קשר_פקד=socketserver.ThreadingTCPServer(('127.0.0.1',יציאת_TCP),נקודת_אחיזה_קשר_בקשה)
        try:자신.יחידת_נתונים_פקד=socketserver.ThreadingUDPServer(('127.0.0.1',פרוטוקול_יחידת_נתונים_של_משתמש_הסב),יחידת_נתונים_נקודת_אחיזה_בקשה)
        except Exception:자신.קשר_פקד.server_close();raise
        자신.קשר_פקד.daemon_threads=자신.יחידת_נתונים_פקד.daemon_threads=True
        자신.יציאת_TCP=자신.קשר_פקד.server_address[1];자신.פרוטוקול_יחידת_נתונים_של_משתמש_הסב=자신.יחידת_נתונים_פקד.server_address[1]

    def __enter__(자신):
        for שרת_ערך in (자신.קשר_פקד,자신.יחידת_נתונים_פקד):
            משימתרקע=threading.Thread(target=שרת_ערך.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            משימתרקע.start();자신.작업가닥들.append(משימתרקע)
        return 자신

    def __exit__(자신,*ארגומנט_מערך):
        for שרת_ערך in (자신.קשר_פקד,자신.יחידת_נתונים_פקד):שרת_ערך.shutdown();שרת_ערך.server_close()
        for משימתרקע in 자신.작업가닥들:משימתרקע.join(timeout=1)


if __name__=='__main__':
    מנתח=argparse.ArgumentParser(description=__doc__)
    מנתח.add_argument('--tcp-port',type=int,default=9000);מנתח.add_argument('--udp-port',type=int,default=9001)
    ארגומנט_מערך=מנתח.parse_args()
    with הד_שרתים(ארגומנט_מערך.tcp_port,ארגומנט_מערך.udp_port) as הד_שרת_ערך:
        print('ארח TCP {}, UDP {} להכין. 게스트 למען: 10.0.2.2. יציאה_תוכנית: Ctrl+C'.format(הד_שרת_ערך.יציאת_TCP,הד_שרת_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
