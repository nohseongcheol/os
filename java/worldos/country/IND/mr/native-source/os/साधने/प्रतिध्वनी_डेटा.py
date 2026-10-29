#!/usr/bin/env python3
"""होस्ट 루프백 주소에만 바인딩하는 UDP चाचण्या सर्व्हर_मूल्य. Ctrl+C로 종료한다."""
import argparse
import socket

def आज्ञा_कार्यवाही_करा():
    मूल्य_पार्स_करा = argparse.ArgumentParser(description='jkoros प्रयोक्ता UDP 예제의 로컬 परतकरा_ब्रिज सर्व्हर_मूल्य')
    मूल्य_पार्स_करा.add_argument('--port', type=int, default=9000)
    परिमापन_वितर्क = मूल्य_पार्स_करा.parse_args()
    if not 1 <= परिमापन_वितर्क.port <= 65535: मूल्य_पार्स_करा.error('पॉर्ट_मूल्य 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as सर्व्हर_मूल्य:
        सर्व्हर_मूल्य.bind(('127.0.0.1', परिमापन_वितर्क.port))
        print('UDP 127.0.0.1:{} तयार_करणे. Ctrl+C로 निर्गमन_करा_अनुप्रयोग.'.format(परिमापन_वितर्क.port), flush=True)
        while True:
            डेटा, समकक्ष_मूल्य = सर्व्हर_मूल्य.recvfrom(65535)
            सर्व्हर_मूल्य.sendto(डेटा, समकक्ष_मूल्य)

if __name__ == '__main__':
    try: आज्ञा_कार्यवाही_करा()
    except KeyboardInterrupt: pass
