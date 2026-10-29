#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. gazdă 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from executa_comandă import Comandă


def Pornește():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nume(예: valida.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI utiliza_VALUE')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='adăuga_intrare class Fișier 또는 class 디렉터리(패키지 Nume 유지)')
    argument_ARRAY = parser.parse_args()
    date = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nume = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(date) > 16384 or not 1 <= len(Nume.encode('utf-8')) <= 63 or '\n' in Nume or '\r' in Nume:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    zonă_VALUE = '.elf' if date[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and zonă_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if zonă_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(șir_date.encode('utf-8')) > 255 or '\n' in șir_date or '\r' in șir_date for șir_date in argument_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opțiuni = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Opțiuni += ['-vnc', argument_ARRAY.vnc]
    Proces = subprocess.Popen(Comandă() + Opțiuni, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector = selectors.DefaultSelector(); selector.register(Proces.stdout, selectors.EVENT_READ)
    def primi_mesaj(marcaj, executare_TIMEOUT=45):
        출력결과 = bytearray(); termina_un_apel_OFFSET = time.monotonic() + executare_TIMEOUT
        while marcaj not in 출력결과:
            if time.monotonic() > termina_un_apel_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in selector.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def trimite(Linie, marcaj=b'jkoros-native> '):
        Proces.stdin.write(Linie.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return primi_mesaj(marcaj)
    def executa_comandă(Linie):
        출력결과 = trimite(Linie); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        primi_mesaj(b'jkoros-native> ')
        Fișier_Listă = []
        for include in argument_ARRAY.include:
            if include.is_dir():
                Fișier_Listă += [(str(date_poziție.relative_to(include).with_suffix('')).replace('/', '.') + '.class', date_poziție.read_bytes()) for date_poziție in sorted(include.rglob('*.class'))]
            else:
                Fișier_Listă.append((include.name, include.read_bytes()))
        Fișier_Listă = [(element_COUNT, destinație_date) for element_COUNT, destinație_date in Fișier_Listă if element_COUNT != Nume] + [(Nume, date)]
        for Upload_nume, Upload_date in Fișier_Listă:
            if len(Upload_date) > 16384 or len(Upload_nume.encode('utf-8')) > 63 or '\n' in Upload_nume or '\r' in Upload_nume:
                raise ValueError('adăuga_intrare 파일의 Nume/Mărime 제한 초과: ' + Upload_nume)
            trimite('load ' + shlex.quote(Upload_nume), b'hex> ')
            for 순번 in range(0, len(Upload_date), 64): trimite(Upload_date[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in trimite('.'): raise RuntimeError('upload failed: ' + Upload_nume)
            갈무리자료 = trimite('hex ' + shlex.quote(Upload_nume))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_date: raise RuntimeError('upload verification failed')
        if zonă_VALUE == '.java' and executa_comandă('javac ' + shlex.quote(Nume)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if zonă_VALUE == '.c' and executa_comandă('cc ' + shlex.quote(Nume) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if zonă_VALUE in ('.java', '.class') else ('python ' if zonă_VALUE == '.py' else 'run ') + shlex.quote(Nume)
        if zonă_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Nume)
        if zonă_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: program = 'run --linux ' + shlex.quote(Nume)
        if argument_ARRAY.arguments: program += ' ' + ' '.join(shlex.quote(șir_date) for șir_date in argument_ARRAY.arguments)
        return 0 if executa_comandă(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selector.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Pornește())
