#!/usr/bin/env python3
"""হ_ষ্ট libc 없이 연결한 한국어 C 프로그램을 প্ৰকৃত_ডাটা ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ভাৰ্ছুৱেল_মেচিন

অৱস্থান = Path(__file__).resolve().parents[1]

def নিষ্পাদন_আদেশ():
    পৰিমাপ = {}
    ছাৰ্ভাৰ_মান = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ছাৰ্ভাৰ_মান.bind(('127.0.0.1', 0))
    ছাৰ্ভাৰ_মান.settimeout(0.1)
    접속번호 = ছাৰ্ভাৰ_মান.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ডাটা, ঠিকনা = ছাৰ্ভাৰ_মান.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ডাটা)
            ছাৰ্ভাৰ_মান.sendto(ডাটা, ঠিকনা)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / ('build/kernel.' + 종류), 종류)
            try:
                for পুণৰাবৃত্তি_মান in range(2):
                    মেচিন.কমান্ড('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    মেচিন.কমান্ড('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                সঞ্চালন = len(মেচিন.লগ_শাৰী)
                মেচিন.직렬.sendall(b'run posixinput\n')
                মেচিন.기다림('POSIX INPUT READY', সঞ্চালন)
                মেচিন.직렬.sendall(b'abcdef')
                নিৰ্গম = মেচিন.기다림('jkoros> ', সঞ্চালন)
                assert 'POSIX INPUT PASS' in নিৰ্গম and 'Exit: 0' in নিৰ্গম, নিৰ্গম
                মেচিন.কমান্ড('javac Hello.java', ['Exit: 0'])
                মেচিন.কমান্ড('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                মেচিন.কমান্ড('run hello recovered', ['arg: recovered', 'Exit: 0'])
                পৰিমাপ[종류] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX নথিপত্ৰ/공유 অৱস্থান/삭제 수명/ঠিকনা প্রতিৰোধ_কৰক_মান/UDP/표준 입력/기존 Java', flush=True)
            finally:
                মেচিন.বন্ধ_কৰক()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ছাৰ্ভাৰ_মান.close()
    পৰিমাপ['host_datagrams'] = [ডাটা.decode() for ডাটা in 받은자료]
    (অৱস্থান / 'build/규약시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    নিষ্পাদন_আদেশ()
