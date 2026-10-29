#!/usr/bin/env python3
"""vert libc 없이 연결한 norsk C 프로그램을 faktisk_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_bruker_nettverk import VM

Posisjon = Path(__file__).resolve().parents[1]

def Utfør_kommando():
    KR = {}
    server_VERDI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VERDI.bind(('127.0.0.1', 0))
    server_VERDI.settimeout(0.1)
    portnummer = server_VERDI.getsockname()[1]
    MOTTATT_AVKAST_data = []
    끝냄 = threading.Event()
    def oppdatere_skjerm_svar():
        while not 끝냄.is_set():
            try:
                data, e_post = server_VERDI.recvfrom(4096)
            except socket.timeout:
                continue
            MOTTATT_AVKAST_data.append(data)
            server_VERDI.sendto(data, e_post)
    arbeider_VERDI = threading.Thread(target=oppdatere_skjerm_svar, daemon=True)
    arbeider_VERDI.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskin = VM(Posisjon / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VERDI in range(2):
                    maskin.Kommando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maskin.Kommando('run posixudp ' + str(portnummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Kjør_2 = len(maskin.LOG_POST)
                maskin.직렬.sendall(b'run posixinput\n')
                maskin.ventende_tilstand('POSIX INPUT READY', Kjør_2)
                maskin.직렬.sendall(b'abcdef')
                Utgang = maskin.ventende_tilstand('jkoros> ', Kjør_2)
                assert 'POSIX INPUT PASS' in Utgang and 'Exit: 0' in Utgang, Utgang
                maskin.Kommando('javac Hello.java', ['Exit: 0'])
                maskin.Kommando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maskin.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = maskin.LOG_POST.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fil/공유 Posisjon/삭제 수명/e_post beskytte_VERDI/UDP/표준 inndata_VERDI/기존 Java', flush=True)
            finally:
                maskin.Lukk()
        assert b'posix-udp' in MOTTATT_AVKAST_data and b'truncate' in MOTTATT_AVKAST_data and b'' in MOTTATT_AVKAST_data
    finally:
        끝냄.set(); arbeider_VERDI.join(timeout=2); server_VERDI.close()
    KR['host_datagrams'] = [data.decode() for data in MOTTATT_AVKAST_data]
    (Posisjon / 'build/sak_test.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Utfør_kommando()
