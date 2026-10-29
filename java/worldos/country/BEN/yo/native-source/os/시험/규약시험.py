#!/usr/bin/env python3
"""olùpèsè libc 없이 연결한 한국어 C 프로그램을 gangan_détà ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import àfojúunúṣe_maṣíìnì

위치 = Path(__file__).resolve().parents[1]

def ṣiṣẹ́_àṣẹ():
    결과 = {}
    apèsè_iye = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    apèsè_iye.bind(('127.0.0.1', 0))
    apèsè_iye.settimeout(0.1)
    접속번호 = apèsè_iye.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                détà, àdírẹ́ẹ̀sì = apèsè_iye.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(détà)
            apèsè_iye.sendto(détà, àdírẹ́ẹ̀sì)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for àṣetúnṣe_iye in range(2):
                    maṣíìnì.Àṣẹ('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    maṣíìnì.Àṣẹ('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Rọ́ọ̀nù = len(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
                maṣíìnì.직렬.sendall(b'run posixinput\n')
                maṣíìnì.기다림('POSIX INPUT READY', Rọ́ọ̀nù)
                maṣíìnì.직렬.sendall(b'abcdef')
                출력 = maṣíìnì.기다림('jkoros> ', Rọ́ọ̀nù)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                maṣíìnì.Àṣẹ('javac Hello.java', ['Exit: 0'])
                maṣíìnì.Àṣẹ('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                maṣíìnì.Àṣẹ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Fáìlì/공유 위치/삭제 수명/àdírẹ́ẹ̀sì dáàbòbò_iye/UDP/표준 입력/기존 Java', flush=True)
            finally:
                maṣíìnì.Ti()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); apèsè_iye.close()
    결과['host_datagrams'] = [détà.decode() for détà in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ṣiṣẹ́_àṣẹ()
