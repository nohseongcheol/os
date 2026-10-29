#!/usr/bin/env python3
"""hos 루프백 주소에만 바인딩하는 UDP ujian pelayan_VALUE. Ctrl+C로 종료한다."""
import argparse
import socket

def laksanakan_perintah():
    hurai_VALUE = argparse.ArgumentParser(description='jkoros ruang_pengguna UDP 예제의 로컬 kembalikan_penghubung pelayan_VALUE')
    hurai_VALUE.add_argument('--port', type=int, default=9000)
    parameter_argumen = hurai_VALUE.parse_args()
    if not 1 <= parameter_argumen.port <= 65535: hurai_VALUE.error('port_VALUE 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as pelayan_VALUE:
        pelayan_VALUE.bind(('127.0.0.1', parameter_argumen.port))
        print('UDP 127.0.0.1:{} Sediakan. Ctrl+C로 Keluar_aplikasi.'.format(parameter_argumen.port), flush=True)
        while True:
            data, rakan_VALUE = pelayan_VALUE.recvfrom(65535)
            pelayan_VALUE.sendto(data, rakan_VALUE)

if __name__ == '__main__':
    try: laksanakan_perintah()
    except KeyboardInterrupt: pass
