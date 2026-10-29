#!/usr/bin/env python3
"""mwenyeji 루프백 주소에만 바인딩하는 UDP 시험 seva_thamani. Ctrl+C로 종료한다."""
import argparse
import socket

def tekeleza_amri():
    changanua_thamani = argparse.ArgumentParser(description='jkoros mtumiaji UDP 예제의 로컬 되돌림 seva_thamani')
    changanua_thamani.add_argument('--port', type=int, default=9000)
    parameta_hoja = changanua_thamani.parse_args()
    if not 1 <= parameta_hoja.port <= 65535: changanua_thamani.error('kituo_thamani 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as seva_thamani:
        seva_thamani.bind(('127.0.0.1', parameta_hoja.port))
        print('UDP 127.0.0.1:{} Andaa. Ctrl+C로 toka_programu.'.format(parameta_hoja.port), flush=True)
        while True:
            data, kompyuta_rika_thamani = seva_thamani.recvfrom(65535)
            seva_thamani.sendto(data, kompyuta_rika_thamani)

if __name__ == '__main__':
    try: tekeleza_amri()
    except KeyboardInterrupt: pass
