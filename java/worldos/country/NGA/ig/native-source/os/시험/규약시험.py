#!/usr/bin/env python3
"""usu libc 없이 연결한 한국어 C 프로그램을 ǹdịnezie_datà ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import kendìnuchè_ngwa_komputa

위치 = Path(__file__).resolve().parents[1]

def mee_nnyemiwu():
    결과 = {}
    savà_valuu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    savà_valuu.bind(('127.0.0.1', 0))
    savà_valuu.settimeout(0.1)
    접속번호 = savà_valuu.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                datà, àdreèsì = savà_valuu.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(datà)
            savà_valuu.sendto(datà, àdreèsì)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for memmekwa_valuu in range(2):
                    ngwa_komputa.Ntiiwu('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ngwa_komputa.Ntiiwu('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Bido = len(ngwa_komputa.ndekọ_NDEKỌ)
                ngwa_komputa.직렬.sendall(b'run posixinput\n')
                ngwa_komputa.기다림('POSIX INPUT READY', Bido)
                ngwa_komputa.직렬.sendall(b'abcdef')
                출력 = ngwa_komputa.기다림('jkoros> ', Bido)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                ngwa_komputa.Ntiiwu('javac Hello.java', ['Exit: 0'])
                ngwa_komputa.Ntiiwu('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ngwa_komputa.Ntiiwu('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Faịlụ/공유 위치/삭제 수명/àdreèsì nchedo_valuu/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ngwa_komputa.Mechie()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); savà_valuu.close()
    결과['host_datagrams'] = [datà.decode() for datà in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    mee_nnyemiwu()
