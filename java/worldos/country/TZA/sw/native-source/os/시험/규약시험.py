#!/usr/bin/env python3
"""mwenyeji libc 없이 연결한 한국어 C 프로그램을 halisi_data ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import pepe_mashine

위치 = Path(__file__).resolve().parents[1]

def tekeleza_amri():
    결과 = {}
    seva_thamani = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seva_thamani.bind(('127.0.0.1', 0))
    seva_thamani.settimeout(0.1)
    namba_ya_kituo = seva_thamani.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                data, anwani = seva_thamani.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(data)
            seva_thamani.sendto(data, anwani)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mashine = pepe_mashine(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for sprint_thamani in range(2):
                    mashine.amri('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    mashine.amri('run posixudp ' + str(namba_ya_kituo), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                endesha = len(mashine.batli_REKODI)
                mashine.직렬.sendall(b'run posixinput\n')
                mashine.subiri_hali('POSIX INPUT READY', endesha)
                mashine.직렬.sendall(b'abcdef')
                출력 = mashine.subiri_hali('jkoros> ', endesha)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                mashine.amri('javac Hello.java', ['Exit: 0'])
                mashine.amri('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                mashine.amri('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = mashine.batli_REKODI.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX faili/공유 위치/삭제 수명/anwani linda_thamani/UDP/표준 입력/기존 Java', flush=True)
            finally:
                mashine.funga()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); seva_thamani.close()
    결과['host_datagrams'] = [data.decode() for data in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    tekeleza_amri()
