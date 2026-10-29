#!/usr/bin/env python3
"""värd libc 없이 연결한 Svenska C 프로그램을 verklig_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_användare_nätverk import VM

position = Path(__file__).resolve().parents[1]

def köra_kommando():
    RESULTAT = {}
    server_värde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_värde.bind(('127.0.0.1', 0))
    server_värde.settimeout(0.1)
    portnummer = server_värde.getsockname()[1]
    BELOPP_data = []
    끝냄 = threading.Event()
    def UppdateraSkärm_svara():
        while not 끝냄.is_set():
            try:
                data, Adress = server_värde.recvfrom(4096)
            except socket.timeout:
                continue
            BELOPP_data.append(data)
            server_värde.sendto(data, Adress)
    arbete_värde = threading.Thread(target=UppdateraSkärm_svara, daemon=True)
    arbete_värde.start()
    try:
        for variant_värde in ('elf', 'iso'):
            dator = VM(position / ('build/kernel.' + variant_värde), variant_värde)
            try:
                for sprint_värde in range(2):
                    dator.kommando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    dator.kommando('run posixudp ' + str(portnummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Kör = len(dator.LOG_POST)
                dator.직렬.sendall(b'run posixinput\n')
                dator.tillståndet_Vänta('POSIX INPUT READY', Kör)
                dator.직렬.sendall(b'abcdef')
                utmatningsposition = dator.tillståndet_Vänta('jkoros> ', Kör)
                assert 'POSIX INPUT PASS' in utmatningsposition and 'Exit: 0' in utmatningsposition, utmatningsposition
                dator.kommando('javac Hello.java', ['Exit: 0'])
                dator.kommando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                dator.kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTAT[variant_värde] = dator.LOG_POST.decode('utf-8', 'replace')
                print('PASS:', variant_värde, 'POSIX filnamn/공유 position/삭제 수명/Adress skydda_värde/UDP/표준 indata_värde/기존 Java', flush=True)
            finally:
                dator.Stäng()
        assert b'posix-udp' in BELOPP_data and b'truncate' in BELOPP_data and b'' in BELOPP_data
    finally:
        끝냄.set(); arbete_värde.join(timeout=2); server_värde.close()
    RESULTAT['host_datagrams'] = [data.decode() for data in BELOPP_data]
    (position / 'build/jobb_test.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    köra_kommando()
