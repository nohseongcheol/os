#!/usr/bin/env python3
"""tashkilotchi libc 없이 연결한 한국어 C 프로그램을 real_ma_lumotlar ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

Holati = Path(__file__).resolve().parents[1]

def bajarmoq_buyruq():
    o_lchov = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    접속번호 = server_VALUE.getsockname()[1]
    RECEIVED_ma_lumotlar = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ma_lumotlar, manzil = server_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_ma_lumotlar.append(ma_lumotlar)
            server_VALUE.sendto(ma_lumotlar, manzil)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(Holati / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    기계.Buyruq('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.Buyruq('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Bajarish = len(기계.LOG_satr)
                기계.직렬.sendall(b'run posixinput\n')
                기계.bir_daqiqa_holat('POSIX INPUT READY', Bajarish)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.bir_daqiqa_holat('jkoros> ', Bajarish)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.Buyruq('javac Hello.java', ['Exit: 0'])
                기계.Buyruq('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.Buyruq('run hello recovered', ['arg: recovered', 'Exit: 0'])
                o_lchov[종류] = 기계.LOG_satr.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fayl/공유 Holati/삭제 수명/manzil himoya_qilmoq_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.Yopish()
        assert b'posix-udp' in RECEIVED_ma_lumotlar and b'truncate' in RECEIVED_ma_lumotlar and b'' in RECEIVED_ma_lumotlar
    finally:
        끝냄.set(); 일꾼.join(timeout=2); server_VALUE.close()
    o_lchov['host_datagrams'] = [ma_lumotlar.decode() for ma_lumotlar in RECEIVED_ma_lumotlar]
    (Holati / 'build/규약시험.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    bajarmoq_buyruq()
