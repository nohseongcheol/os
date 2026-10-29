#!/usr/bin/env python3
"""హోస్ట్ 루프백 주소에만 바인딩하는 UDP 시험 సర్వర్_మూల్యం. Ctrl+C로 종료한다."""
import argparse
import socket

def అమలు_చేయి_ఆదేశం():
    పార్స్_మూల్యం = argparse.ArgumentParser(description='jkoros వినియోగదారు UDP 예제의 로컬 되돌림 సర్వర్_మూల్యం')
    పార్స్_మూల్యం.add_argument('--port', type=int, default=9000)
    పారామీటర్_కారకం = పార్స్_మూల్యం.parse_args()
    if not 1 <= పారామీటర్_కారకం.port <= 65535: పార్స్_మూల్యం.error('పోర్టు_మూల్యం 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as సర్వర్_మూల్యం:
        సర్వర్_మూల్యం.bind(('127.0.0.1', పారామీటర్_కారకం.port))
        print('UDP 127.0.0.1:{} సిద్ధం_చేయు. Ctrl+C로 నిష్క్రమణ_అనువర్తనం.'.format(పారామీటర్_కారకం.port), flush=True)
        while True:
            డేటా, పియర్_మూల్యం = సర్వర్_మూల్యం.recvfrom(65535)
            సర్వర్_మూల్యం.sendto(డేటా, పియర్_మూల్యం)

if __name__ == '__main__':
    try: అమలు_చేయి_ఆదేశం()
    except KeyboardInterrupt: pass
