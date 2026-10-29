#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. хост_рачунар 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import команда


def 시작():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 назив(예: овјерити.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class фајл 또는 class 디렉터리(패키지 назив 유지)')
    аргумент_низ = 인수해석기.parse_args()
    подаци = аргумент_низ.file.read_bytes()
    if аргумент_низ.class_name and аргумент_низ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    назив = аргумент_низ.class_name + '.class' if аргумент_низ.class_name else аргумент_низ.file.name
    if len(подаци) > 16384 or not 1 <= len(назив.encode('utf-8')) <= 63 or '\n' in назив or '\r' in назив:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    категорија_вриједност = '.elf' if подаци[:4] == b'\x7fELF' else аргумент_низ.file.suffix
    if аргумент_низ.linux and категорија_вриједност != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if категорија_вриједност not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_низ.arguments) > 7 or any(len(стринг_подаци.encode('utf-8')) > 255 or '\n' in стринг_подаци or '\r' in стринг_подаци for стринг_подаци in аргумент_низ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Опције = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_низ.vnc: Опције += ['-vnc', аргумент_низ.vnc]
    процес = subprocess.Popen(команда() + Опције, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(процес.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if процес.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def послати(редак, 확인표시=b'jkoros-native> '):
        процес.stdin.write(редак.encode('utf-8') + b'\n'); процес.stdin.flush()
        return 수신하기(확인표시)
    def 실행(редак):
        출력결과 = послати(редак); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        фајл_списак = []
        for 포함항목 in аргумент_низ.include:
            if 포함항목.is_dir():
                фајл_списак += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                фајл_списак.append((포함항목.name, 포함항목.read_bytes()))
        фајл_списак = [(개수, одредиште_подаци) for 개수, одредиште_подаци in фајл_списак if 개수 != назив] + [(назив, подаци)]
        for трансферирати_назив, трансферирати_подаци in фајл_списак:
            if len(трансферирати_подаци) > 16384 or len(трансферирати_назив.encode('utf-8')) > 63 or '\n' in трансферирати_назив or '\r' in трансферирати_назив:
                raise ValueError('추가 파일의 назив/подесити_величину 제한 초과: ' + трансферирати_назив)
            послати('load ' + shlex.quote(трансферирати_назив), b'hex> ')
            for 순번 in range(0, len(трансферирати_подаци), 64): послати(трансферирати_подаци[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in послати('.'): raise RuntimeError('upload failed: ' + трансферирати_назив)
            갈무리자료 = послати('hex ' + shlex.quote(трансферирати_назив))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != трансферирати_подаци: raise RuntimeError('upload verification failed')
        if категорија_вриједност == '.java' and 실행('javac ' + shlex.quote(назив)) != 0: return 1
        실행가능파일 = аргумент_низ.file.stem + '.elf'
        if категорија_вриједност == '.c' and 실행('cc ' + shlex.quote(назив) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програм = 'java ' + shlex.quote(аргумент_низ.class_name or аргумент_низ.file.stem) if категорија_вриједност in ('.java', '.class') else ('python ' if категорија_вриједност == '.py' else 'run ') + shlex.quote(назив)
        if категорија_вриједност == '.jar': програм = 'java -jar ' + shlex.quote(назив)
        if категорија_вриједност == '.c': програм = 'run ' + shlex.quote(실행가능파일)
        if аргумент_низ.linux: програм = 'run --linux ' + shlex.quote(назив)
        if аргумент_низ.arguments: програм += ' ' + ' '.join(shlex.quote(стринг_подаци) for стринг_подаци in аргумент_низ.arguments)
        return 0 if 실행(програм) == 0 else 1
    finally:
        if процес.poll() is None:
            процес.terminate()
            try: процес.wait(timeout=5)
            except subprocess.TimeoutExpired: процес.kill(); процес.wait(timeout=5)
        준비선택기.close(); процес.stdin.close(); процес.stdout.close()


if __name__ == '__main__':
    raise SystemExit(시작())
