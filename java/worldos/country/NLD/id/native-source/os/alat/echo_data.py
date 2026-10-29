#!/usr/bin/env python3
"""host 루프백 주소에만 바인딩하는 UDP pengujian server_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def Jalankan_perintah():
    urai_VALUE = argparse.ArgumentParser(description='jkoros ruang_pengguna UDP 예제의 로컬 kembalikan_bridge server_VALUE')
    urai_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argumen = urai_VALUE.parse_args()
    if not 1 <= parameter_argumen.port <= 65535: urai_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_VALUE:
        server_VALUE.bind(('127.0.0.1', parameter_argumen.port))
        print('UDP 127.0.0.1:{} Siapkan. Ctrl+C로 Keluar_apl.'.format(parameter_argumen.port), flush=True)
        while True:
            data, serekan_VALUE = server_VALUE.recvfrom(65535)
            server_VALUE.sendto(data, serekan_VALUE)

if __name__ == '__main__':
    try: Jalankan_perintah()
    except KeyboardInterrupt: pass
