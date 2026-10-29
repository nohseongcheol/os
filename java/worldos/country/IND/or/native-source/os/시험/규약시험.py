#!/usr/bin/env python3
"""ଆୟୋଜକ libc 없이 연결한 한국어 C 프로그램을 ପ୍ରକୃତ_ଡାଟା ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ବାସ୍ତବ_ମେସିନ୍

ଅବସ୍ଥାନ = Path(__file__).resolve().parents[1]

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ମାପ = {}
    ସର୍ଭର୍_ମୂଲ୍ୟ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ସର୍ଭର୍_ମୂଲ୍ୟ.bind(('127.0.0.1', 0))
    ସର୍ଭର୍_ମୂଲ୍ୟ.settimeout(0.1)
    ପୋର୍ଟ୍_ନମ୍ଵର୍ = ସର୍ଭର୍_ମୂଲ୍ୟ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ଡାଟା, ଠିକଣା = ସର୍ଭର୍_ମୂଲ୍ୟ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ଡାଟା)
            ସର୍ଭର୍_ମୂଲ୍ୟ.sendto(ଡାଟା, ଠିକଣା)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / ('build/kernel.' + 종류), 종류)
            try:
                for ବାରମ୍ବାର_ମୂଲ୍ୟ in range(2):
                    ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run posixudp ' + str(ପୋର୍ଟ୍_ନମ୍ଵର୍), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ଚଳାନ୍ତୁ = len(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
                ମେସିନ୍.직렬.sendall(b'run posixinput\n')
                ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('POSIX INPUT READY', ଚଳାନ୍ତୁ)
                ମେସିନ୍.직렬.sendall(b'abcdef')
                ନିର୍ଗମ = ମେସିନ୍.ଅପେକ୍ଷା_ସ୍ଥିତି('jkoros> ', ଚଳାନ୍ତୁ)
                assert 'POSIX INPUT PASS' in ନିର୍ଗମ and 'Exit: 0' in ନିର୍ଗମ, ନିର୍ଗମ
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('javac Hello.java', ['Exit: 0'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ମାପ[종류] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ଫାଇଲ/공유 ଅବସ୍ଥାନ/삭제 수명/ଠିକଣା ପ୍ରତିରୋଧ_ମୂଲ୍ୟ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ସର୍ଭର୍_ମୂଲ୍ୟ.close()
    ମାପ['host_datagrams'] = [ଡାଟା.decode() for ଡାଟା in 받은자료]
    (ଅବସ୍ଥାନ / 'build/규약시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
