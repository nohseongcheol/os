#!/usr/bin/env python3
"""አዘጋጅ_b78e430d 루프백 주소에만 바인딩하는 UDP 시험 አገልጋይ_እሴት. Ctrl+C로 종료한다."""
import argparse
import socket

def ፈጽም_ትእዛዝ():
    ተንትን_እሴት = argparse.ArgumentParser(description='jkoros ተጠቃሚ UDP 예제의 로컬 되돌림 አገልጋይ_እሴት')
    ተንትን_እሴት.add_argument('--port', type=int, default=9000)
    ግቤት_ነጋሪ_እሴት = ተንትን_እሴት.parse_args()
    if not 1 <= ግቤት_ነጋሪ_እሴት.port <= 65535: ተንትን_እሴት.error('ወደብ_እሴት 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as አገልጋይ_እሴት:
        አገልጋይ_እሴት.bind(('127.0.0.1', ግቤት_ነጋሪ_እሴት.port))
        print('UDP 127.0.0.1:{} አዘጋጅ_9ce364fc. Ctrl+C로 ውጣ_ፕሮግራም.'.format(ግቤት_ነጋሪ_እሴት.port), flush=True)
        while True:
            ውሂብ, አቻ_እሴት = አገልጋይ_እሴት.recvfrom(65535)
            አገልጋይ_እሴት.sendto(ውሂብ, አቻ_እሴት)

if __name__ == '__main__':
    try: ፈጽም_ትእዛዝ()
    except KeyboardInterrupt: pass
