#!/usr/bin/env python3
"""میزبان libc 없이 연결한 فارسی C 프로그램을 واقعی_داده_ها ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import مجازی_دستگاه

مرتب_کردن = Path(__file__).resolve().parents[1]

def اجرا_فرمان():
    سنجش = {}
    سرور_مقدار = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_مقدار.bind(('127.0.0.1', 0))
    سرور_مقدار.settimeout(0.1)
    شماره_درگاه = سرور_مقدار.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                داده_ها, آدرس = سرور_مقدار.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(داده_ها)
            سرور_مقدار.sendto(داده_ها, آدرس)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            دستگاه = مجازی_دستگاه(مرتب_کردن / ('build/kernel.' + 종류), 종류)
            try:
                for تکرار_مقدار in range(2):
                    دستگاه.فرمان('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    دستگاه.فرمان('run posixudp ' + str(شماره_درگاه), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                اجرا_2 = len(دستگاه.واقعه_نگار_ردیف)
                دستگاه.직렬.sendall(b'run posixinput\n')
                دستگاه.منتظر_ماندن_وضعیت('POSIX INPUT READY', اجرا_2)
                دستگاه.직렬.sendall(b'abcdef')
                خروجی = دستگاه.منتظر_ماندن_وضعیت('jkoros> ', اجرا_2)
                assert 'POSIX INPUT PASS' in خروجی and 'Exit: 0' in خروجی, خروجی
                دستگاه.فرمان('javac Hello.java', ['Exit: 0'])
                دستگاه.فرمان('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                دستگاه.فرمان('run hello recovered', ['arg: recovered', 'Exit: 0'])
                سنجش[종류] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX پرونده/공유 مرتب_کردن/삭제 수명/آدرس حفاظت_کردن_مقدار/UDP/표준 입력/기존 Java', flush=True)
            finally:
                دستگاه.بستن()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); سرور_مقدار.close()
    سنجش['host_datagrams'] = [داده_ها.decode() for داده_ها in 받은자료]
    (مرتب_کردن / 'build/규약시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    اجرا_فرمان()
