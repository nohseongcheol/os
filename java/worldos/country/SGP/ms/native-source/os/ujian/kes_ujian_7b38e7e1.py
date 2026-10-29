#!/usr/bin/env python3
"""hos libc 없이 연결한 Melayu C 프로그램을 sebenar_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from ujian_pengguna_rangkaian import mesin_maya

Kedudukan = Path(__file__).resolve().parents[1]

def laksanakan_perintah():
    ukuran = {}
    pelayan_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pelayan_VALUE.bind(('127.0.0.1', 0))
    pelayan_VALUE.settimeout(0.1)
    nombor_port = pelayan_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, e_mel = pelayan_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            pelayan_VALUE.sendto(data, e_mel)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mesin = mesin_maya(Kedudukan / ('build/kernel.' + 종류), 종류)
            try:
                for lelaran_VALUE in range(2):
                    mesin.Perintah('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mesin.Perintah('run posixudp ' + str(nombor_port), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Jalan = len(mesin.LOG_baris)
                mesin.직렬.sendall(b'run posixinput\n')
                mesin.keadaan_tunggu('POSIX INPUT READY', Jalan)
                mesin.직렬.sendall(b'abcdef')
                출력 = mesin.keadaan_tunggu('jkoros> ', Jalan)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                mesin.Perintah('javac Hello.java', ['Exit: 0'])
                mesin.Perintah('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mesin.Perintah('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ukuran[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fail/공유 Kedudukan/삭제 수명/e_mel lindung_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mesin.Tutup()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); pelayan_VALUE.close()
    ukuran['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (Kedudukan / 'build/kes_ujian_7b38e7e1.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    laksanakan_perintah()
