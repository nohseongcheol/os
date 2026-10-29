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
from Täida_käsk import Käsk


def Käivita_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nimi_2(예: valideerima.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI kasutus_VALUE')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='Lisa_kirje class Fail 또는 class 디렉터리(패키지 Nimi_2 유지)')
    argument_ARRAY = parser.parse_args()
    andmed = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nimi_2 = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(andmed) > 16384 or not 1 <= len(Nimi_2.encode('utf-8')) <= 63 or '\n' in Nimi_2 or '\r' in Nimi_2:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ala_VALUE = '.elf' if andmed[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and ala_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ala_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(string_andmed.encode('utf-8')) > 255 or '\n' in string_andmed or '\r' in string_andmed for string_andmed in argument_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Suvandid = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Suvandid += ['-vnc', argument_ARRAY.vnc]
    Protsess = subprocess.Popen(Käsk() + Suvandid, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valija = selectors.DefaultSelector(); valija.register(Protsess.stdout, selectors.EVENT_READ)
    def saama_meil(marker, 시간제한=45):
        toodang = bytearray(); lõpeta_kõne_nihe = time.monotonic() + 시간제한
        while marker not in toodang:
            if time.monotonic() > lõpeta_kõne_nihe: raise RuntimeError('UART timeout: ' + toodang.decode('utf-8', 'replace'))
            for 누름값, _ in valija.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: toodang.extend(조각)
            if b'PANIC:' in toodang or b'FAIL ' in toodang: raise RuntimeError(toodang.decode('utf-8', 'replace'))
            if Protsess.poll() is not None: raise RuntimeError('QEMU exited: ' + toodang.decode('utf-8', 'replace'))
        return bytes(toodang)
    def saatma(Joon, marker=b'jkoros-native> '):
        Protsess.stdin.write(Joon.encode('utf-8') + b'\n'); Protsess.stdin.flush()
        return saama_meil(marker)
    def Täida_käsk(Joon):
        toodang = saatma(Joon); sys.stdout.buffer.write(toodang); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', toodang)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        saama_meil(b'jkoros-native> ')
        Fail_Loend = []
        for hõlmama in argument_ARRAY.include:
            if hõlmama.is_dir():
                Fail_Loend += [(str(andmed_ametikoht.relative_to(hõlmama).with_suffix('')).replace('/', '.') + '.class', andmed_ametikoht.read_bytes()) for andmed_ametikoht in sorted(hõlmama.rglob('*.class'))]
            else:
                Fail_Loend.append((hõlmama.name, hõlmama.read_bytes()))
        Fail_Loend = [(kaup_COUNT, sihtkoht_andmed) for kaup_COUNT, sihtkoht_andmed in Fail_Loend if kaup_COUNT != Nimi_2] + [(Nimi_2, andmed)]
        for Upload_nimetus, Upload_andmed in Fail_Loend:
            if len(Upload_andmed) > 16384 or len(Upload_nimetus.encode('utf-8')) > 63 or '\n' in Upload_nimetus or '\r' in Upload_nimetus:
                raise ValueError('Lisa_kirje 파일의 Nimi_2/Suurus 제한 초과: ' + Upload_nimetus)
            saatma('load ' + shlex.quote(Upload_nimetus), b'hex> ')
            for 순번 in range(0, len(Upload_andmed), 64): saatma(Upload_andmed[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in saatma('.'): raise RuntimeError('upload failed: ' + Upload_nimetus)
            갈무리자료 = saatma('hex ' + shlex.quote(Upload_nimetus))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_andmed: raise RuntimeError('upload verification failed')
        if ala_VALUE == '.java' and Täida_käsk('javac ' + shlex.quote(Nimi_2)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if ala_VALUE == '.c' and Täida_käsk('cc ' + shlex.quote(Nimi_2) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programm = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if ala_VALUE in ('.java', '.class') else ('python ' if ala_VALUE == '.py' else 'run ') + shlex.quote(Nimi_2)
        if ala_VALUE == '.jar': programm = 'java -jar ' + shlex.quote(Nimi_2)
        if ala_VALUE == '.c': programm = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: programm = 'run --linux ' + shlex.quote(Nimi_2)
        if argument_ARRAY.arguments: programm += ' ' + ' '.join(shlex.quote(string_andmed) for string_andmed in argument_ARRAY.arguments)
        return 0 if Täida_käsk(programm) == 0 else 1
    finally:
        if Protsess.poll() is None:
            Protsess.terminate()
            try: Protsess.wait(timeout=5)
            except subprocess.TimeoutExpired: Protsess.kill(); Protsess.wait(timeout=5)
        valija.close(); Protsess.stdin.close(); Protsess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Käivita_2())
