#!/usr/bin/env python3
"""ᎠᏁᏢᏍᎩ libc 없이 연결한 한국어 C 프로그램을 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from ᎠᏓᎪᎵᏰᏍᎩ_ᎬᏗᏍᎩ_ᏧᎾᏚᏓᎵ import 가상기계

위치 = Path(__file__).resolve().parents[1]

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    결과 = {}
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.1', 0))
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.settimeout(0.1)
    접속번호 = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ᎦᏟᏌᏅᎯ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ᎦᏟᏌᏅᎯ)
            ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendto(ᎦᏟᏌᏅᎯ, ᎪᏪᎵ_ᏫᏗᎦᏅᏗ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for 반복 in range(2):
                    기계.ᎤᏁᏤᎸᎩ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.ᎤᏁᏤᎸᎩ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ᎠᎢᏎᏍᏗ = len(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', ᎠᎢᏎᏍᏗ)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', ᎠᎢᏎᏍᏗ)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.ᎤᏁᏤᎸᎩ('javac Hello.java', ['Exit: 0'])
                기계.ᎤᏁᏤᎸᎩ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.ᎤᏁᏤᎸᎩ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ᎠᏍᏆᏂᎪᏙᏗ/공유 위치/삭제 수명/ᎪᏪᎵ_ᏫᏗᎦᏅᏗ ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.ᎯᏍᏚᎲᎦ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.close()
    결과['host_datagrams'] = [ᎦᏟᏌᏅᎯ.decode() for ᎦᏟᏌᏅᎯ in 받은자료]
    (위치 / 'build/ᎢᏳᎵᏍᏔᏅᎢ_ᎠᏓᎪᎵᏰᏍᎩ.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
