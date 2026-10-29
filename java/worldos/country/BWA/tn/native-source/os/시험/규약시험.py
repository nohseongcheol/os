#!/usr/bin/env python3
"""pinagare libc 없이 연결한 한국어 C 프로그램을 tota_tshedimosetso ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import seka_motšhine

위치 = Path(__file__).resolve().parents[1]

def diragatsa_Taelo():
    결과 = {}
    sefara_Boleng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sefara_Boleng.bind(('127.0.0.1', 0))
    sefara_Boleng.settimeout(0.1)
    접속번호 = sefara_Boleng.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                tshedimosetso, aterese = sefara_Boleng.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(tshedimosetso)
            sefara_Boleng.sendto(tshedimosetso, aterese)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            motšhine = seka_motšhine(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for poeletso_Boleng in range(2):
                    motšhine.Taelo('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    motšhine.Taelo('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                dirisa = len(motšhine.rekota_mola)
                motšhine.직렬.sendall(b'run posixinput\n')
                motšhine.기다림('POSIX INPUT READY', dirisa)
                motšhine.직렬.sendall(b'abcdef')
                출력 = motšhine.기다림('jkoros> ', dirisa)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                motšhine.Taelo('javac Hello.java', ['Exit: 0'])
                motšhine.Taelo('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                motšhine.Taelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = motšhine.rekota_mola.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX faele/공유 위치/삭제 수명/aterese sireletsa_Boleng/UDP/표준 입력/기존 Java', flush=True)
            finally:
                motšhine.tswala()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); sefara_Boleng.close()
    결과['host_datagrams'] = [tshedimosetso.decode() for tshedimosetso in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    diragatsa_Taelo()
