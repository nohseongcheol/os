#!/usr/bin/env python3
"""vert libc 없이 연결한 한국어 C 프로그램을 faktisk_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import virtuell_maskin

Posisjon = Path(__file__).resolve().parents[1]

def Utfør_kommando():
    forretningsmål = {}
    tenar_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tenar_VALUE.bind(('127.0.0.1', 0))
    tenar_VALUE.settimeout(0.1)
    portnummer = tenar_VALUE.getsockname()[1]
    RECEIVED_data = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, ADDRESS = tenar_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_data.append(data)
            tenar_VALUE.sendto(data, ADDRESS)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskin = virtuell_maskin(Posisjon / ('build/kernel.' + 종류), 종류)
            try:
                for gjentaking_VALUE in range(2):
                    maskin.Kommando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maskin.Kommando('run posixudp ' + str(portnummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Køyr_2 = len(maskin.LOG_rad)
                maskin.직렬.sendall(b'run posixinput\n')
                maskin.vent_status('POSIX INPUT READY', Køyr_2)
                maskin.직렬.sendall(b'abcdef')
                Utdata = maskin.vent_status('jkoros> ', Køyr_2)
                assert 'POSIX INPUT PASS' in Utdata and 'Exit: 0' in Utdata, Utdata
                maskin.Kommando('javac Hello.java', ['Exit: 0'])
                maskin.Kommando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maskin.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                forretningsmål[종류] = maskin.LOG_rad.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fil/공유 Posisjon/삭제 수명/ADDRESS verne_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                maskin.Lukk()
        assert b'posix-udp' in RECEIVED_data and b'truncate' in RECEIVED_data and b'' in RECEIVED_data
    finally:
        끝냄.set(); 일꾼.join(timeout=2); tenar_VALUE.close()
    forretningsmål['host_datagrams'] = [data.decode() for data in RECEIVED_data]
    (Posisjon / 'build/규약시험.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Utfør_kommando()
