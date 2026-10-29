#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. होस्ट 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from कार्यान्वयन_गर्नुहोस्_आदेश import आदेश


def चलाउनुहोस्():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 नाम(예: वैध_गर्नुहोस्.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class फाइल 또는 class 디렉터리(패키지 नाम 유지)')
    तर्क_विन्यास = 인수해석기.parse_args()
    लगत = तर्क_विन्यास.file.read_bytes()
    if तर्क_विन्यास.class_name and तर्क_विन्यास.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    नाम = तर्क_विन्यास.class_name + '.class' if तर्क_विन्यास.class_name else तर्क_विन्यास.file.name
    if len(लगत) > 16384 or not 1 <= len(नाम.encode('utf-8')) <= 63 or '\n' in नाम or '\r' in नाम:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    कोटि_मान = '.elf' if लगत[:4] == b'\x7fELF' else तर्क_विन्यास.file.suffix
    if तर्क_विन्यास.linux and कोटि_मान != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if कोटि_मान not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(तर्क_विन्यास.arguments) > 7 or any(len(स्ट्रिङ_लगत.encode('utf-8')) > 255 or '\n' in स्ट्रिङ_लगत or '\r' in स्ट्रिङ_लगत for स्ट्रिङ_लगत in तर्क_विन्यास.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    विकल्पहरु = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if तर्क_विन्यास.vnc: विकल्पहरु += ['-vnc', तर्क_विन्यास.vnc]
    प्रक्रिया = subprocess.Popen(आदेश() + विकल्पहरु, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    चयनकर्ता = selectors.DefaultSelector(); चयनकर्ता.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); समाप्त_गर्नुहोस्_अफसेट = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > समाप्त_गर्नुहोस्_अफसेट: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in चयनकर्ता.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if प्रक्रिया.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def पठाउनुहोस्(रेखा, 확인표시=b'jkoros-native> '):
        प्रक्रिया.stdin.write(रेखा.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
        return 수신하기(확인표시)
    def कार्यान्वयन_गर्नुहोस्_आदेश(रेखा):
        출력결과 = पठाउनुहोस्(रेखा); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        फाइल_सूची = []
        for 포함항목 in तर्क_विन्यास.include:
            if 포함항목.is_dir():
                फाइल_सूची += [(str(लगत_राख्नुहोस्.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', लगत_राख्नुहोस्.read_bytes()) for लगत_राख्नुहोस् in sorted(포함항목.rglob('*.class'))]
            else:
                फाइल_सूची.append((포함항목.name, 포함항목.read_bytes()))
        फाइल_सूची = [(개수, गन्तव्य_लगत) for 개수, गन्तव्य_लगत in फाइल_सूची if 개수 != नाम] + [(नाम, लगत)]
        for अपलोड_गर्नुहोस्_नाम, अपलोड_गर्नुहोस्_लगत in फाइल_सूची:
            if len(अपलोड_गर्नुहोस्_लगत) > 16384 or len(अपलोड_गर्नुहोस्_नाम.encode('utf-8')) > 63 or '\n' in अपलोड_गर्नुहोस्_नाम or '\r' in अपलोड_गर्नुहोस्_नाम:
                raise ValueError('추가 파일의 नाम/आकार 제한 초과: ' + अपलोड_गर्नुहोस्_नाम)
            पठाउनुहोस्('load ' + shlex.quote(अपलोड_गर्नुहोस्_नाम), b'hex> ')
            for 순번 in range(0, len(अपलोड_गर्नुहोस्_लगत), 64): पठाउनुहोस्(अपलोड_गर्नुहोस्_लगत[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in पठाउनुहोस्('.'): raise RuntimeError('upload failed: ' + अपलोड_गर्नुहोस्_नाम)
            갈무리자료 = पठाउनुहोस्('hex ' + shlex.quote(अपलोड_गर्नुहोस्_नाम))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != अपलोड_गर्नुहोस्_लगत: raise RuntimeError('upload verification failed')
        if कोटि_मान == '.java' and कार्यान्वयन_गर्नुहोस्_आदेश('javac ' + shlex.quote(नाम)) != 0: return 1
        실행가능파일 = तर्क_विन्यास.file.stem + '.elf'
        if कोटि_मान == '.c' and कार्यान्वयन_गर्नुहोस्_आदेश('cc ' + shlex.quote(नाम) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        अनुप्रयोग = 'java ' + shlex.quote(तर्क_विन्यास.class_name or तर्क_विन्यास.file.stem) if कोटि_मान in ('.java', '.class') else ('python ' if कोटि_मान == '.py' else 'run ') + shlex.quote(नाम)
        if कोटि_मान == '.jar': अनुप्रयोग = 'java -jar ' + shlex.quote(नाम)
        if कोटि_मान == '.c': अनुप्रयोग = 'run ' + shlex.quote(실행가능파일)
        if तर्क_विन्यास.linux: अनुप्रयोग = 'run --linux ' + shlex.quote(नाम)
        if तर्क_विन्यास.arguments: अनुप्रयोग += ' ' + ' '.join(shlex.quote(स्ट्रिङ_लगत) for स्ट्रिङ_लगत in तर्क_विन्यास.arguments)
        return 0 if कार्यान्वयन_गर्नुहोस्_आदेश(अनुप्रयोग) == 0 else 1
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
        चयनकर्ता.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()


if __name__ == '__main__':
    raise SystemExit(चलाउनुहोस्())
