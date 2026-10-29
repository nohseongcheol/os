#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. organizator 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Izvrši_komanda import Naredba


def Pokreni():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Naziv(예: ovjeriti.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fajl 또는 class 디렉터리(패키지 Naziv 유지)')
    argument_niz = 인수해석기.parse_args()
    podaci = argument_niz.file.read_bytes()
    if argument_niz.class_name and argument_niz.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Naziv = argument_niz.class_name + '.class' if argument_niz.class_name else argument_niz.file.name
    if len(podaci) > 16384 or not 1 <= len(Naziv.encode('utf-8')) <= 63 or '\n' in Naziv or '\r' in Naziv:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    oblast_VALUE = '.elf' if podaci[:4] == b'\x7fELF' else argument_niz.file.suffix
    if argument_niz.linux and oblast_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if oblast_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_niz.arguments) > 7 or any(len(string_podaci.encode('utf-8')) > 255 or '\n' in string_podaci or '\r' in string_podaci for string_podaci in argument_niz.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcije = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_niz.vnc: Opcije += ['-vnc', argument_niz.vnc]
    proces = subprocess.Popen(Naredba() + Opcije, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač = selectors.DefaultSelector(); birač.register(proces.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); završiti_Pomak = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > završiti_Pomak: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in birač.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if proces.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def poslati(Linija, 확인표시=b'jkoros-native> '):
        proces.stdin.write(Linija.encode('utf-8') + b'\n'); proces.stdin.flush()
        return 수신하기(확인표시)
    def Izvrši_komanda(Linija):
        출력결과 = poslati(Linija); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fajl_spisak = []
        for 포함항목 in argument_niz.include:
            if 포함항목.is_dir():
                fajl_spisak += [(str(podaci_položaj.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', podaci_položaj.read_bytes()) for podaci_položaj in sorted(포함항목.rglob('*.class'))]
            else:
                fajl_spisak.append((포함항목.name, 포함항목.read_bytes()))
        fajl_spisak = [(stavka_COUNT, odredište_podaci) for stavka_COUNT, odredište_podaci in fajl_spisak if stavka_COUNT != Naziv] + [(Naziv, podaci)]
        for Upload_naziv, Upload_podaci in fajl_spisak:
            if len(Upload_podaci) > 16384 or len(Upload_naziv.encode('utf-8')) > 63 or '\n' in Upload_naziv or '\r' in Upload_naziv:
                raise ValueError('추가 파일의 Naziv/Veličina 제한 초과: ' + Upload_naziv)
            poslati('load ' + shlex.quote(Upload_naziv), b'hex> ')
            for 순번 in range(0, len(Upload_podaci), 64): poslati(Upload_podaci[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in poslati('.'): raise RuntimeError('upload failed: ' + Upload_naziv)
            갈무리자료 = poslati('hex ' + shlex.quote(Upload_naziv))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_podaci: raise RuntimeError('upload verification failed')
        if oblast_VALUE == '.java' and Izvrši_komanda('javac ' + shlex.quote(Naziv)) != 0: return 1
        실행가능파일 = argument_niz.file.stem + '.elf'
        if oblast_VALUE == '.c' and Izvrši_komanda('cc ' + shlex.quote(Naziv) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_niz.class_name or argument_niz.file.stem) if oblast_VALUE in ('.java', '.class') else ('python ' if oblast_VALUE == '.py' else 'run ') + shlex.quote(Naziv)
        if oblast_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Naziv)
        if oblast_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_niz.linux: program = 'run --linux ' + shlex.quote(Naziv)
        if argument_niz.arguments: program += ' ' + ' '.join(shlex.quote(string_podaci) for string_podaci in argument_niz.arguments)
        return 0 if Izvrši_komanda(program) == 0 else 1
    finally:
        if proces.poll() is None:
            proces.terminate()
            try: proces.wait(timeout=5)
            except subprocess.TimeoutExpired: proces.kill(); proces.wait(timeout=5)
        birač.close(); proces.stdin.close(); proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Pokreni())
