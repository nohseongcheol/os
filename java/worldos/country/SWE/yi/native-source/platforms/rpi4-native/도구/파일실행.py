#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. 호스트 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import 명령


def 시작():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 נאָמען(예: 검증.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class טעקע 또는 class 디렉터리(패키지 נאָמען 유지)')
    인수배열 = 인수해석기.parse_args()
    자료 = 인수배열.file.read_bytes()
    if 인수배열.class_name and 인수배열.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    נאָמען = 인수배열.class_name + '.class' if 인수배열.class_name else 인수배열.file.name
    if len(자료) > 16384 or not 1 <= len(נאָמען.encode('utf-8')) <= 63 or '\n' in נאָמען or '\r' in נאָמען:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    분류 = '.elf' if 자료[:4] == b'\x7fELF' else 인수배열.file.suffix
    if 인수배열.linux and 분류 != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if 분류 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(인수배열.arguments) > 7 or any(len(문자열값.encode('utf-8')) > 255 or '\n' in 문자열값 or '\r' in 문자열값 for 문자열값 in 인수배열.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    선택사항 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if 인수배열.vnc: 선택사항 += ['-vnc', 인수배열.vnc]
    실행과정 = subprocess.Popen(명령() + 선택사항, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(실행과정.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if 실행과정.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def 보내기(줄, 확인표시=b'jkoros-native> '):
        실행과정.stdin.write(줄.encode('utf-8') + b'\n'); 실행과정.stdin.flush()
        return 수신하기(확인표시)
    def 실행(줄):
        출력결과 = 보내기(줄); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        파일목록 = []
        for 포함항목 in 인수배열.include:
            if 포함항목.is_dir():
                파일목록 += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                파일목록.append((포함항목.name, 포함항목.read_bytes()))
        파일목록 = [(개수, 목적자료) for 개수, 목적자료 in 파일목록 if 개수 != נאָמען] + [(נאָמען, 자료)]
        for 올릴이름, 올릴자료 in 파일목록:
            if len(올릴자료) > 16384 or len(올릴이름.encode('utf-8')) > 63 or '\n' in 올릴이름 or '\r' in 올릴이름:
                raise ValueError('추가 파일의 נאָמען/גרײס 제한 초과: ' + 올릴이름)
            보내기('load ' + shlex.quote(올릴이름), b'hex> ')
            for 순번 in range(0, len(올릴자료), 64): 보내기(올릴자료[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in 보내기('.'): raise RuntimeError('upload failed: ' + 올릴이름)
            갈무리자료 = 보내기('hex ' + shlex.quote(올릴이름))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != 올릴자료: raise RuntimeError('upload verification failed')
        if 분류 == '.java' and 실행('javac ' + shlex.quote(נאָמען)) != 0: return 1
        실행가능파일 = 인수배열.file.stem + '.elf'
        if 분류 == '.c' and 실행('cc ' + shlex.quote(נאָמען) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        실행항목 = 'java ' + shlex.quote(인수배열.class_name or 인수배열.file.stem) if 분류 in ('.java', '.class') else ('python ' if 분류 == '.py' else 'run ') + shlex.quote(נאָמען)
        if 분류 == '.jar': 실행항목 = 'java -jar ' + shlex.quote(נאָמען)
        if 분류 == '.c': 실행항목 = 'run ' + shlex.quote(실행가능파일)
        if 인수배열.linux: 실행항목 = 'run --linux ' + shlex.quote(נאָמען)
        if 인수배열.arguments: 실행항목 += ' ' + ' '.join(shlex.quote(문자열값) for 문자열값 in 인수배열.arguments)
        return 0 if 실행(실행항목) == 0 else 1
    finally:
        if 실행과정.poll() is None:
            실행과정.terminate()
            try: 실행과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait(timeout=5)
        준비선택기.close(); 실행과정.stdin.close(); 실행과정.stdout.close()


if __name__ == '__main__':
    raise SystemExit(시작())
