#!/usr/bin/env python3
"""ධාරකය libc 없이 연결한 한국어 C 프로그램을 තථ්_ය_දත්ත ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import අතථ්_ය_යන්ත්_රය

පිහිටීම = Path(__file__).resolve().parents[1]

def ක්_රියාත්මක_කරන්න_විධානය():
    결과 = {}
    සේවාදායකය_අගය = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    සේවාදායකය_අගය.bind(('127.0.0.1', 0))
    සේවාදායකය_අගය.settimeout(0.1)
    접속번호 = සේවාදායකය_අගය.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                දත්ත, යොමුව = සේවාදායකය_අගය.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(දත්ත)
            සේවාදායකය_අගය.sendto(දත්ත, යොමුව)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / ('build/kernel.' + 종류), 종류)
            try:
                for පුනර්කරණය_අගය in range(2):
                    යන්ත්_රය.විධානය('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    යන්ත්_රය.විධානය('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ක්_රියාත්මක_කරන්න_2 = len(යන්ත්_රය.ලොගය_පේළිය)
                යන්ත්_රය.직렬.sendall(b'run posixinput\n')
                යන්ත්_රය.기다림('POSIX INPUT READY', ක්_රියාත්මක_කරන්න_2)
                යන්ත්_රය.직렬.sendall(b'abcdef')
                출력 = යන්ත්_රය.기다림('jkoros> ', ක්_රියාත්මක_කරන්න_2)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                යන්ත්_රය.විධානය('javac Hello.java', ['Exit: 0'])
                යන්ත්_රය.විධානය('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                යන්ත්_රය.විධානය('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ගොනු/공유 පිහිටීම/삭제 수명/යොමුව ආරක්ෂා_කරන්න_අගය/UDP/표준 입력/기존 Java', flush=True)
            finally:
                යන්ත්_රය.වසන්න()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); සේවාදායකය_අගය.close()
    결과['host_datagrams'] = [දත්ත.decode() for දත්ත in 받은자료]
    (පිහිටීම / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_විධානය()
