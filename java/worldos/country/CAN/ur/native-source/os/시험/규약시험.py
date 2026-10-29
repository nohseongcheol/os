#!/usr/bin/env python3
"""میزبان libc 없이 연결한 اردو C 프로그램을 اصل_کوائف ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import مجازی_مشین

مقام = Path(__file__).resolve().parents[1]

def نفاذ_کریں_حکم():
    پیمائش = {}
    سرور_قدر = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_قدر.bind(('127.0.0.1', 0))
    سرور_قدر.settimeout(0.1)
    دہانہ_نمبر = سرور_قدر.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                کوائف, پتہ = سرور_قدر.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(کوائف)
            سرور_قدر.sendto(کوائف, پتہ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مشین = مجازی_مشین(مقام / ('build/kernel.' + 종류), 종류)
            try:
                for تکرار_قدر in range(2):
                    مشین.حکم('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    مشین.حکم('run posixudp ' + str(دہانہ_نمبر), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                چلائیں = len(مشین.لاگ_صف)
                مشین.직렬.sendall(b'run posixinput\n')
                مشین.انتظار_حالت('POSIX INPUT READY', چلائیں)
                مشین.직렬.sendall(b'abcdef')
                اخراج_کا_مقام = مشین.انتظار_حالت('jkoros> ', چلائیں)
                assert 'POSIX INPUT PASS' in اخراج_کا_مقام and 'Exit: 0' in اخراج_کا_مقام, اخراج_کا_مقام
                مشین.حکم('javac Hello.java', ['Exit: 0'])
                مشین.حکم('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                مشین.حکم('run hello recovered', ['arg: recovered', 'Exit: 0'])
                پیمائش[종류] = مشین.لاگ_صف.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX فائل_کا_نام/공유 مقام/삭제 수명/پتہ بچانا_قدر/UDP/표준 입력/기존 Java', flush=True)
            finally:
                مشین.بند_کریں()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); سرور_قدر.close()
    پیمائش['host_datagrams'] = [کوائف.decode() for کوائف in 받은자료]
    (مقام / 'build/규약시험.json').write_text(json.dumps(پیمائش, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    نفاذ_کریں_حکم()
