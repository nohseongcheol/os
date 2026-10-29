#!/usr/bin/env python3
"""ትግርኛ 네트워크 예제용 አዐንግድ TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ሓበሬታ=bytearray()
                while b'\n' not in ሓበሬታ and len(ሓበሬታ)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ሓበሬታ.extend(조각)
                수신됨.append(('tcp',bytes(ሓበሬታ)));자신.request.sendall(ሓበሬታ)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ሓበሬታ,소켓=자신.request;수신됨.append(('udp',ሓበሬታ));소켓.sendto(ሓበሬታ,자신.client_address)
        자신.ርክብ_ቁጽጽር=socketserver.ThreadingTCPServer(('127.0.0.1',ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.ርክብ_ቁጽጽር.server_close();raise
        자신.ርክብ_ቁጽጽር.daemon_threads=자신.전문제어.daemon_threads=True
        자신.ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ=자신.ርክብ_ቁጽጽር.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for ኣገልጋሊ_ዋጋ in (자신.ርክብ_ቁጽጽር,자신.전문제어):
            작업가닥=threading.Thread(target=ኣገልጋሊ_ዋጋ.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*ሓባሪ_ቁጽሪ_ተርታ):
        for ኣገልጋሊ_ዋጋ in (자신.ርክብ_ቁጽጽር,자신.전문제어):ኣገልጋሊ_ዋጋ.shutdown();ኣገልጋሊ_ዋጋ.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    ሓባሪ_ቁጽሪ_ተርታ=인수해석기.parse_args()
    with 되돌림서버(ሓባሪ_ቁጽሪ_ተርታ.tcp_port,ሓባሪ_ቁጽሪ_ተርታ.udp_port) as 되돌림서버항목:
        print('አዐንግድ TCP {}, UDP {} ኣዳልው. 게스트 ኣድራሻ: 10.0.2.2. ውጻእ_መተግበሪ: Ctrl+C'.format(되돌림서버항목.ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
