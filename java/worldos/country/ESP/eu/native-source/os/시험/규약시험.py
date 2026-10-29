#!/usr/bin/env python3
"""Ostalari libc 없이 연결한 Euskara C 프로그램을 benetako_datuak ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import makina_birtual

Posizioa = Path(__file__).resolve().parents[1]

def exekutatu_komando():
    EMAITZA = {}
    zerbitzari_balio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    zerbitzari_balio.bind(('127.0.0.1', 0))
    zerbitzari_balio.settimeout(0.1)
    ataka_zenbaki = zerbitzari_balio.getsockname()[1]
    RECEIVED_datuak = []
    끝냄 = threading.Event()
    def atzeko_planoko_eguneratze_erantzun():
        while not 끝냄.is_set():
            try:
                datuak, helbide = zerbitzari_balio.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_datuak.append(datuak)
            zerbitzari_balio.sendto(datuak, helbide)
    일꾼 = threading.Thread(target=atzeko_planoko_eguneratze_erantzun, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            gailu = makina_birtual(Posizioa / ('build/kernel.' + 종류), 종류)
            try:
                for iterazio_balio in range(2):
                    gailu.Komandoa('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    gailu.Komandoa('run posixudp ' + str(ataka_zenbaki), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Exekutatu_2 = len(gailu.LOG_marka)
                gailu.직렬.sendall(b'run posixinput\n')
                gailu.itxaron_Egoera('POSIX INPUT READY', Exekutatu_2)
                gailu.직렬.sendall(b'abcdef')
                Irteera = gailu.itxaron_Egoera('jkoros> ', Exekutatu_2)
                assert 'POSIX INPUT PASS' in Irteera and 'Exit: 0' in Irteera, Irteera
                gailu.Komandoa('javac Hello.java', ['Exit: 0'])
                gailu.Komandoa('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                gailu.Komandoa('run hello recovered', ['arg: recovered', 'Exit: 0'])
                EMAITZA[종류] = gailu.LOG_marka.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fitxategia/공유 Posizioa/삭제 수명/helbide babestu_balio/UDP/표준 입력/기존 Java', flush=True)
            finally:
                gailu.Itxi()
        assert b'posix-udp' in RECEIVED_datuak and b'truncate' in RECEIVED_datuak and b'' in RECEIVED_datuak
    finally:
        끝냄.set(); 일꾼.join(timeout=2); zerbitzari_balio.close()
    EMAITZA['host_datagrams'] = [datuak.decode() for datuak in RECEIVED_datuak]
    (Posizioa / 'build/규약시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    exekutatu_komando()
