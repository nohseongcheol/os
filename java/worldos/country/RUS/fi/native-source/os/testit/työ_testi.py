#!/usr/bin/env python3
"""isäntä libc 없이 연결한 suomi C 프로그램을 todellinen_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from testi_käyttäjä_verkko import VM

paikka = Path(__file__).resolve().parents[1]

def Suorita_komento():
    TULOS = {}
    palvelin_ARVO = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    palvelin_ARVO.bind(('127.0.0.1', 0))
    palvelin_ARVO.settimeout(0.1)
    portin_numero = palvelin_ARVO.getsockname()[1]
    SAATU_HINTA_data = []
    끝냄 = threading.Event()
    def päivitys_palaute():
        while not 끝냄.is_set():
            try:
                data, OSOITE = palvelin_ARVO.recvfrom(4096)
            except socket.timeout:
                continue
            SAATU_HINTA_data.append(data)
            palvelin_ARVO.sendto(data, OSOITE)
    työntekijä_ARVO = threading.Thread(target=päivitys_palaute, daemon=True)
    työntekijä_ARVO.start()
    try:
        for 종류 in ('elf', 'iso'):
            kone = VM(paikka / ('build/kernel.' + 종류), 종류)
            try:
                for sprintti_ARVO in range(2):
                    kone.komento('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    kone.komento('run posixudp ' + str(portin_numero), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Suorita_2 = len(kone.LOG_TIETUE)
                kone.직렬.sendall(b'run posixinput\n')
                kone.odotustila('POSIX INPUT READY', Suorita_2)
                kone.직렬.sendall(b'abcdef')
                tulostuspaikka = kone.odotustila('jkoros> ', Suorita_2)
                assert 'POSIX INPUT PASS' in tulostuspaikka and 'Exit: 0' in tulostuspaikka, tulostuspaikka
                kone.komento('javac Hello.java', ['Exit: 0'])
                kone.komento('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                kone.komento('run hello recovered', ['arg: recovered', 'Exit: 0'])
                TULOS[종류] = kone.LOG_TIETUE.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX tiedoston_nimi/공유 paikka/삭제 수명/OSOITE suojata_ARVO/UDP/표준 syöte_ARVO/기존 Java', flush=True)
            finally:
                kone.Sulje()
        assert b'posix-udp' in SAATU_HINTA_data and b'truncate' in SAATU_HINTA_data and b'' in SAATU_HINTA_data
    finally:
        끝냄.set(); työntekijä_ARVO.join(timeout=2); palvelin_ARVO.close()
    TULOS['host_datagrams'] = [data.decode() for data in SAATU_HINTA_data]
    (paikka / 'build/työ_testi.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Suorita_komento()
