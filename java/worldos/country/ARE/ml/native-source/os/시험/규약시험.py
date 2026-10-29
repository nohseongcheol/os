#!/usr/bin/env python3
"""ഹോസ്റ്റ് libc 없이 연결한 한국어 C 프로그램을 വാസ്തവമായ_ഡാറ്റാ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import അയഥാര്_ഥ_മെഷീൻ

സ്ഥാനം = Path(__file__).resolve().parents[1]

def നടപ്പാക്കുക_കമാന്_ഡ്():
    അളവ് = {}
    സെര്_വര്_മൂല്യം = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    സെര്_വര്_മൂല്യം.bind(('127.0.0.1', 0))
    സെര്_വര്_മൂല്യം.settimeout(0.1)
    പോര്_ട്ട്_നമ്പര് = സെര്_വര്_മൂല്യം.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ഡാറ്റാ, ഇമെയിൽ = സെര്_വര്_മൂല്യം.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ഡാറ്റാ)
            സെര്_വര്_മൂല്യം.sendto(ഡാറ്റാ, ഇമെയിൽ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / ('build/kernel.' + 종류), 종류)
            try:
                for ആവര്_ത്തനം_മൂല്യം in range(2):
                    മെഷീൻ.ആജ്ഞ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    മെഷീൻ.ആജ്ഞ('run posixudp ' + str(പോര്_ട്ട്_നമ്പര്), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                നടപ്പിലാക്കുക = len(മെഷീൻ.ലോഗ്_രേഖ)
                മെഷീൻ.직렬.sendall(b'run posixinput\n')
                മെഷീൻ.കാക്കുക_അവസ്ഥ('POSIX INPUT READY', നടപ്പിലാക്കുക)
                മെഷീൻ.직렬.sendall(b'abcdef')
                ഫലം = മെഷീൻ.കാക്കുക_അവസ്ഥ('jkoros> ', നടപ്പിലാക്കുക)
                assert 'POSIX INPUT PASS' in ഫലം and 'Exit: 0' in ഫലം, ഫലം
                മെഷീൻ.ആജ്ഞ('javac Hello.java', ['Exit: 0'])
                മെഷീൻ.ആജ്ഞ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                മെഷീൻ.ആജ്ഞ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                അളവ്[종류] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ഫയല്/공유 സ്ഥാനം/삭제 수명/ഇമെയിൽ പരിരക്ഷിക്കുക_മൂല്യം/UDP/표준 입력/기존 Java', flush=True)
            finally:
                മെഷീൻ.അടയ്ക്കു()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); സെര്_വര്_മൂല്യം.close()
    അളവ്['host_datagrams'] = [ഡാറ്റാ.decode() for ഡാറ്റാ in 받은자료]
    (സ്ഥാനം / 'build/규약시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    നടപ്പാക്കുക_കമാന്_ഡ്()
