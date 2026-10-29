#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hou 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from uitvoer_bevel import Opdrag


def Loop():
    ontleder = argparse.ArgumentParser(description=__doc__)
    ontleder.add_argument('file', type=Path)
    ontleder.add_argument('arguments', nargs='*')
    ontleder.add_argument('--class-name', help='패키지가 있는 .class의 전체 Naam(예: valideer.꾸러미시험)')
    ontleder.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    ontleder.add_argument('--vnc', help='예: 127.0.0.1:2')
    ontleder.add_argument('--include', action='append', type=Path, default=[], help='추가 class Lêer 또는 class 디렉터리(패키지 Naam 유지)')
    argument_ARRAY = ontleder.parse_args()
    data = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': ontleder.error('--class-name은 .class 입력에서 사용합니다.')
    Naam = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(Naam.encode('utf-8')) <= 63 or '\n' in Naam or '\r' in Naam:
        ontleder.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategorie_VALUE = '.elf' if data[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and kategorie_VALUE != '.elf': ontleder.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategorie_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ontleder.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(string_data.encode('utf-8')) > 255 or '\n' in string_data or '\r' in string_data for string_data in argument_ARRAY.arguments):
        ontleder.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    opsies = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: opsies += ['-vnc', argument_ARRAY.vnc]
    Proses = subprocess.Popen(Opdrag() + opsies, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selekteerder = selectors.DefaultSelector(); selekteerder.register(Proses.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); beëindig_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > beëindig_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in selekteerder.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def e_pos(lyn, 확인표시=b'jkoros-native> '):
        Proses.stdin.write(lyn.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return 수신하기(확인표시)
    def uitvoer_bevel(lyn):
        출력결과 = e_pos(lyn); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        lêer_Lys = []
        for 포함항목 in argument_ARRAY.include:
            if 포함항목.is_dir():
                lêer_Lys += [(str(data_plaas.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_plaas.read_bytes()) for data_plaas in sorted(포함항목.rglob('*.class'))]
            else:
                lêer_Lys.append((포함항목.name, 포함항목.read_bytes()))
        lêer_Lys = [(item_COUNT, bestemming_data) for item_COUNT, bestemming_data in lêer_Lys if item_COUNT != Naam] + [(Naam, data)]
        for oplaai_naam, oplaai_data in lêer_Lys:
            if len(oplaai_data) > 16384 or len(oplaai_naam.encode('utf-8')) > 63 or '\n' in oplaai_naam or '\r' in oplaai_naam:
                raise ValueError('추가 파일의 Naam/Grootte 제한 초과: ' + oplaai_naam)
            e_pos('load ' + shlex.quote(oplaai_naam), b'hex> ')
            for 순번 in range(0, len(oplaai_data), 64): e_pos(oplaai_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in e_pos('.'): raise RuntimeError('upload failed: ' + oplaai_naam)
            갈무리자료 = e_pos('hex ' + shlex.quote(oplaai_naam))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != oplaai_data: raise RuntimeError('upload verification failed')
        if kategorie_VALUE == '.java' and uitvoer_bevel('javac ' + shlex.quote(Naam)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if kategorie_VALUE == '.c' and uitvoer_bevel('cc ' + shlex.quote(Naam) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if kategorie_VALUE in ('.java', '.class') else ('python ' if kategorie_VALUE == '.py' else 'run ') + shlex.quote(Naam)
        if kategorie_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Naam)
        if kategorie_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: program = 'run --linux ' + shlex.quote(Naam)
        if argument_ARRAY.arguments: program += ' ' + ' '.join(shlex.quote(string_data) for string_data in argument_ARRAY.arguments)
        return 0 if uitvoer_bevel(program) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        selekteerder.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Loop())
