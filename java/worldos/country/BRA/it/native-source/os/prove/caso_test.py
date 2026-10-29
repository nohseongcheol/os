#!/usr/bin/env python3
"""host libc 없이 연결한 Italiano C 프로그램을 effettivo_dati ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_Usenet import VM

posizione = Path(__file__).resolve().parents[1]

def Esegui_comando():
    risultato = {}
    server_VALORE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALORE.bind(('127.0.0.1', 0))
    server_VALORE.settimeout(0.1)
    numero_di_porta = server_VALORE.getsockname()[1]
    RICEV_SCAD_dati = []
    terminazione_Stato = threading.Event()
    def eco_schermo_replica():
        while not terminazione_Stato.is_set():
            try:
                dati, e_mail = server_VALORE.recvfrom(4096)
            except socket.timeout:
                continue
            RICEV_SCAD_dati.append(dati)
            server_VALORE.sendto(dati, e_mail)
    lavoratore_VALORE = threading.Thread(target=eco_schermo_replica, daemon=True)
    lavoratore_VALORE.start()
    try:
        for Kind_VALORE in ('elf', 'iso'):
            computer = VM(posizione / ('build/kernel.' + Kind_VALORE), Kind_VALORE)
            try:
                for sprint_VALORE in range(2):
                    computer.comando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    computer.comando('run posixudp ' + str(numero_di_porta), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                avvia = len(computer.LOG_riga)
                computer.seriale_VALORE.sendall(b'run posixinput\n')
                computer.stato_di_attesa('POSIX INPUT READY', avvia)
                computer.seriale_VALORE.sendall(b'abcdef')
                uscitaTesto = computer.stato_di_attesa('jkoros> ', avvia)
                assert 'POSIX INPUT PASS' in uscitaTesto and 'Exit: 0' in uscitaTesto, uscitaTesto
                computer.comando('javac Hello.java', ['Exit: 0'])
                computer.comando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                computer.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                risultato[Kind_VALORE] = computer.LOG_riga.decode('utf-8', 'replace')
                print('PASS:', Kind_VALORE, 'POSIX file/공유 posizione/삭제 수명/e_mail proteggere_VALORE/UDP/표준 input_VALORE/기존 Java', flush=True)
            finally:
                computer.Chiudi()
        assert b'posix-udp' in RICEV_SCAD_dati and b'truncate' in RICEV_SCAD_dati and b'' in RICEV_SCAD_dati
    finally:
        terminazione_Stato.set(); lavoratore_VALORE.join(timeout=2); server_VALORE.close()
    risultato['host_datagrams'] = [dati.decode() for dati in RICEV_SCAD_dati]
    (posizione / 'build/caso_test.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Esegui_comando()
