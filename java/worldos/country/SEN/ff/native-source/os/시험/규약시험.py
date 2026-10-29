#!/usr/bin/env python3
"""njaatigi libc 없이 연결한 한국어 C 프로그램을 laatii_keɓe ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

위치 = Path(__file__).resolve().parents[1]

def 실행():
    결과 = {}
    sarworde_njaru = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sarworde_njaru.bind(('127.0.0.1', 0))
    sarworde_njaru.settimeout(0.1)
    접속번호 = sarworde_njaru.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                keɓe, ñiiɓirde = sarworde_njaru.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(keɓe)
            sarworde_njaru.sendto(keɓe, ñiiɓirde)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for 반복 in range(2):
                    기계.ginol('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.ginol('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                huutoraade = len(기계.suurnal_winndande)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', huutoraade)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', huutoraade)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.ginol('javac Hello.java', ['Exit: 0'])
                기계.ginol('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.ginol('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.suurnal_winndande.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX fiilde/공유 위치/삭제 수명/ñiiɓirde suurde_njaru/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.uddude()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); sarworde_njaru.close()
    결과['host_datagrams'] = [keɓe.decode() for keɓe in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
