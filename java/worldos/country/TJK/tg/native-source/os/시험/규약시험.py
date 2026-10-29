#!/usr/bin/env python3
"""мизбон libc 없이 연결한 한국어 C 프로그램을 воқеӣ_иттилоот ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import виртуалӣ_компютер

위치 = Path(__file__).resolve().parents[1]

def иҷро_кардан_фармон():
    결과 = {}
    сервер_қимат = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_қимат.bind(('127.0.0.1', 0))
    сервер_қимат.settimeout(0.1)
    접속번호 = сервер_қимат.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                иттилоот, суроға = сервер_қимат.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(иттилоот)
            сервер_қимат.sendto(иттилоот, суроға)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компютер = виртуалӣ_компютер(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for такрор_қимат in range(2):
                    компютер.фармон('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    компютер.фармон('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                порча = len(компютер.сабт_кардан_сабт)
                компютер.직렬.sendall(b'run posixinput\n')
                компютер.기다림('POSIX INPUT READY', порча)
                компютер.직렬.sendall(b'abcdef')
                출력 = компютер.기다림('jkoros> ', порча)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                компютер.фармон('javac Hello.java', ['Exit: 0'])
                компютер.фармон('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                компютер.фармон('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Файл/공유 위치/삭제 수명/суроға муҳофизат_кардан_қимат/UDP/표준 입력/기존 Java', flush=True)
            finally:
                компютер.Пӯшидан()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); сервер_қимат.close()
    결과['host_datagrams'] = [иттилоот.decode() for иттилоот in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    иҷро_кардан_фармон()
