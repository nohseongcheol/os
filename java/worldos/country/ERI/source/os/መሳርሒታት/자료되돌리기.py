#!/usr/bin/env python3
"""አዐንግድ 루프백 주소에만 바인딩하는 UDP 시험 ኣገልጋሊ_ዋጋ. Ctrl+C로 종료한다."""
import argparse
import socket

def ተግብር_ትእዛዝ():
    해석 = argparse.ArgumentParser(description='jkoros ተጠቃሚ UDP 예제의 로컬 되돌림 ኣገልጋሊ_ዋጋ')
    해석.add_argument('--port', type=int, default=9000)
    인자 = 해석.parse_args()
    if not 1 <= 인자.port <= 65535: 해석.error('ወደብ_ዋጋ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ኣገልጋሊ_ዋጋ:
        ኣገልጋሊ_ዋጋ.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} ኣዳልው. Ctrl+C로 ውጻእ_መተግበሪ.'.format(인자.port), flush=True)
        while True:
            ሓበሬታ, መዘና_ዋጋ = ኣገልጋሊ_ዋጋ.recvfrom(65535)
            ኣገልጋሊ_ዋጋ.sendto(ሓበሬታ, መዘና_ዋጋ)

if __name__ == '__main__':
    try: ተግብር_ትእዛዝ()
    except KeyboardInterrupt: pass
