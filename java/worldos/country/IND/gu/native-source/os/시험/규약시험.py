#!/usr/bin/env python3
"""હોસ્ટ libc 없이 연결한 ગુજરાતી C 프로그램을 વાસ્તવિક_ડેટા ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import વર્ચુઅલ_મશીન

સ્થાન = Path(__file__).resolve().parents[1]

def અમલ_કરો_આદેશ():
    પરિમાણ = {}
    સર્વર_મૂલ્ય = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    સર્વર_મૂલ્ય.bind(('127.0.0.1', 0))
    સર્વર_મૂલ્ય.settimeout(0.1)
    પોર્ટ_નંબર = સર્વર_મૂલ્ય.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ડેટા, સરનામું = સર્વર_મૂલ્ય.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ડેટા)
            સર્વર_મૂલ્ય.sendto(ડેટા, સરનામું)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            મશીન = વર્ચુઅલ_મશીન(સ્થાન / ('build/kernel.' + 종류), 종류)
            try:
                for પુનરાવર્તન_મૂલ્ય in range(2):
                    મશીન.આદેશ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    મશીન.આદેશ('run posixudp ' + str(પોર્ટ_નંબર), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ચલાવો_2 = len(મશીન.લૉગ_પંક્તિ)
                મશીન.직렬.sendall(b'run posixinput\n')
                મશીન.પ્રતીક્ષા_સ્થિતિ('POSIX INPUT READY', ચલાવો_2)
                મશીન.직렬.sendall(b'abcdef')
                આઉટપુટ = મશીન.પ્રતીક્ષા_સ્થિતિ('jkoros> ', ચલાવો_2)
                assert 'POSIX INPUT PASS' in આઉટપુટ and 'Exit: 0' in આઉટપુટ, આઉટપુટ
                મશીન.આદેશ('javac Hello.java', ['Exit: 0'])
                મશીન.આદેશ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                મશીન.આદેશ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                પરિમાણ[종류] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ફાઈલ/공유 સ્થાન/삭제 수명/સરનામું રક્ષણ_કરો_મૂલ્ય/UDP/표준 입력/기존 Java', flush=True)
            finally:
                મશીન.બંધ_કરો()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); સર્વર_મૂલ્ય.close()
    પરિમાણ['host_datagrams'] = [ડેટા.decode() for ડેટા in 받은자료]
    (સ્થાન / 'build/규약시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    અમલ_કરો_આદેશ()
