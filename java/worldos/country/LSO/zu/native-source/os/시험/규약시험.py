#!/usr/bin/env python3
"""singatha libc 없이 연결한 Isi_Zulu C 프로그램을 ulwazi_ngokwenzekile_imininingwane ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import utalagu_umshini

위치 = Path(__file__).resolve().parents[1]

def yenza_umyalo():
    결과 = {}
    Iseva_inani = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Iseva_inani.bind(('127.0.0.1', 0))
    Iseva_inani.settimeout(0.1)
    접속번호 = Iseva_inani.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                imininingwane, ikheli = Iseva_inani.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(imininingwane)
            Iseva_inani.sendto(imininingwane, ikheli)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            umshini = utalagu_umshini(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for impinda_inani in range(2):
                    umshini.Umlayelo('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    umshini.Umlayelo('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Sebenzisa = len(umshini.loga_umugqa)
                umshini.직렬.sendall(b'run posixinput\n')
                umshini.기다림('POSIX INPUT READY', Sebenzisa)
                umshini.직렬.sendall(b'abcdef')
                출력 = umshini.기다림('jkoros> ', Sebenzisa)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                umshini.Umlayelo('javac Hello.java', ['Exit: 0'])
                umshini.Umlayelo('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                umshini.Umlayelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = umshini.loga_umugqa.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Ihele/공유 위치/삭제 수명/ikheli vikela_inani/UDP/표준 입력/기존 Java', flush=True)
            finally:
                umshini.Vala()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); Iseva_inani.close()
    결과['host_datagrams'] = [imininingwane.decode() for imininingwane in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    yenza_umyalo()
