#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. хост 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from үтәргә_команда import команда


def эшләтү():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 исем(예: тикшерү.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Birem 또는 class 디렉터리(패키지 исем 유지)')
    аргумент_МАССИВ = 인수해석기.parse_args()
    мәгълүмат = аргумент_МАССИВ.file.read_bytes()
    if аргумент_МАССИВ.class_name and аргумент_МАССИВ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    исем = аргумент_МАССИВ.class_name + '.class' if аргумент_МАССИВ.class_name else аргумент_МАССИВ.file.name
    if len(мәгълүмат) > 16384 or not 1 <= len(исем.encode('utf-8')) <= 63 or '\n' in исем or '\r' in исем:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    категория_VALUE = '.elf' if мәгълүмат[:4] == b'\x7fELF' else аргумент_МАССИВ.file.suffix
    if аргумент_МАССИВ.linux and категория_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if категория_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_МАССИВ.arguments) > 7 or any(len(юл_мәгълүмат.encode('utf-8')) > 255 or '\n' in юл_мәгълүмат or '\r' in юл_мәгълүмат for юл_мәгълүмат in аргумент_МАССИВ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметрлар = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_МАССИВ.vnc: Параметрлар += ['-vnc', аргумент_МАССИВ.vnc]
    Процесс = subprocess.Popen(команда() + Параметрлар, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сайлагыч = selectors.DefaultSelector(); сайлагыч.register(Процесс.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); тәмамлау_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > тәмамлау_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in сайлагыч.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процесс.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def җибәрү(юл, 확인표시=b'jkoros-native> '):
        Процесс.stdin.write(юл.encode('utf-8') + b'\n'); Процесс.stdin.flush()
        return 수신하기(확인표시)
    def үтәргә_команда(юл):
        출력결과 = җибәрү(юл); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Исемлек = []
        for 포함항목 in аргумент_МАССИВ.include:
            if 포함항목.is_dir():
                файл_Исемлек += [(str(мәгълүмат_урнаштыру.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', мәгълүмат_урнаштыру.read_bytes()) for мәгълүмат_урнаштыру in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Исемлек.append((포함항목.name, 포함항목.read_bytes()))
        файл_Исемлек = [(элемент_COUNT, күчерү_урыны_мәгълүмат) for элемент_COUNT, күчерү_урыны_мәгълүмат in файл_Исемлек if элемент_COUNT != исем] + [(исем, мәгълүмат)]
        for йөкләп_җибәрү_исем, йөкләп_җибәрү_мәгълүмат in файл_Исемлек:
            if len(йөкләп_җибәрү_мәгълүмат) > 16384 or len(йөкләп_җибәрү_исем.encode('utf-8')) > 63 or '\n' in йөкләп_җибәрү_исем or '\r' in йөкләп_җибәрү_исем:
                raise ValueError('추가 파일의 исем/үлчәмен_үзгәртү 제한 초과: ' + йөкләп_җибәрү_исем)
            җибәрү('load ' + shlex.quote(йөкләп_җибәрү_исем), b'hex> ')
            for 순번 in range(0, len(йөкләп_җибәрү_мәгълүмат), 64): җибәрү(йөкләп_җибәрү_мәгълүмат[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in җибәрү('.'): raise RuntimeError('upload failed: ' + йөкләп_җибәрү_исем)
            갈무리자료 = җибәрү('hex ' + shlex.quote(йөкләп_җибәрү_исем))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != йөкләп_җибәрү_мәгълүмат: raise RuntimeError('upload verification failed')
        if категория_VALUE == '.java' and үтәргә_команда('javac ' + shlex.quote(исем)) != 0: return 1
        실행가능파일 = аргумент_МАССИВ.file.stem + '.elf'
        if категория_VALUE == '.c' and үтәргә_команда('cc ' + shlex.quote(исем) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        кушымта = 'java ' + shlex.quote(аргумент_МАССИВ.class_name or аргумент_МАССИВ.file.stem) if категория_VALUE in ('.java', '.class') else ('python ' if категория_VALUE == '.py' else 'run ') + shlex.quote(исем)
        if категория_VALUE == '.jar': кушымта = 'java -jar ' + shlex.quote(исем)
        if категория_VALUE == '.c': кушымта = 'run ' + shlex.quote(실행가능파일)
        if аргумент_МАССИВ.linux: кушымта = 'run --linux ' + shlex.quote(исем)
        if аргумент_МАССИВ.arguments: кушымта += ' ' + ' '.join(shlex.quote(юл_мәгълүмат) for юл_мәгълүмат in аргумент_МАССИВ.arguments)
        return 0 if үтәргә_команда(кушымта) == 0 else 1
    finally:
        if Процесс.poll() is None:
            Процесс.terminate()
            try: Процесс.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait(timeout=5)
        сайлагыч.close(); Процесс.stdin.close(); Процесс.stdout.close()


if __name__ == '__main__':
    raise SystemExit(эшләтү())
