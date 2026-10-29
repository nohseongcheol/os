#!/usr/bin/env python3
"""go_nea_ditirelo libc 없이 연결한 한국어 C 프로그램을 kgonthe_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import sethalwa_motšhene

위치 = Path(__file__).resolve().parents[1]

def phethagatša_taelo():
    결과 = {}
    seba_boleng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seba_boleng.bind(('127.0.0.1', 0))
    seba_boleng.settimeout(0.1)
    접속번호 = seba_boleng.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, atrese = seba_boleng.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(data)
            seba_boleng.sendto(data, atrese)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            motšhene = sethalwa_motšhene(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for poeletšo_boleng in range(2):
                    motšhene.Taelo('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    motšhene.Taelo('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Diriša = len(motšhene.pego_rei)
                motšhene.직렬.sendall(b'run posixinput\n')
                motšhene.기다림('POSIX INPUT READY', Diriša)
                motšhene.직렬.sendall(b'abcdef')
                출력 = motšhene.기다림('jkoros> ', Diriša)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                motšhene.Taelo('javac Hello.java', ['Exit: 0'])
                motšhene.Taelo('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                motšhene.Taelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = motšhene.pego_rei.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Faele/공유 위치/삭제 수명/atrese šireletša_boleng/UDP/표준 입력/기존 Java', flush=True)
            finally:
                motšhene.Tswalela()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); seba_boleng.close()
    결과['host_datagrams'] = [data.decode() for data in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    phethagatša_taelo()
