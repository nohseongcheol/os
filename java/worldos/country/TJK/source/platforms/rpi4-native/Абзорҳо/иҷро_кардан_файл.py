#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. мизбон 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from иҷро_кардан_фармон import фармон


def порча():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ном(예: санҷидани_эътибор.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Файл 또는 class 디렉터리(패키지 Ном 유지)')
    аргумент_қатор = 인수해석기.parse_args()
    иттилоот = аргумент_қатор.file.read_bytes()
    if аргумент_қатор.class_name and аргумент_қатор.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Ном = аргумент_қатор.class_name + '.class' if аргумент_қатор.class_name else аргумент_қатор.file.name
    if len(иттилоот) > 16384 or not 1 <= len(Ном.encode('utf-8')) <= 63 or '\n' in Ном or '\r' in Ном:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    категория_қимат = '.elf' if иттилоот[:4] == b'\x7fELF' else аргумент_қатор.file.suffix
    if аргумент_қатор.linux and категория_қимат != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if категория_қимат not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_қатор.arguments) > 7 or any(len(сатр_иттилоот.encode('utf-8')) > 255 or '\n' in сатр_иттилоот or '\r' in сатр_иттилоот for сатр_иттилоот in аргумент_қатор.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Имконот = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_қатор.vnc: Имконот += ['-vnc', аргумент_қатор.vnc]
    Раванд = subprocess.Popen(фармон() + Имконот, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    интихобкунанда = selectors.DefaultSelector(); интихобкунанда.register(Раванд.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); анҷом_додан_Интиқолшавӣ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > анҷом_додан_Интиқолшавӣ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in интихобкунанда.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Раванд.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def фиристодан(хат, 확인표시=b'jkoros-native> '):
        Раванд.stdin.write(хат.encode('utf-8') + b'\n'); Раванд.stdin.flush()
        return 수신하기(확인표시)
    def иҷро_кардан_фармон(хат):
        출력결과 = фиристодан(хат); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Рӯйхат = []
        for 포함항목 in аргумент_қатор.include:
            if 포함항목.is_dir():
                файл_Рӯйхат += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Рӯйхат.append((포함항목.name, 포함항목.read_bytes()))
        файл_Рӯйхат = [(개수, ҷои_таъинот_иттилоот) for 개수, ҷои_таъинот_иттилоот in файл_Рӯйхат if 개수 != Ном] + [(Ном, иттилоот)]
        for бор_кардан_ном, бор_кардан_иттилоот in файл_Рӯйхат:
            if len(бор_кардан_иттилоот) > 16384 or len(бор_кардан_ном.encode('utf-8')) > 63 or '\n' in бор_кардан_ном or '\r' in бор_кардан_ном:
                raise ValueError('추가 파일의 Ном/андоза_кардан 제한 초과: ' + бор_кардан_ном)
            фиристодан('load ' + shlex.quote(бор_кардан_ном), b'hex> ')
            for 순번 in range(0, len(бор_кардан_иттилоот), 64): фиристодан(бор_кардан_иттилоот[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in фиристодан('.'): raise RuntimeError('upload failed: ' + бор_кардан_ном)
            갈무리자료 = фиристодан('hex ' + shlex.quote(бор_кардан_ном))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != бор_кардан_иттилоот: raise RuntimeError('upload verification failed')
        if категория_қимат == '.java' and иҷро_кардан_фармон('javac ' + shlex.quote(Ном)) != 0: return 1
        실행가능파일 = аргумент_қатор.file.stem + '.elf'
        if категория_қимат == '.c' and иҷро_кардан_фармон('cc ' + shlex.quote(Ном) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        барнома = 'java ' + shlex.quote(аргумент_қатор.class_name or аргумент_қатор.file.stem) if категория_қимат in ('.java', '.class') else ('python ' if категория_қимат == '.py' else 'run ') + shlex.quote(Ном)
        if категория_қимат == '.jar': барнома = 'java -jar ' + shlex.quote(Ном)
        if категория_қимат == '.c': барнома = 'run ' + shlex.quote(실행가능파일)
        if аргумент_қатор.linux: барнома = 'run --linux ' + shlex.quote(Ном)
        if аргумент_қатор.arguments: барнома += ' ' + ' '.join(shlex.quote(сатр_иттилоот) for сатр_иттилоот in аргумент_қатор.arguments)
        return 0 if иҷро_кардан_фармон(барнома) == 0 else 1
    finally:
        if Раванд.poll() is None:
            Раванд.terminate()
            try: Раванд.wait(timeout=5)
            except subprocess.TimeoutExpired: Раванд.kill(); Раванд.wait(timeout=5)
        интихобкунанда.close(); Раванд.stdin.close(); Раванд.stdout.close()


if __name__ == '__main__':
    raise SystemExit(порча())
