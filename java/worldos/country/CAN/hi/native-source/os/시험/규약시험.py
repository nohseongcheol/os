#!/usr/bin/env python3
"""आयोजक libc 없이 연결한 हिंदी C 프로그램을 वास्तविक_डेटा ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import वर्चुअल_मशीन

स्थान = Path(__file__).resolve().parents[1]

def निष्पादित_करें_आदेश():
    परिणाम = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    पोर्ट_संख्या = 서버.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def प्रतिध्वनि_उत्तर():
        while not 끝냄.is_set():
            try:
                आँकड़े, पता = 서버.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(आँकड़े)
            서버.sendto(आँकड़े, पता)
    일꾼 = threading.Thread(target=प्रतिध्वनि_उत्तर, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            यंत्र = वर्चुअल_मशीन(स्थान / ('build/kernel.' + 종류), 종류)
            try:
                for पुनरावृति_मान in range(2):
                    यंत्र.आदेश('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    यंत्र.आदेश('run posixudp ' + str(पोर्ट_संख्या), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                चलाएँ = len(यंत्र.लॉग_रिकॉर्ड)
                यंत्र.직렬.sendall(b'run posixinput\n')
                यंत्र.प्रतीक्षा_स्थिति('POSIX INPUT READY', चलाएँ)
                यंत्र.직렬.sendall(b'abcdef')
                निर्गम = यंत्र.प्रतीक्षा_स्थिति('jkoros> ', चलाएँ)
                assert 'POSIX INPUT PASS' in निर्गम and 'Exit: 0' in निर्गम, निर्गम
                यंत्र.आदेश('javac Hello.java', ['Exit: 0'])
                यंत्र.आदेश('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                यंत्र.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                परिणाम[종류] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX संचिका/공유 स्थान/삭제 수명/पता रक्षित_करें_मान/UDP/표준 입력/기존 Java', flush=True)
            finally:
                यंत्र.बंदकरें()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); 서버.close()
    परिणाम['host_datagrams'] = [आँकड़े.decode() for आँकड़े in 받은자료]
    (स्थान / 'build/규약시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    निष्पादित_करें_आदेश()
