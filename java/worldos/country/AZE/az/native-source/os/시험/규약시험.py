#!/usr/bin/env python3
"""host libc 없이 연결한 한국어 C 프로그램을 faktiki_verilənlər ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtual_maşın

yerinə_qoymaq = Path(__file__).resolve().parents[1]

def icra_etmək_əmr():
    ölçü = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    접속번호 = server_VALUE.getsockname()[1]
    RECEIVED_verilənlər = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                verilənlər, ünvan = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_verilənlər.append(verilənlər)
            server_VALUE.sendto(verilənlər, ünvan)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maşın = virtual_maşın(yerinə_qoymaq / ('build/kernel.' + 종류), 종류)
            try:
                for iterasiya_VALUE in range(2):
                    maşın.Əmr('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maşın.Əmr('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                İcra_Et = len(maşın.LOG_yaz)
                maşın.직렬.sendall(b'run posixinput\n')
                maşın.gözlə_vəziyyət('POSIX INPUT READY', İcra_Et)
                maşın.직렬.sendall(b'abcdef')
                출력 = maşın.gözlə_vəziyyət('jkoros> ', İcra_Et)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                maşın.Əmr('javac Hello.java', ['Exit: 0'])
                maşın.Əmr('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maşın.Əmr('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ölçü[종류] = maşın.LOG_yaz.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX FAYL/공유 yerinə_qoymaq/삭제 수명/ünvan qorumaq_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                maşın.Bağla()
        assert b'posix-udp' in RECEIVED_verilənlər and b'truncate' in RECEIVED_verilənlər and b'' in RECEIVED_verilənlər
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    ölçü['host_datagrams'] = [verilənlər.decode() for verilənlər in RECEIVED_verilənlər]
    (yerinə_qoymaq / 'build/규약시험.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    icra_etmək_əmr()
