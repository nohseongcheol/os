#!/usr/bin/env python3
"""ελληνικά 네트워크 예제용 φιλοξενώ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class ηχώ_Διακομιστές:
    def __init__(자신,θύρα_TCP=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class δείκτης_χειρισμού_σύνδεση_αίτηση(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);δεδομένα=bytearray()
                while b'\n' not in δεδομένα and len(δεδομένα)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    δεδομένα.extend(조각)
                수신됨.append(('tcp',bytes(δεδομένα)));자신.request.sendall(δεδομένα)
        class αυτοδύναμο_πακέτο_δείκτης_χειρισμού_αίτηση(socketserver.BaseRequestHandler):
            def handle(자신):
                δεδομένα,υποδοχή_τιμή=자신.request;수신됨.append(('udp',δεδομένα));υποδοχή_τιμή.sendto(δεδομένα,자신.client_address)
        자신.σύνδεση_έλεγχος=socketserver.ThreadingTCPServer(('127.0.0.1',θύρα_TCP),δείκτης_χειρισμού_σύνδεση_αίτηση)
        try:자신.αυτοδύναμο_πακέτο_έλεγχος=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),αυτοδύναμο_πακέτο_δείκτης_χειρισμού_αίτηση)
        except Exception:자신.σύνδεση_έλεγχος.server_close();raise
        자신.σύνδεση_έλεγχος.daemon_threads=자신.αυτοδύναμο_πακέτο_έλεγχος.daemon_threads=True
        자신.θύρα_TCP=자신.σύνδεση_έλεγχος.server_address[1];자신.전문접속번호=자신.αυτοδύναμο_πακέτο_έλεγχος.server_address[1]

    def __enter__(자신):
        for διακομιστής_τιμή in (자신.σύνδεση_έλεγχος,자신.αυτοδύναμο_πακέτο_έλεγχος):
            작업가닥=threading.Thread(target=διακομιστής_τιμή.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*όρισμα_πίνακας):
        for διακομιστής_τιμή in (자신.σύνδεση_έλεγχος,자신.αυτοδύναμο_πακέτο_έλεγχος):διακομιστής_τιμή.shutdown();διακομιστής_τιμή.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    ανάλυση=argparse.ArgumentParser(description=__doc__)
    ανάλυση.add_argument('--tcp-port',type=int,default=9000);ανάλυση.add_argument('--udp-port',type=int,default=9001)
    όρισμα_πίνακας=ανάλυση.parse_args()
    with ηχώ_Διακομιστές(όρισμα_πίνακας.tcp_port,όρισμα_πίνακας.udp_port) as ηχώ_διακομιστής_καταχώρηση:
        print('φιλοξενώ TCP {}, UDP {} Προετοίμασε. 게스트 διεύθυνση: 10.0.2.2. Έξοδος_εφαρμογή: Ctrl+C'.format(ηχώ_διακομιστής_καταχώρηση.θύρα_TCP,ηχώ_διακομιστής_καταχώρηση.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
