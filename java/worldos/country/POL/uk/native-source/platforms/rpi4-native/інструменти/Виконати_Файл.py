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
from Виконати_команда import команда


def запустити():
    аналізатор = argparse.ArgumentParser(description=__doc__)
    аналізатор.add_argument('file', type=Path)
    аналізатор.add_argument('arguments', nargs='*')
    аналізатор.add_argument('--class-name', help='패키지가 있는 .class의 전체 Назва(예: затвердити.꾸러미시험)')
    аналізатор.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI використання_значення')
    аналізатор.add_argument('--vnc', help='예: 127.0.0.1:2')
    аналізатор.add_argument('--include', action='append', type=Path, default=[], help='додавати_запис class файл 또는 class 디렉터리(패키지 Назва 유지)')
    аргумент_масив = аналізатор.parse_args()
    дані = аргумент_масив.file.read_bytes()
    if аргумент_масив.class_name and аргумент_масив.file.suffix != '.class': аналізатор.error('--class-name은 .class 입력에서 사용합니다.')
    Назва = аргумент_масив.class_name + '.class' if аргумент_масив.class_name else аргумент_масив.file.name
    if len(дані) > 16384 or not 1 <= len(Назва.encode('utf-8')) <= 63 or '\n' in Назва or '\r' in Назва:
        аналізатор.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    область_значення = '.elf' if дані[:4] == b'\x7fELF' else аргумент_масив.file.suffix
    if аргумент_масив.linux and область_значення != '.elf': аналізатор.error('--linux는 ELF 바이너리에만 사용합니다.')
    if область_значення not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        аналізатор.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_масив.arguments) > 7 or any(len(рядок_дані.encode('utf-8')) > 255 or '\n' in рядок_дані or '\r' in рядок_дані for рядок_дані in аргумент_масив.arguments):
        аналізатор.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметри = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_масив.vnc: Параметри += ['-vnc', аргумент_масив.vnc]
    Процеси = subprocess.Popen(команда() + Параметри, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор = selectors.DefaultSelector(); селектор.register(Процеси.stdout, selectors.EVENT_READ)
    def отримувати_повідомлення(маркер, 시간제한=45):
        출력결과 = bytearray(); завершити_виклик_Зміщена_копія = time.monotonic() + 시간제한
        while маркер not in 출력결과:
            if time.monotonic() > завершити_виклик_Зміщена_копія: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in селектор.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процеси.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def надсилати(рядок_введення, маркер=b'jkoros-native> '):
        Процеси.stdin.write(рядок_введення.encode('utf-8') + b'\n'); Процеси.stdin.flush()
        return отримувати_повідомлення(маркер)
    def Виконати_команда(рядок_введення):
        출력결과 = надсилати(рядок_введення); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        отримувати_повідомлення(b'jkoros-native> ')
        Файл_список = []
        for містити in аргумент_масив.include:
            if містити.is_dir():
                Файл_список += [(str(дані_посада.relative_to(містити).with_suffix('')).replace('/', '.') + '.class', дані_посада.read_bytes()) for дані_посада in sorted(містити.rglob('*.class'))]
            else:
                Файл_список.append((містити.name, містити.read_bytes()))
        Файл_список = [(개수, місце_дані) for 개수, місце_дані in Файл_список if 개수 != Назва] + [(Назва, дані)]
        for передавати_ім_я, передавати_дані in Файл_список:
            if len(передавати_дані) > 16384 or len(передавати_ім_я.encode('utf-8')) > 63 or '\n' in передавати_ім_я or '\r' in передавати_ім_я:
                raise ValueError('додавати_запис 파일의 Назва/Розмір 제한 초과: ' + передавати_ім_я)
            надсилати('load ' + shlex.quote(передавати_ім_я), b'hex> ')
            for 순번 in range(0, len(передавати_дані), 64): надсилати(передавати_дані[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in надсилати('.'): raise RuntimeError('upload failed: ' + передавати_ім_я)
            갈무리자료 = надсилати('hex ' + shlex.quote(передавати_ім_я))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != передавати_дані: raise RuntimeError('upload verification failed')
        if область_значення == '.java' and Виконати_команда('javac ' + shlex.quote(Назва)) != 0: return 1
        실행가능파일 = аргумент_масив.file.stem + '.elf'
        if область_значення == '.c' and Виконати_команда('cc ' + shlex.quote(Назва) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програма = 'java ' + shlex.quote(аргумент_масив.class_name or аргумент_масив.file.stem) if область_значення in ('.java', '.class') else ('python ' if область_значення == '.py' else 'run ') + shlex.quote(Назва)
        if область_значення == '.jar': програма = 'java -jar ' + shlex.quote(Назва)
        if область_значення == '.c': програма = 'run ' + shlex.quote(실행가능파일)
        if аргумент_масив.linux: програма = 'run --linux ' + shlex.quote(Назва)
        if аргумент_масив.arguments: програма += ' ' + ' '.join(shlex.quote(рядок_дані) for рядок_дані in аргумент_масив.arguments)
        return 0 if Виконати_команда(програма) == 0 else 1
    finally:
        if Процеси.poll() is None:
            Процеси.terminate()
            try: Процеси.wait(timeout=5)
            except subprocess.TimeoutExpired: Процеси.kill(); Процеси.wait(timeout=5)
        селектор.close(); Процеси.stdin.close(); Процеси.stdout.close()


if __name__ == '__main__':
    raise SystemExit(запустити())
