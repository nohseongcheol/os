#!/usr/bin/env python3
"""ហូស libc 없이 연결한 한국어 C 프로그램을 ដែលពិត_ទិន្នន័យ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import និម្មិត_ម៉ាស៊ីន

កំណត់ទីតាំង = Path(__file__).resolve().parents[1]

def អនុវត្ត_ពាក្យបញ្ជា():
    ការវាស់វែង = {}
    ម៉ាស៊ីនមេ_តំលៃ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ម៉ាស៊ីនមេ_តំលៃ.bind(('127.0.0.1', 0))
    ម៉ាស៊ីនមេ_តំលៃ.settimeout(0.1)
    លេខរន្ធ = ម៉ាស៊ីនមេ_តំលៃ.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ទិន្នន័យ, អ៊ីម៉ែល = ម៉ាស៊ីនមេ_តំលៃ.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ទិន្នន័យ)
            ម៉ាស៊ីនមេ_តំលៃ.sendto(ទិន្នន័យ, អ៊ីម៉ែល)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / ('build/kernel.' + 종류), 종류)
            try:
                for ការធ្វើឡើងវិញ_តំលៃ in range(2):
                    ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run posixudp ' + str(លេខរន្ធ), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                រត់ = len(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
                ម៉ាស៊ីន.직렬.sendall(b'run posixinput\n')
                ម៉ាស៊ីន.រង់ចាំ_ភាព('POSIX INPUT READY', រត់)
                ម៉ាស៊ីន.직렬.sendall(b'abcdef')
                លទ្ធផល = ម៉ាស៊ីន.រង់ចាំ_ភាព('jkoros> ', រត់)
                assert 'POSIX INPUT PASS' in លទ្ធផល and 'Exit: 0' in លទ្ធផល, លទ្ធផល
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('javac Hello.java', ['Exit: 0'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ការវាស់វែង[종류] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ឯកសារ/공유 កំណត់ទីតាំង/삭제 수명/អ៊ីម៉ែល ការពារ_តំលៃ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ម៉ាស៊ីន.បិទ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); ម៉ាស៊ីនមេ_តំលៃ.close()
    ការវាស់វែង['host_datagrams'] = [ទិន្នន័យ.decode() for ទិន្នន័យ in 받은자료]
    (កំណត់ទីតាំង / 'build/규약시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    អនុវត្ត_ពាក្យបញ្ជា()
