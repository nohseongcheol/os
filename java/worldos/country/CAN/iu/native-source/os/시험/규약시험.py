#!/usr/bin/env python3
"""tuttarvik libc 없이 연결한 한국어 C 프로그램을 taannallarik_titiqqat ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import 가상기계

위치 = Path(__file__).resolve().parents[1]

def 실행():
    결과 = {}
    ikiaqqitittivik_atuutilik = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ikiaqqitittivik_atuutilik.bind(('127.0.0.1', 0))
    ikiaqqitittivik_atuutilik.settimeout(0.1)
    접속번호 = ikiaqqitittivik_atuutilik.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                titiqqat, turaarut = ikiaqqitittivik_atuutilik.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(titiqqat)
            ikiaqqitittivik_atuutilik.sendto(titiqqat, turaarut)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for utiqtaqtuq_atuutilik in range(2):
                    기계.piqujijjut('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    기계.piqujijjut('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                시작 = len(기계.papattivik_sanimukutaak)
                기계.직렬.sendall(b'run posixinput\n')
                기계.기다림('POSIX INPUT READY', 시작)
                기계.직렬.sendall(b'abcdef')
                출력 = 기계.기다림('jkoros> ', 시작)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                기계.piqujijjut('javac Hello.java', ['Exit: 0'])
                기계.piqujijjut('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                기계.piqujijjut('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ini/공유 위치/삭제 수명/turaarut pijjairli_atuutilik/UDP/표준 입력/기존 Java', flush=True)
            finally:
                기계.matuli()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ikiaqqitittivik_atuutilik.close()
    결과['host_datagrams'] = [titiqqat.decode() for titiqqat in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    실행()
