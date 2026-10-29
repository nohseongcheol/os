#!/usr/bin/env python3
"""esasy libc 없이 연결한 한국어 C 프로그램을 hakyky_maglumat ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import hyýaly_kompýuter

위치 = Path(__file__).resolve().parents[1]

def ýerine_ýetir_buýruk():
    결과 = {}
    serwer_baha = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serwer_baha.bind(('127.0.0.1', 0))
    serwer_baha.settimeout(0.1)
    접속번호 = serwer_baha.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                maglumat, salgy = serwer_baha.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(maglumat)
            serwer_baha.sendto(maglumat, salgy)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            kompýuter = hyýaly_kompýuter(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for iterasiýa_baha in range(2):
                    kompýuter.buýruk('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    kompýuter.buýruk('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Bitir = len(kompýuter.hasaba_alyş_setir)
                kompýuter.직렬.sendall(b'run posixinput\n')
                kompýuter.기다림('POSIX INPUT READY', Bitir)
                kompýuter.직렬.sendall(b'abcdef')
                출력 = kompýuter.기다림('jkoros> ', Bitir)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                kompýuter.buýruk('javac Hello.java', ['Exit: 0'])
                kompýuter.buýruk('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                kompýuter.buýruk('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Faýl/공유 위치/삭제 수명/salgy gora_baha/UDP/표준 입력/기존 Java', flush=True)
            finally:
                kompýuter.Ýap()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); serwer_baha.close()
    결과['host_datagrams'] = [maglumat.decode() for maglumat in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ýerine_ýetir_buýruk()
