#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. आयोजक 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from निष्पादित_करें_आदेश import आदेश


def चलाएँ():
    पार्सर = argparse.ArgumentParser(description=__doc__)
    पार्सर.add_argument('file', type=Path)
    पार्सर.add_argument('arguments', nargs='*')
    पार्सर.add_argument('--class-name', help='패키지가 있는 .class의 전체 नाम(예: मान्य_करें.꾸러미시험)')
    पार्सर.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    पार्सर.add_argument('--vnc', help='예: 127.0.0.1:2')
    पार्सर.add_argument('--include', action='append', type=Path, default=[], help='जोड़ें_एन्ट्री class संचिका 또는 class 디렉터리(패키지 नाम 유지)')
    तर्क_सरणी = पार्सर.parse_args()
    आँकड़े = तर्क_सरणी.file.read_bytes()
    if तर्क_सरणी.class_name and तर्क_सरणी.file.suffix != '.class': पार्सर.error('--class-name은 .class 입력에서 사용합니다.')
    नाम = तर्क_सरणी.class_name + '.class' if तर्क_सरणी.class_name else तर्क_सरणी.file.name
    if len(आँकड़े) > 16384 or not 1 <= len(नाम.encode('utf-8')) <= 63 or '\n' in नाम or '\r' in नाम:
        पार्सर.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    श्रेणी_मान = '.elf' if आँकड़े[:4] == b'\x7fELF' else तर्क_सरणी.file.suffix
    if तर्क_सरणी.linux and श्रेणी_मान != '.elf': पार्सर.error('--linux는 ELF 바이너리에만 사용합니다.')
    if श्रेणी_मान not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        पार्सर.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(तर्क_सरणी.arguments) > 7 or any(len(स्ट्रिंग_डेटा.encode('utf-8')) > 255 or '\n' in स्ट्रिंग_डेटा or '\r' in स्ट्रिंग_डेटा for स्ट्रिंग_डेटा in तर्क_सरणी.arguments):
        पार्सर.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    विकल्प = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if तर्क_सरणी.vnc: विकल्प += ['-vnc', तर्क_सरणी.vnc]
    प्रक्रिया = subprocess.Popen(आदेश() + विकल्प, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    सिलेक्टर = selectors.DefaultSelector(); सिलेक्टर.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    def 수신하기(मार्कर, 시간제한=45):
        출력결과 = bytearray(); समाप्त_करें_ऑफ़सेट = time.monotonic() + 시간제한
        while मार्कर not in 출력결과:
            if time.monotonic() > समाप्त_करें_ऑफ़सेट: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in सिलेक्टर.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if प्रक्रिया.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def भेजें(पंक्ति, मार्कर=b'jkoros-native> '):
        प्रक्रिया.stdin.write(पंक्ति.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
        return 수신하기(मार्कर)
    def निष्पादित_करें_आदेश(पंक्ति):
        출력결과 = भेजें(पंक्ति); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        फ़ाइल_सूची = []
        for 포함항목 in तर्क_सरणी.include:
            if 포함항목.is_dir():
                फ़ाइल_सूची += [(str(डेटा_पद.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', डेटा_पद.read_bytes()) for डेटा_पद in sorted(포함항목.rglob('*.class'))]
            else:
                फ़ाइल_सूची.append((포함항목.name, 포함항목.read_bytes()))
        फ़ाइल_सूची = [(개수, गंतव्य_डेटा) for 개수, गंतव्य_डेटा in फ़ाइल_सूची if 개수 != नाम] + [(नाम, आँकड़े)]
        for अपलोड_नाम, अपलोड_डेटा in फ़ाइल_सूची:
            if len(अपलोड_डेटा) > 16384 or len(अपलोड_नाम.encode('utf-8')) > 63 or '\n' in अपलोड_नाम or '\r' in अपलोड_नाम:
                raise ValueError('जोड़ें_एन्ट्री 파일의 नाम/आकार 제한 초과: ' + अपलोड_नाम)
            भेजें('load ' + shlex.quote(अपलोड_नाम), b'hex> ')
            for 순번 in range(0, len(अपलोड_डेटा), 64): भेजें(अपलोड_डेटा[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in भेजें('.'): raise RuntimeError('upload failed: ' + अपलोड_नाम)
            갈무리자료 = भेजें('hex ' + shlex.quote(अपलोड_नाम))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != अपलोड_डेटा: raise RuntimeError('upload verification failed')
        if श्रेणी_मान == '.java' and निष्पादित_करें_आदेश('javac ' + shlex.quote(नाम)) != 0: return 1
        निष्पादन_योग्य_फ़ाइल_छवि = तर्क_सरणी.file.stem + '.elf'
        if श्रेणी_मान == '.c' and निष्पादित_करें_आदेश('cc ' + shlex.quote(नाम) + ' -o ' + shlex.quote(निष्पादन_योग्य_फ़ाइल_छवि)) != 0: return 1
        ऐप = 'java ' + shlex.quote(तर्क_सरणी.class_name or तर्क_सरणी.file.stem) if श्रेणी_मान in ('.java', '.class') else ('python ' if श्रेणी_मान == '.py' else 'run ') + shlex.quote(नाम)
        if श्रेणी_मान == '.jar': ऐप = 'java -jar ' + shlex.quote(नाम)
        if श्रेणी_मान == '.c': ऐप = 'run ' + shlex.quote(निष्पादन_योग्य_फ़ाइल_छवि)
        if तर्क_सरणी.linux: ऐप = 'run --linux ' + shlex.quote(नाम)
        if तर्क_सरणी.arguments: ऐप += ' ' + ' '.join(shlex.quote(स्ट्रिंग_डेटा) for स्ट्रिंग_डेटा in तर्क_सरणी.arguments)
        return 0 if निष्पादित_करें_आदेश(ऐप) == 0 else 1
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
        सिलेक्टर.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()


if __name__ == '__main__':
    raise SystemExit(चलाएँ())
