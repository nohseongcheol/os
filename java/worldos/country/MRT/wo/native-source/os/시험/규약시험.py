#!/usr/bin/env python3
"""dalal libc 없이 연결한 한국어 C 프로그램을 liteew_mbir ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import luy_feeñ_te_jëmmadi_masin

위치 = Path(__file__).resolve().parents[1]

def def_ndigel():
    결과 = {}
    dëggu_xëyma = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dëggu_xëyma.bind(('127.0.0.1', 0))
    dëggu_xëyma.settimeout(0.1)
    접속번호 = dëggu_xëyma.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                mbir, dëkkuwaay = dëggu_xëyma.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(mbir)
            dëggu_xëyma.sendto(mbir, dëkkuwaay)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            masin = luy_feeñ_te_jëmmadi_masin(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for baamtu_xëyma in range(2):
                    masin.ndigel('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    masin.ndigel('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                daw = len(masin.làq_Dënk)
                masin.직렬.sendall(b'run posixinput\n')
                masin.기다림('POSIX INPUT READY', daw)
                masin.직렬.sendall(b'abcdef')
                출력 = masin.기다림('jkoros> ', daw)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                masin.ndigel('javac Hello.java', ['Exit: 0'])
                masin.ndigel('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                masin.ndigel('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = masin.làq_Dënk.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX bara_denc/공유 위치/삭제 수명/dëkkuwaay saama_xëyma/UDP/표준 입력/기존 Java', flush=True)
            finally:
                masin.Tej()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); dëggu_xëyma.close()
    결과['host_datagrams'] = [mbir.decode() for mbir in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    def_ndigel()
