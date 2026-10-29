#!/usr/bin/env python3
"""العربية 네트워크 예제용 مضيف TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class ارتداد_خوادم:
    def __init__(자신,TCP_منفذ=0,بروتوكول_مخطط_بيانات_المستخدم_منفذ=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class مؤشر_صديق_طلب(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);بيانات=bytearray()
                while b'\n' not in بيانات and len(بيانات)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    بيانات.extend(조각)
                수신됨.append(('tcp',bytes(بيانات)));자신.request.sendall(بيانات)
        class مخطط_بيانات_مؤشر_طلب(socketserver.BaseRequestHandler):
            def handle(자신):
                بيانات,مأخذ_التوصيل_قيمة=자신.request;수신됨.append(('udp',بيانات));مأخذ_التوصيل_قيمة.sendto(بيانات,자신.client_address)
        자신.صديق_تحكم=socketserver.ThreadingTCPServer(('127.0.0.1',TCP_منفذ),مؤشر_صديق_طلب)
        try:자신.مخطط_بيانات_تحكم=socketserver.ThreadingUDPServer(('127.0.0.1',بروتوكول_مخطط_بيانات_المستخدم_منفذ),مخطط_بيانات_مؤشر_طلب)
        except Exception:자신.صديق_تحكم.server_close();raise
        자신.صديق_تحكم.daemon_threads=자신.مخطط_بيانات_تحكم.daemon_threads=True
        자신.TCP_منفذ=자신.صديق_تحكم.server_address[1];자신.بروتوكول_مخطط_بيانات_المستخدم_منفذ=자신.مخطط_بيانات_تحكم.server_address[1]

    def __enter__(자신):
        for خادم_قيمة in (자신.صديق_تحكم,자신.مخطط_بيانات_تحكم):
            خيطالعمل=threading.Thread(target=خادم_قيمة.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            خيطالعمل.start();자신.작업가닥들.append(خيطالعمل)
        return 자신

    def __exit__(자신,*وسيطة_صفيف):
        for خادم_قيمة in (자신.صديق_تحكم,자신.مخطط_بيانات_تحكم):خادم_قيمة.shutdown();خادم_قيمة.server_close()
        for خيطالعمل in 자신.작업가닥들:خيطالعمل.join(timeout=1)


if __name__=='__main__':
    المحلل=argparse.ArgumentParser(description=__doc__)
    المحلل.add_argument('--tcp-port',type=int,default=9000);المحلل.add_argument('--udp-port',type=int,default=9001)
    وسيطة_صفيف=المحلل.parse_args()
    with ارتداد_خوادم(وسيطة_صفيف.tcp_port,وسيطة_صفيف.udp_port) as ارتداد_خادم_إدخال:
        print('مضيف TCP {}, UDP {} إعداد. 게스트 عنوان: 10.0.2.2. خروج_تطبيق: Ctrl+C'.format(ارتداد_خادم_إدخال.TCP_منفذ,ارتداد_خادم_إدخال.بروتوكول_مخطط_بيانات_المستخدم_منفذ),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
