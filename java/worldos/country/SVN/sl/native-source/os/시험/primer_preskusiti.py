#!/usr/bin/env python3
"""gostiti libc 없이 연결한 slovenščina C 프로그램을 dejanski_podatki ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from preskusiti_uporabnik_mreža import navidezni_računalnik

Položaj = Path(__file__).resolve().parents[1]

def Izvedi_ukaz():
    REZULTAT = {}
    strežnik_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    strežnik_VALUE.bind(('127.0.0.1', 0))
    strežnik_VALUE.settimeout(0.1)
    številka_vrat = strežnik_VALUE.getsockname()[1]
    RECEIVED_podatki = []
    끝냄 = threading.Event()
    def odmev_odgovor():
        while not 끝냄.is_set():
            try:
                podatki, naslov = strežnik_VALUE.recvfrom(4096)
            except socket.timeout:
                continue
            RECEIVED_podatki.append(podatki)
            strežnik_VALUE.sendto(podatki, naslov)
    일꾼 = threading.Thread(target=odmev_odgovor, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            računalnik = navidezni_računalnik(Položaj / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VALUE in range(2):
                    računalnik.Ukaz('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    računalnik.Ukaz('run posixudp ' + str(številka_vrat), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Zaženi = len(računalnik.LOG_zapis)
                računalnik.직렬.sendall(b'run posixinput\n')
                računalnik.čakalno_stanje('POSIX INPUT READY', Zaženi)
                računalnik.직렬.sendall(b'abcdef')
                Izpis = računalnik.čakalno_stanje('jkoros> ', Zaženi)
                assert 'POSIX INPUT PASS' in Izpis and 'Exit: 0' in Izpis, Izpis
                računalnik.Ukaz('javac Hello.java', ['Exit: 0'])
                računalnik.Ukaz('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                računalnik.Ukaz('run hello recovered', ['arg: recovered', 'Exit: 0'])
                REZULTAT[종류] = računalnik.LOG_zapis.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Datoteka/공유 Položaj/삭제 수명/naslov zaščititi_VALUE/UDP/표준 입력/기존 Java', flush=True)
            finally:
                računalnik.Zapri()
        assert b'posix-udp' in RECEIVED_podatki and b'truncate' in RECEIVED_podatki and b'' in RECEIVED_podatki
    finally:
        끝냄.set(); 일꾼.join(timeout=2); strežnik_VALUE.close()
    REZULTAT['host_datagrams'] = [podatki.decode() for podatki in RECEIVED_podatki]
    (Položaj / 'build/primer_preskusiti.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Izvedi_ukaz()
