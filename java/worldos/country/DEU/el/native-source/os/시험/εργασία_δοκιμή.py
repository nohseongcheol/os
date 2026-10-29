#!/usr/bin/env python3
"""φιλοξενώ libc 없이 연결한 ελληνικά C 프로그램을 πραγματικός_δεδομένα ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from δοκιμή_χρήστης_δίκτυο import εικονική_μηχανή

Θέση = Path(__file__).resolve().parents[1]

def εκτελώ_εντολή():
    μέτρηση = {}
    διακομιστής_τιμή = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    διακομιστής_τιμή.bind(('127.0.0.1', 0))
    διακομιστής_τιμή.settimeout(0.1)
    αριθμός_θύρας = διακομιστής_τιμή.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def ηχώ_απαντώ():
        while not 끝냄.is_set():
            try:
                δεδομένα, διεύθυνση = διακομιστής_τιμή.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(δεδομένα)
            διακομιστής_τιμή.sendto(δεδομένα, διεύθυνση)
    일꾼 = threading.Thread(target=ηχώ_απαντώ, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / ('build/kernel.' + 종류), 종류)
            try:
                for επανάληψη_τιμή in range(2):
                    υπολογιστής_5eb260fa.Εντολή('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    υπολογιστής_5eb260fa.Εντολή('run posixudp ' + str(αριθμός_θύρας), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Εκτέλεση_2 = len(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
                υπολογιστής_5eb260fa.직렬.sendall(b'run posixinput\n')
                υπολογιστής_5eb260fa.κατάσταση_αναμονής('POSIX INPUT READY', Εκτέλεση_2)
                υπολογιστής_5eb260fa.직렬.sendall(b'abcdef')
                Έξοδος = υπολογιστής_5eb260fa.κατάσταση_αναμονής('jkoros> ', Εκτέλεση_2)
                assert 'POSIX INPUT PASS' in Έξοδος and 'Exit: 0' in Έξοδος, Έξοδος
                υπολογιστής_5eb260fa.Εντολή('javac Hello.java', ['Exit: 0'])
                υπολογιστής_5eb260fa.Εντολή('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                υπολογιστής_5eb260fa.Εντολή('run hello recovered', ['arg: recovered', 'Exit: 0'])
                μέτρηση[종류] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Αρχείο/공유 Θέση/삭제 수명/διεύθυνση προστασία_τιμή/UDP/표준 είσοδος_τιμή/기존 Java', flush=True)
            finally:
                υπολογιστής_5eb260fa.Κλείσιμο()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); διακομιστής_τιμή.close()
    μέτρηση['host_datagrams'] = [δεδομένα.decode() for δεδομένα in 받은자료]
    (Θέση / 'build/εργασία_δοκιμή.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    εκτελώ_εντολή()
