#!/usr/bin/env python3
"""جێدەر libc 없이 연결한 한국어 C 프로그램을 ڕاستەکی_دەیتا ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import مەجازی_مەکینه

위치 = Path(__file__).resolve().parents[1]

def جێبەجێکردن_فەرمان():
    결과 = {}
    ڕاژەکار_نرخ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ڕاژەکار_نرخ.bind(('127.0.0.1', 0))
    ڕاژەکار_نرخ.settimeout(0.1)
    접속번호 = ڕاژەکار_نرخ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                دەیتا, ناونیشان = ڕاژەکار_نرخ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(دەیتا)
            ڕاژەکار_نرخ.sendto(دەیتا, ناونیشان)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مەکینه = مەجازی_مەکینه(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for دووبارەکردنەوە_نرخ in range(2):
                    مەکینه.فەرمان('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    مەکینه.فەرمان('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ڕادان = len(مەکینه.تۆمار_ڕزن)
                مەکینه.직렬.sendall(b'run posixinput\n')
                مەکینه.چاوەڕوان_کردن_دۆخ('POSIX INPUT READY', ڕادان)
                مەکینه.직렬.sendall(b'abcdef')
                출력 = مەکینه.چاوەڕوان_کردن_دۆخ('jkoros> ', ڕادان)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                مەکینه.فەرمان('javac Hello.java', ['Exit: 0'])
                مەکینه.فەرمان('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                مەکینه.فەرمان('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX فایل/공유 위치/삭제 수명/ناونیشان پاراستن_نرخ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                مەکینه.داخستن()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ڕاژەکار_نرخ.close()
    결과['host_datagrams'] = [دەیتا.decode() for دەیتا in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    جێبەجێکردن_فەرمان()
