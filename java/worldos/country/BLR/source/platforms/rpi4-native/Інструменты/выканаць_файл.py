#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. вузел 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from выканаць_каманда import Загад


def Выканаць():
    аналізатар = argparse.ArgumentParser(description=__doc__)
    аналізатар.add_argument('file', type=Path)
    аналізатар.add_argument('arguments', nargs='*')
    аналізатар.add_argument('--class-name', help='패키지가 있는 .class의 전체 Назва(예: праверыць_5fb2b747.꾸러미시험)')
    аналізатар.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    аналізатар.add_argument('--vnc', help='예: 127.0.0.1:2')
    аналізатар.add_argument('--include', action='append', type=Path, default=[], help='추가 class Файл 또는 class 디렉터리(패키지 Назва 유지)')
    аргумент_масіў = аналізатар.parse_args()
    дадзеныя = аргумент_масіў.file.read_bytes()
    if аргумент_масіў.class_name and аргумент_масіў.file.suffix != '.class': аналізатар.error('--class-name은 .class 입력에서 사용합니다.')
    Назва = аргумент_масіў.class_name + '.class' if аргумент_масіў.class_name else аргумент_масіў.file.name
    if len(дадзеныя) > 16384 or not 1 <= len(Назва.encode('utf-8')) <= 63 or '\n' in Назва or '\r' in Назва:
        аналізатар.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    катэгорыя_значэнне = '.elf' if дадзеныя[:4] == b'\x7fELF' else аргумент_масіў.file.suffix
    if аргумент_масіў.linux and катэгорыя_значэнне != '.elf': аналізатар.error('--linux는 ELF 바이너리에만 사용합니다.')
    if катэгорыя_значэнне not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        аналізатар.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_масіў.arguments) > 7 or any(len(радок_дадзеныя.encode('utf-8')) > 255 or '\n' in радок_дадзеныя or '\r' in радок_дадзеныя for радок_дадзеныя in аргумент_масіў.arguments):
        аналізатар.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметры = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_масіў.vnc: Параметры += ['-vnc', аргумент_масіў.vnc]
    Працэс = subprocess.Popen(Загад() + Параметры, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектар = selectors.DefaultSelector(); селектар.register(Працэс.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); скончыць_Зрух = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > скончыць_Зрух: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in селектар.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Працэс.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def адправіць(лінія, 확인표시=b'jkoros-native> '):
        Працэс.stdin.write(лінія.encode('utf-8') + b'\n'); Працэс.stdin.flush()
        return 수신하기(확인표시)
    def выканаць_каманда(лінія):
        출력결과 = адправіць(лінія); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Спіс = []
        for 포함항목 in аргумент_масіў.include:
            if 포함항목.is_dir():
                файл_Спіс += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Спіс.append((포함항목.name, 포함항목.read_bytes()))
        файл_Спіс = [(개수, прызначэнне_дадзеныя) for 개수, прызначэнне_дадзеныя in файл_Спіс if 개수 != Назва] + [(Назва, дадзеныя)]
        for запампоўка_імя, запампоўка_дадзеныя in файл_Спіс:
            if len(запампоўка_дадзеныя) > 16384 or len(запампоўка_імя.encode('utf-8')) > 63 or '\n' in запампоўка_імя or '\r' in запампоўка_імя:
                raise ValueError('추가 파일의 Назва/Памер 제한 초과: ' + запампоўка_імя)
            адправіць('load ' + shlex.quote(запампоўка_імя), b'hex> ')
            for 순번 in range(0, len(запампоўка_дадзеныя), 64): адправіць(запампоўка_дадзеныя[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in адправіць('.'): raise RuntimeError('upload failed: ' + запампоўка_імя)
            갈무리자료 = адправіць('hex ' + shlex.quote(запампоўка_імя))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != запампоўка_дадзеныя: raise RuntimeError('upload verification failed')
        if катэгорыя_значэнне == '.java' and выканаць_каманда('javac ' + shlex.quote(Назва)) != 0: return 1
        실행가능파일 = аргумент_масіў.file.stem + '.elf'
        if катэгорыя_значэнне == '.c' and выканаць_каманда('cc ' + shlex.quote(Назва) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        праграма = 'java ' + shlex.quote(аргумент_масіў.class_name or аргумент_масіў.file.stem) if катэгорыя_значэнне in ('.java', '.class') else ('python ' if катэгорыя_значэнне == '.py' else 'run ') + shlex.quote(Назва)
        if катэгорыя_значэнне == '.jar': праграма = 'java -jar ' + shlex.quote(Назва)
        if катэгорыя_значэнне == '.c': праграма = 'run ' + shlex.quote(실행가능파일)
        if аргумент_масіў.linux: праграма = 'run --linux ' + shlex.quote(Назва)
        if аргумент_масіў.arguments: праграма += ' ' + ' '.join(shlex.quote(радок_дадзеныя) for радок_дадзеныя in аргумент_масіў.arguments)
        return 0 if выканаць_каманда(праграма) == 0 else 1
    finally:
        if Працэс.poll() is None:
            Працэс.terminate()
            try: Працэс.wait(timeout=5)
            except subprocess.TimeoutExpired: Працэс.kill(); Працэс.wait(timeout=5)
        селектар.close(); Працэс.stdin.close(); Працэс.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Выканаць())
