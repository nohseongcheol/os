#!/usr/bin/env python3
"""umsingathi libc 없이 연결한 isiXhosa C 프로그램을 eyona_yenzekileyo_iingcombolo ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import enembonakalo_yenyani_umatshini

위치 = Path(__file__).resolve().parents[1]

def ukwenza_umyalelo():
    결과 = {}
    iseva_ixabiso = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    iseva_ixabiso.bind(('127.0.0.1', 0))
    iseva_ixabiso.settimeout(0.1)
    접속번호 = iseva_ixabiso.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                iingcombolo, idilesi = iseva_ixabiso.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(iingcombolo)
            iseva_ixabiso.sendto(iingcombolo, idilesi)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            umatshini = enembonakalo_yenyani_umatshini(위치 / ('build/kernel.' + 종류), 종류)
            try:
                for uniko_lomyalelo_omnye_ixabiso in range(2):
                    umatshini.Umyalelo('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    umatshini.Umyalelo('run posixudp ' + str(접속번호), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                Phumeza = len(umatshini.ilog_umqolo)
                umatshini.직렬.sendall(b'run posixinput\n')
                umatshini.기다림('POSIX INPUT READY', Phumeza)
                umatshini.직렬.sendall(b'abcdef')
                출력 = umatshini.기다림('jkoros> ', Phumeza)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                umatshini.Umyalelo('javac Hello.java', ['Exit: 0'])
                umatshini.Umyalelo('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                umatshini.Umyalelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX iFayili/공유 위치/삭제 수명/idilesi khusela_ixabiso/UDP/표준 입력/기존 Java', flush=True)
            finally:
                umatshini.Vala()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); iseva_ixabiso.close()
    결과['host_datagrams'] = [iingcombolo.decode() for iingcombolo in 받은자료]
    (위치 / 'build/규약시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ukwenza_umyalelo()
