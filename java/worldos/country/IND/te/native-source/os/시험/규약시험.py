#!/usr/bin/env python3
"""హోస్ట్ libc 없이 연결한 한국어 C 프로그램을 వాస్తవ_డేటా ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import వర్చువల్_యంత్రం

స్థానము = Path(__file__).resolve().parents[1]

def అమలు_చేయి_ఆదేశం():
    ప్రమాణం = {}
    సర్వర్_మూల్యం = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    సర్వర్_మూల్యం.bind(('127.0.0.1', 0))
    సర్వర్_మూల్యం.settimeout(0.1)
    పోర్ట్_సంఖ్య = సర్వర్_మూల్యం.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                డేటా, ఇమెయిల్ = సర్వర్_మూల్యం.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(డేటా)
            సర్వర్_మూల్యం.sendto(డేటా, ఇమెయిల్)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            యంత్రం = వర్చువల్_యంత్రం(స్థానము / ('build/kernel.' + 종류), 종류)
            try:
                for పునరావృతం_మూల్యం in range(2):
                    యంత్రం.ఆదేశము('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    యంత్రం.ఆదేశము('run posixudp ' + str(పోర్ట్_సంఖ్య), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                నడుపుము = len(యంత్రం.లాగ్_వరుస)
                యంత్రం.직렬.sendall(b'run posixinput\n')
                యంత్రం.వేచియుండు_స్థితి('POSIX INPUT READY', నడుపుము)
                యంత్రం.직렬.sendall(b'abcdef')
                అవుట్పుట్ = యంత్రం.వేచియుండు_స్థితి('jkoros> ', నడుపుము)
                assert 'POSIX INPUT PASS' in అవుట్పుట్ and 'Exit: 0' in అవుట్పుట్, అవుట్పుట్
                యంత్రం.ఆదేశము('javac Hello.java', ['Exit: 0'])
                యంత్రం.ఆదేశము('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                యంత్రం.ఆదేశము('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ప్రమాణం[종류] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX దస్త్రం/공유 స్థానము/삭제 수명/ఇమెయిల్ రక్షించు_మూల్యం/UDP/표준 입력/기존 Java', flush=True)
            finally:
                యంత్రం.మూసివేయి()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); సర్వర్_మూల్యం.close()
    ప్రమాణం['host_datagrams'] = [డేటా.decode() for డేటా in 받은자료]
    (స్థానము / 'build/규약시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    అమలు_చేయి_ఆదేశం()
