#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. येजमान 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from पाळो_दिवचो_आदेश import आदेश


def चलोवप():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 नांव(예: पुनर्तपासणी_करची_5fb2b747.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class फायल 또는 class 디렉터리(패키지 नांव 유지)')
    युक्तीवाद_क्रम = 인수해석기.parse_args()
    डेटा = युक्तीवाद_क्रम.file.read_bytes()
    if युक्तीवाद_क्रम.class_name and युक्तीवाद_क्रम.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    नांव = युक्तीवाद_क्रम.class_name + '.class' if युक्तीवाद_क्रम.class_name else युक्तीवाद_क्रम.file.name
    if len(डेटा) > 16384 or not 1 <= len(नांव.encode('utf-8')) <= 63 or '\n' in नांव or '\r' in नांव:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    वर्ग_मोल = '.elf' if डेटा[:4] == b'\x7fELF' else युक्तीवाद_क्रम.file.suffix
    if युक्तीवाद_क्रम.linux and वर्ग_मोल != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if वर्ग_मोल not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(युक्तीवाद_क्रम.arguments) > 7 or any(len(स्ट्रिंग_डेटा.encode('utf-8')) > 255 or '\n' in स्ट्रिंग_डेटा or '\r' in स्ट्रिंग_डेटा for स्ट्रिंग_डेटा in युक्तीवाद_क्रम.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    पर्याय = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if युक्तीवाद_क्रम.vnc: पर्याय += ['-vnc', युक्तीवाद_क्रम.vnc]
    प्रक्रिया = subprocess.Popen(आदेश() + पर्याय, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    वेंचक = selectors.DefaultSelector(); वेंचक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); सोपोवचें_ऑफसॅट = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > सोपोवचें_ऑफसॅट: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in वेंचक.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if प्रक्रिया.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def धाडचें(रेग, 확인표시=b'jkoros-native> '):
        प्रक्रिया.stdin.write(रेग.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
        return 수신하기(확인표시)
    def पाळो_दिवचो_आदेश(रेग):
        출력결과 = धाडचें(रेग); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        फायल_सुची = []
        for 포함항목 in युक्तीवाद_क्रम.include:
            if 포함항목.is_dir():
                फायल_सुची += [(str(डेटा_स्थिती.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', डेटा_स्थिती.read_bytes()) for डेटा_स्थिती in sorted(포함항목.rglob('*.class'))]
            else:
                फायल_सुची.append((포함항목.name, 포함항목.read_bytes()))
        फायल_सुची = [(आयटम_COUNT, नियुक्त_स्थान_डेटा) for आयटम_COUNT, नियुक्त_स्थान_डेटा in फायल_सुची if आयटम_COUNT != नांव] + [(नांव, डेटा)]
        for अपलोड_करचें_नांव, अपलोड_करचें_डेटा in फायल_सुची:
            if len(अपलोड_करचें_डेटा) > 16384 or len(अपलोड_करचें_नांव.encode('utf-8')) > 63 or '\n' in अपलोड_करचें_नांव or '\r' in अपलोड_करचें_नांव:
                raise ValueError('추가 파일의 नांव/आवाठ 제한 초과: ' + अपलोड_करचें_नांव)
            धाडचें('load ' + shlex.quote(अपलोड_करचें_नांव), b'hex> ')
            for 순번 in range(0, len(अपलोड_करचें_डेटा), 64): धाडचें(अपलोड_करचें_डेटा[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in धाडचें('.'): raise RuntimeError('upload failed: ' + अपलोड_करचें_नांव)
            갈무리자료 = धाडचें('hex ' + shlex.quote(अपलोड_करचें_नांव))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != अपलोड_करचें_डेटा: raise RuntimeError('upload verification failed')
        if वर्ग_मोल == '.java' and पाळो_दिवचो_आदेश('javac ' + shlex.quote(नांव)) != 0: return 1
        실행가능파일 = युक्तीवाद_क्रम.file.stem + '.elf'
        if वर्ग_मोल == '.c' and पाळो_दिवचो_आदेश('cc ' + shlex.quote(नांव) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        एप्लिकेशन = 'java ' + shlex.quote(युक्तीवाद_क्रम.class_name or युक्तीवाद_क्रम.file.stem) if वर्ग_मोल in ('.java', '.class') else ('python ' if वर्ग_मोल == '.py' else 'run ') + shlex.quote(नांव)
        if वर्ग_मोल == '.jar': एप्लिकेशन = 'java -jar ' + shlex.quote(नांव)
        if वर्ग_मोल == '.c': एप्लिकेशन = 'run ' + shlex.quote(실행가능파일)
        if युक्तीवाद_क्रम.linux: एप्लिकेशन = 'run --linux ' + shlex.quote(नांव)
        if युक्तीवाद_क्रम.arguments: एप्लिकेशन += ' ' + ' '.join(shlex.quote(स्ट्रिंग_डेटा) for स्ट्रिंग_डेटा in युक्तीवाद_क्रम.arguments)
        return 0 if पाळो_दिवचो_आदेश(एप्लिकेशन) == 0 else 1
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
        वेंचक.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()


if __name__ == '__main__':
    raise SystemExit(चलोवप())
