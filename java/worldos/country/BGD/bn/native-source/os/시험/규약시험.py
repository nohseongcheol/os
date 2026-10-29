#!/usr/bin/env python3
"""হোস্ট libc 없이 연결한 বাংলা C 프로그램을 প্রকৃত_ডাটা ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import কল্পিত_মেশিন

অবস্থান = Path(__file__).resolve().parents[1]

def কার্যকর_করুন_আদেশ():
    পরিমাপ = {}
    সার্ভার_মান = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    সার্ভার_মান.bind(('127.0.0.1', 0))
    সার্ভার_মান.settimeout(0.1)
    পোর্ট_নম্বর = সার্ভার_মান.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ডাটা, ইমেইল = সার্ভার_মান.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ডাটা)
            সার্ভার_মান.sendto(ডাটা, ইমেইল)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            মেশিন = কল্পিত_মেশিন(অবস্থান / ('build/kernel.' + 종류), 종류)
            try:
                for পুনরুক্তি_মান in range(2):
                    মেশিন.আদেশ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    মেশিন.আদেশ('run posixudp ' + str(পোর্ট_নম্বর), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                চালনা = len(মেশিন.লগ_সারি)
                মেশিন.직렬.sendall(b'run posixinput\n')
                মেশিন.অপেক্ষা_অবস্হা('POSIX INPUT READY', চালনা)
                মেশিন.직렬.sendall(b'abcdef')
                নির্গম = মেশিন.অপেক্ষা_অবস্হা('jkoros> ', চালনা)
                assert 'POSIX INPUT PASS' in নির্গম and 'Exit: 0' in নির্গম, নির্গম
                মেশিন.আদেশ('javac Hello.java', ['Exit: 0'])
                মেশিন.আদেশ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                মেশিন.আদেশ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                পরিমাপ[종류] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX নথির_নাম/공유 অবস্থান/삭제 수명/ইমেইল রক্ষা_করুন_মান/UDP/표준 입력/기존 Java', flush=True)
            finally:
                মেশিন.বন্ধ_করুন()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); সার্ভার_মান.close()
    পরিমাপ['host_datagrams'] = [ডাটা.decode() for ডাটা in 받은자료]
    (অবস্থান / 'build/규약시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    কার্যকর_করুন_আদেশ()
