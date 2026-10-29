#!/usr/bin/env python3
"""አማርኛ 네트워크 예제용 አዘጋጅ_b78e430d TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ=0,전문접속번호=0):
        자신.수신됨=[];자신.작업가닥들=[]
        수신됨=자신.수신됨
        class 연결요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ውሂብ=bytearray()
                while b'\n' not in ውሂብ and len(ውሂብ)<=512:
                    조각=자신.request.recv(512)
                    if not 조각:return
                    ውሂብ.extend(조각)
                수신됨.append(('tcp',bytes(ውሂብ)));자신.request.sendall(ውሂብ)
        class 전문요청처리(socketserver.BaseRequestHandler):
            def handle(자신):
                ውሂብ,소켓=자신.request;수신됨.append(('udp',ውሂብ));소켓.sendto(ውሂብ,자신.client_address)
        자신.ግንኙነት_ቁጥጥር=socketserver.ThreadingTCPServer(('127.0.0.1',የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ),연결요청처리)
        try:자신.전문제어=socketserver.ThreadingUDPServer(('127.0.0.1',전문접속번호),전문요청처리)
        except Exception:자신.ግንኙነት_ቁጥጥር.server_close();raise
        자신.ግንኙነት_ቁጥጥር.daemon_threads=자신.전문제어.daemon_threads=True
        자신.የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ=자신.ግንኙነት_ቁጥጥር.server_address[1];자신.전문접속번호=자신.전문제어.server_address[1]

    def __enter__(자신):
        for አገልጋይ_እሴት in (자신.ግንኙነት_ቁጥጥር,자신.전문제어):
            작업가닥=threading.Thread(target=አገልጋይ_እሴት.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            작업가닥.start();자신.작업가닥들.append(작업가닥)
        return 자신

    def __exit__(자신,*ነጋሪ_እሴት_ድርድር):
        for አገልጋይ_እሴት in (자신.ግንኙነት_ቁጥጥር,자신.전문제어):አገልጋይ_እሴት.shutdown();አገልጋይ_እሴት.server_close()
        for 작업가닥 in 자신.작업가닥들:작업가닥.join(timeout=1)


if __name__=='__main__':
    አግልሎ_ማስቀመጥ=argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ.add_argument('--tcp-port',type=int,default=9000);አግልሎ_ማስቀመጥ.add_argument('--udp-port',type=int,default=9001)
    ነጋሪ_እሴት_ድርድር=አግልሎ_ማስቀመጥ.parse_args()
    with 되돌림서버(ነጋሪ_እሴት_ድርድር.tcp_port,ነጋሪ_እሴት_ድርድር.udp_port) as 되돌림서버항목:
        print('አዘጋጅ_b78e430d TCP {}, UDP {} አዘጋጅ_9ce364fc. 게스트 አድራሻ: 10.0.2.2. ውጣ_ፕሮግራም: Ctrl+C'.format(되돌림서버항목.የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ,되돌림서버항목.전문접속번호),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
