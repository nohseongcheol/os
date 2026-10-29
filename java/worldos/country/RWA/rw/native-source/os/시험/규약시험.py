#!/usr/bin/env python3
"""gucumbikira libc 없이 연결한 Ikinyarwanda C 프로그램을 nyakuri_amakurushingiro ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import kidafatika_imashini

위치 = Path(__file__).resolve().parents[1]

def gukora_ibwiriza():
    결과 = {}
    seriveri_agaciro = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seriveri_agaciro.bind(('127.0.0.1', 0))
    seriveri_agaciro.settimeout(0.1)
    접속번호 = seriveri_agaciro.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                amakurushingiro, aderesi = seriveri_agaciro.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(amakurushingiro)
            seriveri_agaciro.sendto(amakurushingiro, aderesi)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            imashini = kidafatika_imashini(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for isubiramo_agaciro in range(2):
                    imashini.Icyo_wifuza('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    imashini.Icyo_wifuza('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ihuriro = len(imashini.kubika_umurongo)
                imashini.직렬.sendall(b'run posixinput\n')
                imashini.기다림('POSIX INPUT READY', ihuriro)
                imashini.직렬.sendall(b'abcdef')
                출력 = imashini.기다림('jkoros> ', ihuriro)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                imashini.Icyo_wifuza('javac Hello.java', ['Exit: 0'])
                imashini.Icyo_wifuza('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                imashini.Icyo_wifuza('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = imashini.kubika_umurongo.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX Idosiye/공유 위치/삭제 수명/aderesi kurinda_agaciro/UDP/표준 입력/기존 Java', flush=True)
            finally:
                imashini.Gufunga()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); seriveri_agaciro.close()
    결과['host_datagrams'] = [amakurushingiro.decode() for amakurushingiro in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    gukora_ibwiriza()
