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
from Изврши_команда import Наредба


def Покрени():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('file', type=Path)
    анализатор.add_argument('arguments', nargs='*')
    анализатор.add_argument('--class-name', help='패키지가 있는 .class의 전체 Назив(예: потврдити_5fb2b747.꾸러미시험)')
    анализатор.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2')
    анализатор.add_argument('--include', action='append', type=Path, default=[], help='додати_унос class Датотека 또는 class 디렉터리(패키지 Назив 유지)')
    аргумент_низ = анализатор.parse_args()
    подаци = аргумент_низ.file.read_bytes()
    if аргумент_низ.class_name and аргумент_низ.file.suffix != '.class': анализатор.error('--class-name은 .class 입력에서 사용합니다.')
    Назив = аргумент_низ.class_name + '.class' if аргумент_низ.class_name else аргумент_низ.file.name
    if len(подаци) > 16384 or not 1 <= len(Назив.encode('utf-8')) <= 63 or '\n' in Назив or '\r' in Назив:
        анализатор.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    област_вриједност = '.elf' if подаци[:4] == b'\x7fELF' else аргумент_низ.file.suffix
    if аргумент_низ.linux and област_вриједност != '.elf': анализатор.error('--linux는 ELF 바이너리에만 사용합니다.')
    if област_вриједност not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        анализатор.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_низ.arguments) > 7 or any(len(ниска_подаци.encode('utf-8')) > 255 or '\n' in ниска_подаци or '\r' in ниска_подаци for ниска_подаци in аргумент_низ.arguments):
        анализатор.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Опције = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_низ.vnc: Опције += ['-vnc', аргумент_низ.vnc]
    Процес = subprocess.Popen(Наредба() + Опције, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    бирач = selectors.DefaultSelector(); бирач.register(Процес.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); завршити_Помак = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > завршити_Помак: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in бирач.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процес.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def послати(Ред, 확인표시=b'jkoros-native> '):
        Процес.stdin.write(Ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
        return 수신하기(확인표시)
    def Изврши_команда(Ред):
        출력결과 = послати(Ред); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        фајл_Листа = []
        for 포함항목 in аргумент_низ.include:
            if 포함항목.is_dir():
                фајл_Листа += [(str(подаци_позиција.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', подаци_позиција.read_bytes()) for подаци_позиција in sorted(포함항목.rglob('*.class'))]
            else:
                фајл_Листа.append((포함항목.name, 포함항목.read_bytes()))
        фајл_Листа = [(개수, одредиште_подаци) for 개수, одредиште_подаци in фајл_Листа if 개수 != Назив] + [(Назив, подаци)]
        for Отпрема_име, Отпрема_подаци in фајл_Листа:
            if len(Отпрема_подаци) > 16384 or len(Отпрема_име.encode('utf-8')) > 63 or '\n' in Отпрема_име or '\r' in Отпрема_име:
                raise ValueError('додати_унос 파일의 Назив/Величина 제한 초과: ' + Отпрема_име)
            послати('load ' + shlex.quote(Отпрема_име), b'hex> ')
            for 순번 in range(0, len(Отпрема_подаци), 64): послати(Отпрема_подаци[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in послати('.'): raise RuntimeError('upload failed: ' + Отпрема_име)
            갈무리자료 = послати('hex ' + shlex.quote(Отпрема_име))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Отпрема_подаци: raise RuntimeError('upload verification failed')
        if област_вриједност == '.java' and Изврши_команда('javac ' + shlex.quote(Назив)) != 0: return 1
        실행가능파일 = аргумент_низ.file.stem + '.elf'
        if област_вриједност == '.c' and Изврши_команда('cc ' + shlex.quote(Назив) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програм = 'java ' + shlex.quote(аргумент_низ.class_name or аргумент_низ.file.stem) if област_вриједност in ('.java', '.class') else ('python ' if област_вриједност == '.py' else 'run ') + shlex.quote(Назив)
        if област_вриједност == '.jar': програм = 'java -jar ' + shlex.quote(Назив)
        if област_вриједност == '.c': програм = 'run ' + shlex.quote(실행가능파일)
        if аргумент_низ.linux: програм = 'run --linux ' + shlex.quote(Назив)
        if аргумент_низ.arguments: програм += ' ' + ' '.join(shlex.quote(ниска_подаци) for ниска_подаци in аргумент_низ.arguments)
        return 0 if Изврши_команда(програм) == 0 else 1
    finally:
        if Процес.poll() is None:
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait(timeout=5)
        бирач.close(); Процес.stdin.close(); Процес.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Покрени())
