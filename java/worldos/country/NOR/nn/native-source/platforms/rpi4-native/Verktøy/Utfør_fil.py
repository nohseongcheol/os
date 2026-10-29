#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. vert 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Utfør_kommando import Kommando


def Køyr_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Namn(예: bekrefte.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fil 또는 class 디렉터리(패키지 Namn 유지)')
    argument_ARRAY = 인수해석기.parse_args()
    data = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Namn = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(Namn.encode('utf-8')) <= 63 or '\n' in Namn or '\r' in Namn:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategori_VALUE = '.elf' if data[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and kategori_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategori_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(streng_data.encode('utf-8')) > 255 or '\n' in streng_data or '\r' in streng_data for streng_data in argument_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Alternativ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Alternativ += ['-vnc', argument_ARRAY.vnc]
    Prosess = subprocess.Popen(Kommando() + Alternativ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    veljar = selectors.DefaultSelector(); veljar.register(Prosess.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); avslutte_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > avslutte_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in veljar.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Prosess.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def sende(linje, 확인표시=b'jkoros-native> '):
        Prosess.stdin.write(linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
        return 수신하기(확인표시)
    def Utfør_kommando(linje):
        출력결과 = sende(linje); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fil_Liste = []
        for 포함항목 in argument_ARRAY.include:
            if 포함항목.is_dir():
                fil_Liste += [(str(data_plassere.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_plassere.read_bytes()) for data_plassere in sorted(포함항목.rglob('*.class'))]
            else:
                fil_Liste.append((포함항목.name, 포함항목.read_bytes()))
        fil_Liste = [(vare_COUNT, mål_data) for vare_COUNT, mål_data in fil_Liste if vare_COUNT != Namn] + [(Namn, data)]
        for Upload_namn, Upload_data in fil_Liste:
            if len(Upload_data) > 16384 or len(Upload_namn.encode('utf-8')) > 63 or '\n' in Upload_namn or '\r' in Upload_namn:
                raise ValueError('추가 파일의 Namn/Storleik 제한 초과: ' + Upload_namn)
            sende('load ' + shlex.quote(Upload_namn), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): sende(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in sende('.'): raise RuntimeError('upload failed: ' + Upload_namn)
            갈무리자료 = sende('hex ' + shlex.quote(Upload_namn))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if kategori_VALUE == '.java' and Utfør_kommando('javac ' + shlex.quote(Namn)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if kategori_VALUE == '.c' and Utfør_kommando('cc ' + shlex.quote(Namn) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        app = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if kategori_VALUE in ('.java', '.class') else ('python ' if kategori_VALUE == '.py' else 'run ') + shlex.quote(Namn)
        if kategori_VALUE == '.jar': app = 'java -jar ' + shlex.quote(Namn)
        if kategori_VALUE == '.c': app = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: app = 'run --linux ' + shlex.quote(Namn)
        if argument_ARRAY.arguments: app += ' ' + ' '.join(shlex.quote(streng_data) for streng_data in argument_ARRAY.arguments)
        return 0 if Utfør_kommando(app) == 0 else 1
    finally:
        if Prosess.poll() is None:
            Prosess.terminate()
            try: Prosess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait(timeout=5)
        veljar.close(); Prosess.stdin.close(); Prosess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Køyr_2())
