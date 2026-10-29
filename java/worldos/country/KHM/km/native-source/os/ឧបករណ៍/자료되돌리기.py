#!/usr/bin/env python3
"""ហូស 루프백 주소에만 바인딩하는 UDP 시험 ម៉ាស៊ីនមេ_តំលៃ. Ctrl+C로 종료한다."""
import argparse
import socket

def អនុវត្ត_ពាក្យបញ្ជា():
    ញែក_តំលៃ = argparse.ArgumentParser(description='jkoros អ្នកប្រើ UDP 예제의 로컬 되돌림 ម៉ាស៊ីនមេ_តំលៃ')
    ញែក_តំលៃ.add_argument('--port', type=int, default=9000)
    ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ = ញែក_តំលៃ.parse_args()
    if not 1 <= ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.port <= 65535: ញែក_តំលៃ.error('ច្រក_តំលៃ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ម៉ាស៊ីនមេ_តំលៃ:
        ម៉ាស៊ីនមេ_តំលៃ.bind(('127.0.0.1', ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.port))
        print('UDP 127.0.0.1:{} រៀបចំ. Ctrl+C로 ចេញ_កម្មវិធី.'.format(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.port), flush=True)
        while True:
            ទិន្នន័យ, សិទ្ធស្មើ_តំលៃ = ម៉ាស៊ីនមេ_តំលៃ.recvfrom(65535)
            ម៉ាស៊ីនមេ_តំលៃ.sendto(ទិន្នន័យ, សិទ្ធស្មើ_តំលៃ)

if __name__ == '__main__':
    try: អនុវត្ត_ពាក្យបញ្ជា()
    except KeyboardInterrupt: pass
