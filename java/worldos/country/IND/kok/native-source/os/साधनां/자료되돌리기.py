#!/usr/bin/env python3
"""येजमान 루프백 주소에만 바인딩하는 UDP 시험 सर्वर_मोल. Ctrl+C로 종료한다."""
import argparse
import socket

def पाळो_दिवचो_आदेश():
    व्याकरणी_फोडणिशी_मोल = argparse.ArgumentParser(description='jkoros उपेगकर्तो UDP 예제의 로컬 return_ब्रिज सर्वर_मोल')
    व्याकरणी_फोडणिशी_मोल.add_argument('--port', type=int, default=9000)
    인자 = व्याकरणी_फोडणिशी_मोल.parse_args()
    if not 1 <= 인자.port <= 65535: व्याकरणी_फोडणिशी_मोल.error('पोर्ट_मोल 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as सर्वर_मोल:
        सर्वर_मोल.bind(('127.0.0.1', 인자.port))
        print('UDP 127.0.0.1:{} तयार_करचें_9ce364fc. Ctrl+C로 प्रस्थान_करचें_एप्लिकेशन.'.format(인자.port), flush=True)
        while True:
            डेटा, पीयर_मोल = सर्वर_मोल.recvfrom(65535)
            सर्वर_मोल.sendto(डेटा, पीयर_मोल)

if __name__ == '__main__':
    try: पाळो_दिवचो_आदेश()
    except KeyboardInterrupt: pass
