#!/usr/bin/env python3
"""host libc 없이 연결한 Nederlands C 프로그램을 werkelijk_gegevens ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_gebruiker_net import VM

positie = Path(__file__).resolve().parents[1]

def Uitvoeren_opdracht():
    resultaat = {}
    server_WAARDE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_WAARDE.bind(('127.0.0.1', 0))
    server_WAARDE.settimeout(0.1)
    poortnummer = server_WAARDE.getsockname()[1]
    OPBRENGST_gegevens = []
    끝냄 = threading.Event()
    def echo_reactie():
        while not 끝냄.is_set():
            try:
                gegevens, ADRES = server_WAARDE.recvfrom(4096)
            except socket.timeout:
                continue
            OPBRENGST_gegevens.append(gegevens)
            server_WAARDE.sendto(gegevens, ADRES)
    werkrol_WAARDE = threading.Thread(target=echo_reactie, daemon=True)
    werkrol_WAARDE.start()
    try:
        for soort_WAARDE in ('elf', 'iso'):
            machine = VM(positie / ('build/kernel.' + soort_WAARDE), soort_WAARDE)
            try:
                for sprint_WAARDE in range(2):
                    machine.opdracht('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    machine.opdracht('run posixudp ' + str(poortnummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                starten = len(machine.LOG_RECORD)
                machine.직렬.sendall(b'run posixinput\n')
                machine.wachtstatus('POSIX INPUT READY', starten)
                machine.직렬.sendall(b'abcdef')
                tekstuitvoer = machine.wachtstatus('jkoros> ', starten)
                assert 'POSIX INPUT PASS' in tekstuitvoer and 'Exit: 0' in tekstuitvoer, tekstuitvoer
                machine.opdracht('javac Hello.java', ['Exit: 0'])
                machine.opdracht('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                machine.opdracht('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultaat[soort_WAARDE] = machine.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS:', soort_WAARDE, 'POSIX bestand/공유 positie/삭제 수명/ADRES beschermen_WAARDE/UDP/표준 invoer_WAARDE/기존 Java', flush=True)
            finally:
                machine.Sluiten()
        assert b'posix-udp' in OPBRENGST_gegevens and b'truncate' in OPBRENGST_gegevens and b'' in OPBRENGST_gegevens
    finally:
        끝냄.set(); werkrol_WAARDE.join(timeout=2); server_WAARDE.close()
    resultaat['host_datagrams'] = [gegevens.decode() for gegevens in OPBRENGST_gegevens]
    (positie / 'build/taak_test.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Uitvoeren_opdracht()
