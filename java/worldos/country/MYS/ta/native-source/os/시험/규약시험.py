#!/usr/bin/env python3
"""ஓம்பு libc 없이 연결한 தமிழ் C 프로그램을 அசல்_தரவு ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import தோற்றநிலை_இயந்திரம்

இடம் = Path(__file__).resolve().parents[1]

def இயக்கு_கட்டளை():
    அளவிடக்கூடியது = {}
    சேவையகம்_மதிப்பு = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    சேவையகம்_மதிப்பு.bind(('127.0.0.1', 0))
    சேவையகம்_மதிப்பு.settimeout(0.1)
    முனைய_எண் = சேவையகம்_மதிப்பு.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                தரவு, முகவரி = சேவையகம்_மதிப்பு.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(தரவு)
            சேவையகம்_மதிப்பு.sendto(தரவு, முகவரி)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / ('build/kernel.' + 종류), 종류)
            try:
                for மீள்செயல்_மதிப்பு in range(2):
                    இயந்திரம்.கட்டளை('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    இயந்திரம்.கட்டளை('run posixudp ' + str(முனைய_எண்), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                செயல்படுத்துக = len(இயந்திரம்.பதிவு_பதிவு)
                இயந்திரம்.직렬.sendall(b'run posixinput\n')
                இயந்திரம்.காத்திரு_நிலை('POSIX INPUT READY', செயல்படுத்துக)
                இயந்திரம்.직렬.sendall(b'abcdef')
                வெளியீட்டு_இடம் = இயந்திரம்.காத்திரு_நிலை('jkoros> ', செயல்படுத்துக)
                assert 'POSIX INPUT PASS' in வெளியீட்டு_இடம் and 'Exit: 0' in வெளியீட்டு_இடம், வெளியீட்டு_இடம்
                இயந்திரம்.கட்டளை('javac Hello.java', ['Exit: 0'])
                இயந்திரம்.கட்டளை('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                இயந்திரம்.கட்டளை('run hello recovered', ['arg: recovered', 'Exit: 0'])
                அளவிடக்கூடியது[종류] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX கோப்பின்_பெயர்/공유 இடம்/삭제 수명/முகவரி பாதுகாப்பளி_மதிப்பு/UDP/표준 입력/기존 Java', flush=True)
            finally:
                இயந்திரம்.மூடு()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); சேவையகம்_மதிப்பு.close()
    அளவிடக்கூடியது['host_datagrams'] = [தரவு.decode() for தரவு in 받은자료]
    (இடம் / 'build/규약시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    இயக்கு_கட்டளை()
