#!/usr/bin/env python3
"""vært libc 없이 연결한 Dansk C 프로그램을 faktisk_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from test_bruger_netværk import VM

Placering = Path(__file__).resolve().parents[1]

def Udfør_kommando():
    KR = {}
    server_VÆRDI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VÆRDI.bind(('127.0.0.1', 0))
    server_VÆRDI.settimeout(0.1)
    portnummer = server_VÆRDI.getsockname()[1]
    MODTAGET_VED_UDLØB_data = []
    끝냄 = threading.Event()
    def ekko_svar():
        while not 끝냄.is_set():
            try:
                data, mail = server_VÆRDI.recvfrom(4096)
            except socket.timeout:
                continue
            MODTAGET_VED_UDLØB_data.append(data)
            server_VÆRDI.sendto(data, mail)
    arbejder_VÆRDI = threading.Thread(target=ekko_svar, daemon=True)
    arbejder_VÆRDI.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskine = VM(Placering / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_VÆRDI in range(2):
                    maskine.Kommando('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maskine.Kommando('run posixudp ' + str(portnummer), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Kør_2 = len(maskine.LOG_post)
                maskine.직렬.sendall(b'run posixinput\n')
                maskine.ventetilstand('POSIX INPUT READY', Kør_2)
                maskine.직렬.sendall(b'abcdef')
                Udgang = maskine.ventetilstand('jkoros> ', Kør_2)
                assert 'POSIX INPUT PASS' in Udgang and 'Exit: 0' in Udgang, Udgang
                maskine.Kommando('javac Hello.java', ['Exit: 0'])
                maskine.Kommando('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maskine.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = maskine.LOG_post.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fil/공유 Placering/삭제 수명/mail beskytte_VÆRDI/UDP/표준 input_VÆRDI/기존 Java', flush=True)
            finally:
                maskine.Luk()
        assert b'posix-udp' in MODTAGET_VED_UDLØB_data and b'truncate' in MODTAGET_VED_UDLØB_data and b'' in MODTAGET_VED_UDLØB_data
    finally:
        끝냄.set(); arbejder_VÆRDI.join(timeout=2); server_VÆRDI.close()
    KR['host_datagrams'] = [data.decode() for data in MODTAGET_VED_UDLØB_data]
    (Placering / 'build/job_test.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    Udfør_kommando()
