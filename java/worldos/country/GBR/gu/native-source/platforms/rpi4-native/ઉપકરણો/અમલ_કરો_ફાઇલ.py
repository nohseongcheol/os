#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. હોસ્ટ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from અમલ_કરો_આદેશ import આદેશ


def ચલાવો_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 નામ(예: માન્ય_કરો.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ફાઈલ 또는 class 디렉터리(패키지 નામ 유지)')
    દલીલ_અરે = 인수해석기.parse_args()
    ડેટા = દલીલ_અરે.file.read_bytes()
    if દલીલ_અરે.class_name and દલીલ_અરે.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    નામ = દલીલ_અરે.class_name + '.class' if દલીલ_અરે.class_name else દલીલ_અરે.file.name
    if len(ડેટા) > 16384 or not 1 <= len(નામ.encode('utf-8')) <= 63 or '\n' in નામ or '\r' in નામ:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    શ્રેણી_મૂલ્ય = '.elf' if ડેટા[:4] == b'\x7fELF' else દલીલ_અરે.file.suffix
    if દલીલ_અરે.linux and શ્રેણી_મૂલ્ય != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if શ્રેણી_મૂલ્ય not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(દલીલ_અરે.arguments) > 7 or any(len(સ્ટ્રિંગ_ડેટા.encode('utf-8')) > 255 or '\n' in સ્ટ્રિંગ_ડેટા or '\r' in સ્ટ્રિંગ_ડેટા for સ્ટ્રિંગ_ડેટા in દલીલ_અરે.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    વિકલ્પો = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if દલીલ_અરે.vnc: વિકલ્પો += ['-vnc', દલીલ_અરે.vnc]
    પ્રક્રિયા = subprocess.Popen(આદેશ() + વિકલ્પો, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    પસંદકર્તા = selectors.DefaultSelector(); પસંદકર્તા.register(પ્રક્રિયા.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); અંત_કરો_ઑફસેટ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > અંત_કરો_ઑફસેટ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in પસંદકર્તા.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if પ્રક્રિયા.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def મોકલો(લાઇન, 확인표시=b'jkoros-native> '):
        પ્રક્રિયા.stdin.write(લાઇન.encode('utf-8') + b'\n'); પ્રક્રિયા.stdin.flush()
        return 수신하기(확인표시)
    def અમલ_કરો_આદેશ(લાઇન):
        출력결과 = મોકલો(લાઇન); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ફાઇલ_સૂચી = []
        for 포함항목 in દલીલ_અરે.include:
            if 포함항목.is_dir():
                ફાઇલ_સૂચી += [(str(ડેટા_સ્થિતિ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ડેટા_સ્થિતિ.read_bytes()) for ડેટા_સ્થિતિ in sorted(포함항목.rglob('*.class'))]
            else:
                ફાઇલ_સૂચી.append((포함항목.name, 포함항목.read_bytes()))
        ફાઇલ_સૂચી = [(개수, ગંતવ્ય_ડેટા) for 개수, ગંતવ્ય_ડેટા in ફાઇલ_સૂચી if 개수 != નામ] + [(નામ, ડેટા)]
        for અપલોડ_કરો_નામ, અપલોડ_કરો_ડેટા in ફાઇલ_સૂચી:
            if len(અપલોડ_કરો_ડેટા) > 16384 or len(અપલોડ_કરો_નામ.encode('utf-8')) > 63 or '\n' in અપલોડ_કરો_નામ or '\r' in અપલોડ_કરો_નામ:
                raise ValueError('추가 파일의 નામ/માપ 제한 초과: ' + અપલોડ_કરો_નામ)
            મોકલો('load ' + shlex.quote(અપલોડ_કરો_નામ), b'hex> ')
            for 순번 in range(0, len(અપલોડ_કરો_ડેટા), 64): મોકલો(અપલોડ_કરો_ડેટા[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in મોકલો('.'): raise RuntimeError('upload failed: ' + અપલોડ_કરો_નામ)
            갈무리자료 = મોકલો('hex ' + shlex.quote(અપલોડ_કરો_નામ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != અપલોડ_કરો_ડેટા: raise RuntimeError('upload verification failed')
        if શ્રેણી_મૂલ્ય == '.java' and અમલ_કરો_આદેશ('javac ' + shlex.quote(નામ)) != 0: return 1
        실행가능파일 = દલીલ_અરે.file.stem + '.elf'
        if શ્રેણી_મૂલ્ય == '.c' and અમલ_કરો_આદેશ('cc ' + shlex.quote(નામ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        એપ્લિકેશન = 'java ' + shlex.quote(દલીલ_અરે.class_name or દલીલ_અરે.file.stem) if શ્રેણી_મૂલ્ય in ('.java', '.class') else ('python ' if શ્રેણી_મૂલ્ય == '.py' else 'run ') + shlex.quote(નામ)
        if શ્રેણી_મૂલ્ય == '.jar': એપ્લિકેશન = 'java -jar ' + shlex.quote(નામ)
        if શ્રેણી_મૂલ્ય == '.c': એપ્લિકેશન = 'run ' + shlex.quote(실행가능파일)
        if દલીલ_અરે.linux: એપ્લિકેશન = 'run --linux ' + shlex.quote(નામ)
        if દલીલ_અરે.arguments: એપ્લિકેશન += ' ' + ' '.join(shlex.quote(સ્ટ્રિંગ_ડેટા) for સ્ટ્રિંગ_ડેટા in દલીલ_અરે.arguments)
        return 0 if અમલ_કરો_આદેશ(એપ્લિકેશન) == 0 else 1
    finally:
        if પ્રક્રિયા.poll() is None:
            પ્રક્રિયા.terminate()
            try: પ્રક્રિયા.wait(timeout=5)
            except subprocess.TimeoutExpired: પ્રક્રિયા.kill(); પ્રક્રિયા.wait(timeout=5)
        પસંદકર્તા.close(); પ્રક્રિયા.stdin.close(); પ્રક્રિયા.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ચલાવો_2())
