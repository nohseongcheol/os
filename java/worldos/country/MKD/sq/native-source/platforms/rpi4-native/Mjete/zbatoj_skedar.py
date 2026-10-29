#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. pritës 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from zbatoj_komandë import Komanda


def Ekzekuto():
    analizues = argparse.ArgumentParser(description=__doc__)
    analizues.add_argument('file', type=Path)
    analizues.add_argument('arguments', nargs='*')
    analizues.add_argument('--class-name', help='패키지가 있는 .class의 전체 Emër(예: vlerësoj.꾸러미시험)')
    analizues.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    analizues.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizues.add_argument('--include', action='append', type=Path, default=[], help='추가 class Kartelë 또는 class 디렉터리(패키지 Emër 유지)')
    argument_ARRAY = analizues.parse_args()
    të_dhëna = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': analizues.error('--class-name은 .class 입력에서 사용합니다.')
    Emër = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(të_dhëna) > 16384 or not 1 <= len(Emër.encode('utf-8')) <= 63 or '\n' in Emër or '\r' in Emër:
        analizues.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategori_VALUE = '.elf' if të_dhëna[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and kategori_VALUE != '.elf': analizues.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategori_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizues.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(varg_të_dhëna.encode('utf-8')) > 255 or '\n' in varg_të_dhëna or '\r' in varg_të_dhëna for varg_të_dhëna in argument_ARRAY.arguments):
        analizues.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opsione = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Opsione += ['-vnc', argument_ARRAY.vnc]
    Proçes = subprocess.Popen(Komanda() + Opsione, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    përzgjedhësi = selectors.DefaultSelector(); përzgjedhësi.register(Proçes.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); mbaroj_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > mbaroj_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in përzgjedhësi.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proçes.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def dërgoj(linjë, 확인표시=b'jkoros-native> '):
        Proçes.stdin.write(linjë.encode('utf-8') + b'\n'); Proçes.stdin.flush()
        return 수신하기(확인표시)
    def zbatoj_komandë(linjë):
        출력결과 = dërgoj(linjë); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        skedar_Listë = []
        for 포함항목 in argument_ARRAY.include:
            if 포함항목.is_dir():
                skedar_Listë += [(str(të_dhëna_pozicioni.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', të_dhëna_pozicioni.read_bytes()) for të_dhëna_pozicioni in sorted(포함항목.rglob('*.class'))]
            else:
                skedar_Listë.append((포함항목.name, 포함항목.read_bytes()))
        skedar_Listë = [(njësi_COUNT, vendmbërritje_të_dhëna) for njësi_COUNT, vendmbërritje_të_dhëna in skedar_Listë if njësi_COUNT != Emër] + [(Emër, të_dhëna)]
        for Ngarkim_emër, Ngarkim_të_dhëna in skedar_Listë:
            if len(Ngarkim_të_dhëna) > 16384 or len(Ngarkim_emër.encode('utf-8')) > 63 or '\n' in Ngarkim_emër or '\r' in Ngarkim_emër:
                raise ValueError('추가 파일의 Emër/Madhësi 제한 초과: ' + Ngarkim_emër)
            dërgoj('load ' + shlex.quote(Ngarkim_emër), b'hex> ')
            for 순번 in range(0, len(Ngarkim_të_dhëna), 64): dërgoj(Ngarkim_të_dhëna[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in dërgoj('.'): raise RuntimeError('upload failed: ' + Ngarkim_emër)
            갈무리자료 = dërgoj('hex ' + shlex.quote(Ngarkim_emër))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Ngarkim_të_dhëna: raise RuntimeError('upload verification failed')
        if kategori_VALUE == '.java' and zbatoj_komandë('javac ' + shlex.quote(Emër)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if kategori_VALUE == '.c' and zbatoj_komandë('cc ' + shlex.quote(Emër) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if kategori_VALUE in ('.java', '.class') else ('python ' if kategori_VALUE == '.py' else 'run ') + shlex.quote(Emër)
        if kategori_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Emër)
        if kategori_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: program = 'run --linux ' + shlex.quote(Emër)
        if argument_ARRAY.arguments: program += ' ' + ' '.join(shlex.quote(varg_të_dhëna) for varg_të_dhëna in argument_ARRAY.arguments)
        return 0 if zbatoj_komandë(program) == 0 else 1
    finally:
        if Proçes.poll() is None:
            Proçes.terminate()
            try: Proçes.wait(timeout=5)
            except subprocess.TimeoutExpired: Proçes.kill(); Proçes.wait(timeout=5)
        përzgjedhësi.close(); Proçes.stdin.close(); Proçes.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Ekzekuto())
