#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from eżegwixxa_kmand import kmand


def serje():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 isem(예: vvalida.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class fajl 또는 class 디렉터리(패키지 isem 유지)')
    argument_ARRAY = 인수해석기.parse_args()
    data = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    isem = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(isem.encode('utf-8')) <= 63 or '\n' in isem or '\r' in isem:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategorija_VALUE = '.elf' if data[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and kategorija_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategorija_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(string_data.encode('utf-8')) > 255 or '\n' in string_data or '\r' in string_data for string_data in argument_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Għażliet = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Għażliet += ['-vnc', argument_ARRAY.vnc]
    Proċess = subprocess.Popen(kmand() + Għażliet, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettur = selectors.DefaultSelector(); selettur.register(Proċess.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ttermina_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ttermina_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in selettur.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proċess.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def bagħat(linja, 확인표시=b'jkoros-native> '):
        Proċess.stdin.write(linja.encode('utf-8') + b'\n'); Proċess.stdin.flush()
        return 수신하기(확인표시)
    def eżegwixxa_kmand(linja):
        출력결과 = bagħat(linja); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fajl_Lista = []
        for 포함항목 in argument_ARRAY.include:
            if 포함항목.is_dir():
                fajl_Lista += [(str(data_pożizzjoni.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_pożizzjoni.read_bytes()) for data_pożizzjoni in sorted(포함항목.rglob('*.class'))]
            else:
                fajl_Lista.append((포함항목.name, 포함항목.read_bytes()))
        fajl_Lista = [(element_COUNT, destinazzjoni_data) for element_COUNT, destinazzjoni_data in fajl_Lista if element_COUNT != isem] + [(isem, data)]
        for tella_isem, tella_data in fajl_Lista:
            if len(tella_data) > 16384 or len(tella_isem.encode('utf-8')) > 63 or '\n' in tella_isem or '\r' in tella_isem:
                raise ValueError('추가 파일의 isem/daqqas 제한 초과: ' + tella_isem)
            bagħat('load ' + shlex.quote(tella_isem), b'hex> ')
            for 순번 in range(0, len(tella_data), 64): bagħat(tella_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in bagħat('.'): raise RuntimeError('upload failed: ' + tella_isem)
            갈무리자료 = bagħat('hex ' + shlex.quote(tella_isem))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != tella_data: raise RuntimeError('upload verification failed')
        if kategorija_VALUE == '.java' and eżegwixxa_kmand('javac ' + shlex.quote(isem)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if kategorija_VALUE == '.c' and eżegwixxa_kmand('cc ' + shlex.quote(isem) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programm = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if kategorija_VALUE in ('.java', '.class') else ('python ' if kategorija_VALUE == '.py' else 'run ') + shlex.quote(isem)
        if kategorija_VALUE == '.jar': programm = 'java -jar ' + shlex.quote(isem)
        if kategorija_VALUE == '.c': programm = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: programm = 'run --linux ' + shlex.quote(isem)
        if argument_ARRAY.arguments: programm += ' ' + ' '.join(shlex.quote(string_data) for string_data in argument_ARRAY.arguments)
        return 0 if eżegwixxa_kmand(programm) == 0 else 1
    finally:
        if Proċess.poll() is None:
            Proċess.terminate()
            try: Proċess.wait(timeout=5)
            except subprocess.TimeoutExpired: Proċess.kill(); Proċess.wait(timeout=5)
        selettur.close(); Proċess.stdin.close(); Proċess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(serje())
