#!/usr/bin/env python3
"""ಹೋಸ್ಟ್ 루프백 주소에만 바인딩하는 UDP 시험 ಸರ್ವರ್_ಮೌಲ್ಯ. Ctrl+C로 종료한다."""
import argparse
import socket

def ಪೂರೈಸು_ಆದೇಶ():
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ = argparse.ArgumentParser(description='jkoros ಬಳಕೆದಾರ UDP 예제의 로컬 되돌림 ಸರ್ವರ್_ಮೌಲ್ಯ')
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('--port', type=int, default=9000)
    ಪ್ಯಾರಾಮೀಟರ್_ವಾದ = ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.parse_args()
    if not 1 <= ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.port <= 65535: ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.error('ಪೋರ್ಟ್_ಮೌಲ್ಯ 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ಸರ್ವರ್_ಮೌಲ್ಯ:
        ಸರ್ವರ್_ಮೌಲ್ಯ.bind(('127.0.0.1', ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.port))
        print('UDP 127.0.0.1:{} ಸಿದ್ಧಪಡಿಸು. Ctrl+C로 ನಿರ್ಗಮನ_ಅಪ್ಲಿ.'.format(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.port), flush=True)
        while True:
            ಡೇಟಾ, ಪೀರ್_ಮೌಲ್ಯ = ಸರ್ವರ್_ಮೌಲ್ಯ.recvfrom(65535)
            ಸರ್ವರ್_ಮೌಲ್ಯ.sendto(ಡೇಟಾ, ಪೀರ್_ಮೌಲ್ಯ)

if __name__ == '__main__':
    try: ಪೂರೈಸು_ಆದೇಶ()
    except KeyboardInterrupt: pass
