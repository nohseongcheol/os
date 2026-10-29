#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. epiajatü 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import aluwataaya


def 시작():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 이름(예: 검증.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class anaajaalaa 또는 class 디렉터리(패키지 이름 유지)')
    ajutuu_matüriisü = 인수해석기.parse_args()
    atijaaya = ajutuu_matüriisü.file.read_bytes()
    if ajutuu_matüriisü.class_name and ajutuu_matüriisü.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    이름 = ajutuu_matüriisü.class_name + '.class' if ajutuu_matüriisü.class_name else ajutuu_matüriisü.file.name
    if len(atijaaya) > 16384 or not 1 <= len(이름.encode('utf-8')) <= 63 or '\n' in 이름 or '\r' in 이름:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    akotchiraayanüliee_ajutuu = '.elf' if atijaaya[:4] == b'\x7fELF' else ajutuu_matüriisü.file.suffix
    if ajutuu_matüriisü.linux and akotchiraayanüliee_ajutuu != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if akotchiraayanüliee_ajutuu not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ajutuu_matüriisü.arguments) > 7 or any(len(kaleena_atijaaya.encode('utf-8')) > 255 or '\n' in kaleena_atijaaya or '\r' in kaleena_atijaaya for kaleena_atijaaya in ajutuu_matüriisü.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Aneekuui = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ajutuu_matüriisü.vnc: Aneekuui += ['-vnc', ajutuu_matüriisü.vnc]
    실행과정 = subprocess.Popen(aluwataaya() + Aneekuui, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
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
    def ajütaa(liinia, 확인표시=b'jkoros-native> '):
        실행과정.stdin.write(liinia.encode('utf-8') + b'\n'); 실행과정.stdin.flush()
        return 수신하기(확인표시)
    def 실행(liinia):
        출력결과 = ajütaa(liinia); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        파일목록 = []
        for 포함항목 in ajutuu_matüriisü.include:
            if 포함항목.is_dir():
                파일목록 += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                파일목록.append((포함항목.name, 포함항목.read_bytes()))
        파일목록 = [(개수, jalamüinjatü_atijaaya) for 개수, jalamüinjatü_atijaaya in 파일목록 if 개수 != 이름] + [(이름, atijaaya)]
        for 올릴이름, o_ote_eraa_atijaaya in 파일목록:
            if len(o_ote_eraa_atijaaya) > 16384 or len(올릴이름.encode('utf-8')) > 63 or '\n' in 올릴이름 or '\r' in 올릴이름:
                raise ValueError('추가 파일의 이름/크기 제한 초과: ' + 올릴이름)
            ajütaa('load ' + shlex.quote(올릴이름), b'hex> ')
            for 순번 in range(0, len(o_ote_eraa_atijaaya), 64): ajütaa(o_ote_eraa_atijaaya[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ajütaa('.'): raise RuntimeError('upload failed: ' + 올릴이름)
            갈무리자료 = ajütaa('hex ' + shlex.quote(올릴이름))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != o_ote_eraa_atijaaya: raise RuntimeError('upload verification failed')
        if akotchiraayanüliee_ajutuu == '.java' and 실행('javac ' + shlex.quote(이름)) != 0: return 1
        실행가능파일 = ajutuu_matüriisü.file.stem + '.elf'
        if akotchiraayanüliee_ajutuu == '.c' and 실행('cc ' + shlex.quote(이름) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        akumajiaa = 'java ' + shlex.quote(ajutuu_matüriisü.class_name or ajutuu_matüriisü.file.stem) if akotchiraayanüliee_ajutuu in ('.java', '.class') else ('python ' if akotchiraayanüliee_ajutuu == '.py' else 'run ') + shlex.quote(이름)
        if akotchiraayanüliee_ajutuu == '.jar': akumajiaa = 'java -jar ' + shlex.quote(이름)
        if akotchiraayanüliee_ajutuu == '.c': akumajiaa = 'run ' + shlex.quote(실행가능파일)
        if ajutuu_matüriisü.linux: akumajiaa = 'run --linux ' + shlex.quote(이름)
        if ajutuu_matüriisü.arguments: akumajiaa += ' ' + ' '.join(shlex.quote(kaleena_atijaaya) for kaleena_atijaaya in ajutuu_matüriisü.arguments)
        return 0 if 실행(akumajiaa) == 0 else 1
    finally:
        if 실행과정.poll() is None:
            실행과정.terminate()
            try: 실행과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait(timeout=5)
        준비선택기.close(); 실행과정.stdin.close(); 실행과정.stdout.close()


if __name__ == '__main__':
    raise SystemExit(시작())
