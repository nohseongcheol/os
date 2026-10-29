#!/usr/bin/env python3
"""gazda libc 없이 연결한 magyar C 프로그램을 tényleges_adat ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from teszt_felhasználó_hálózat import VM

Pozíció = Path(__file__).resolve().parents[1]

def végrehajt_parancs():
    KR = {}
    kiszolgáló_ÉRTÉK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    kiszolgáló_ÉRTÉK.bind(('127.0.0.1', 0))
    kiszolgáló_ÉRTÉK.settimeout(0.1)
    portszám = kiszolgáló_ÉRTÉK.getsockname()[1]
    KAPOTT_adat = []
    끝냄 = threading.Event()
    def visszhang_válasz():
        while not 끝냄.is_set():
            try:
                adat, CÍM = kiszolgáló_ÉRTÉK.recvfrom(4096)
            except socket.timeout:
                continue
            KAPOTT_adat.append(adat)
            kiszolgáló_ÉRTÉK.sendto(adat, CÍM)
    dolgozó_ÉRTÉK = threading.Thread(target=visszhang_válasz, daemon=True)
    dolgozó_ÉRTÉK.start()
    try:
        for Altípus_ÉRTÉK in ('elf', 'iso'):
            gép = VM(Pozíció / ('build/kernel.' + Altípus_ÉRTÉK), Altípus_ÉRTÉK)
            try:
                for futam_ÉRTÉK in range(2):
                    gép.Parancs('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    gép.Parancs('run posixudp ' + str(portszám), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Futtatás = len(gép.LOG_REKORD)
                gép.직렬.sendall(b'run posixinput\n')
                gép.várakozóállapot('POSIX INPUT READY', Futtatás)
                gép.직렬.sendall(b'abcdef')
                Kimenet = gép.várakozóállapot('jkoros> ', Futtatás)
                assert 'POSIX INPUT PASS' in Kimenet and 'Exit: 0' in Kimenet, Kimenet
                gép.Parancs('javac Hello.java', ['Exit: 0'])
                gép.Parancs('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                gép.Parancs('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[Altípus_ÉRTÉK] = gép.LOG_REKORD.decode('utf-8', 'replace')
                print('PASS:', Altípus_ÉRTÉK, 'POSIX Fájl/공유 Pozíció/삭제 수명/CÍM véd_ÉRTÉK/UDP/표준 bevitel_ÉRTÉK/기존 Java', flush=True)
            finally:
                gép.Bezárás()
        assert b'posix-udp' in KAPOTT_adat and b'truncate' in KAPOTT_adat and b'' in KAPOTT_adat
    finally:
        끝냄.set(); dolgozó_ÉRTÉK.join(timeout=2); kiszolgáló_ÉRTÉK.close()
    KR['host_datagrams'] = [adat.decode() for adat in KAPOTT_adat]
    (Pozíció / 'build/eset_teszt.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    végrehajt_parancs()
