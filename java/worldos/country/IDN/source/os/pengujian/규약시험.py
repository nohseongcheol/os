#!/usr/bin/env python3
"""host libc 없이 연결한 Indonesia C 프로그램을 aktual_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import mesin_virtual

posisi = Path(__file__).resolve().parents[1]

def Jalankan_perintah():
    hasil = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    nomor_port = server_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def echo_balas():
        while not 끝냄.is_set():
            try:
                data, surel = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            server_VALUE.sendto(data, surel)
    일꾼 = threading.Thread(target=echo_balas, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mesin = mesin_virtual(posisi / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    mesin.perintah('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mesin.perintah('run posixudp ' + str(nomor_port), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                jalankan = len(mesin.LOG_baris)
                mesin.직렬.sendall(b'run posixinput\n')
                mesin.tunggu_Status('POSIX INPUT READY', jalankan)
                mesin.직렬.sendall(b'abcdef')
                keluaranTeks = mesin.tunggu_Status('jkoros> ', jalankan)
                assert 'POSIX INPUT PASS' in keluaranTeks and 'Exit: 0' in keluaranTeks, keluaranTeks
                mesin.perintah('javac Hello.java', ['Exit: 0'])
                mesin.perintah('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mesin.perintah('run hello recovered', ['arg: recovered', 'Exit: 0'])
                hasil[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX berkas/공유 posisi/삭제 수명/surel amankan_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mesin.Tutup()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    hasil['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (posisi / 'build/규약시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Jalankan_perintah()
