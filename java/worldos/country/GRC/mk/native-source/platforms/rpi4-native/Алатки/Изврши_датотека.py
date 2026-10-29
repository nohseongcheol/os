#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. вдоми 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Изврши_наредба import Команда


def Изврши_2():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('file', type=Path)
    анализатор.add_argument('arguments', nargs='*')
    анализатор.add_argument('--class-name', help='패키지가 있는 .class의 전체 Име(예: потврди.꾸러미시험)')
    анализатор.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2')
    анализатор.add_argument('--include', action='append', type=Path, default=[], help='추가 class Датотека 또는 class 디렉터리(패키지 Име 유지)')
    аргумент_низа = анализатор.parse_args()
    податоци = аргумент_низа.file.read_bytes()
    if аргумент_низа.class_name and аргумент_низа.file.suffix != '.class': анализатор.error('--class-name은 .class 입력에서 사용합니다.')
    Име = аргумент_низа.class_name + '.class' if аргумент_низа.class_name else аргумент_низа.file.name
    if len(податоци) > 16384 or not 1 <= len(Име.encode('utf-8')) <= 63 or '\n' in Име or '\r' in Име:
        анализатор.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    област_VALUE = '.elf' if податоци[:4] == b'\x7fELF' else аргумент_низа.file.suffix
    if аргумент_низа.linux and област_VALUE != '.elf': анализатор.error('--linux는 ELF 바이너리에만 사용합니다.')
    if област_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        анализатор.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_низа.arguments) > 7 or any(len(низа_податоци.encode('utf-8')) > 255 or '\n' in низа_податоци or '\r' in низа_податоци for низа_податоци in аргумент_низа.arguments):
        анализатор.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Опции = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_низа.vnc: Опции += ['-vnc', аргумент_низа.vnc]
    Процес = subprocess.Popen(Команда() + Опции, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    избирач = selectors.DefaultSelector(); избирач.register(Процес.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); крај_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > крај_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in избирач.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процес.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def испрати(ред, 확인표시=b'jkoros-native> '):
        Процес.stdin.write(ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
        return 수신하기(확인표시)
    def Изврши_наредба(ред):
        출력결과 = испрати(ред); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        датотека_Список = []
        for 포함항목 in аргумент_низа.include:
            if 포함항목.is_dir():
                датотека_Список += [(str(податоци_позиционирање.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', податоци_позиционирање.read_bytes()) for податоци_позиционирање in sorted(포함항목.rglob('*.class'))]
            else:
                датотека_Список.append((포함항목.name, 포함항목.read_bytes()))
        датотека_Список = [(ставка_COUNT, одредиште_податоци) for ставка_COUNT, одредиште_податоци in датотека_Список if ставка_COUNT != Име] + [(Име, податоци)]
        for постави_име, постави_податоци in датотека_Список:
            if len(постави_податоци) > 16384 or len(постави_име.encode('utf-8')) > 63 or '\n' in постави_име or '\r' in постави_име:
                raise ValueError('추가 파일의 Име/Големина 제한 초과: ' + постави_име)
            испрати('load ' + shlex.quote(постави_име), b'hex> ')
            for 순번 in range(0, len(постави_податоци), 64): испрати(постави_податоци[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in испрати('.'): raise RuntimeError('upload failed: ' + постави_име)
            갈무리자료 = испрати('hex ' + shlex.quote(постави_име))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != постави_податоци: raise RuntimeError('upload verification failed')
        if област_VALUE == '.java' and Изврши_наредба('javac ' + shlex.quote(Име)) != 0: return 1
        실행가능파일 = аргумент_низа.file.stem + '.elf'
        if област_VALUE == '.c' and Изврши_наредба('cc ' + shlex.quote(Име) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програма = 'java ' + shlex.quote(аргумент_низа.class_name or аргумент_низа.file.stem) if област_VALUE in ('.java', '.class') else ('python ' if област_VALUE == '.py' else 'run ') + shlex.quote(Име)
        if област_VALUE == '.jar': програма = 'java -jar ' + shlex.quote(Име)
        if област_VALUE == '.c': програма = 'run ' + shlex.quote(실행가능파일)
        if аргумент_низа.linux: програма = 'run --linux ' + shlex.quote(Име)
        if аргумент_низа.arguments: програма += ' ' + ' '.join(shlex.quote(низа_податоци) for низа_податоци in аргумент_низа.arguments)
        return 0 if Изврши_наредба(програма) == 0 else 1
    finally:
        if Процес.poll() is None:
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait(timeout=5)
        избирач.close(); Процес.stdin.close(); Процес.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Изврши_2())
