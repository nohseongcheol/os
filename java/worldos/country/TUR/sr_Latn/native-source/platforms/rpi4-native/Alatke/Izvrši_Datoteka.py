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
from Izvrši_komanda import komanda


def koristiti():
    analizator = argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('file', type=Path)
    analizator.add_argument('arguments', nargs='*')
    analizator.add_argument('--class-name', help='패키지가 있는 .class의 전체 ime(예: potvrditi.꾸러미시험)')
    analizator.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI koristiti_VALUE')
    analizator.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizator.add_argument('--include', action='append', type=Path, default=[], help='dodati_stavka class Datoteka 또는 class 디렉터리(패키지 ime 유지)')
    argument_niz = analizator.parse_args()
    podaci = argument_niz.file.read_bytes()
    if argument_niz.class_name and argument_niz.file.suffix != '.class': analizator.error('--class-name은 .class 입력에서 사용합니다.')
    ime = argument_niz.class_name + '.class' if argument_niz.class_name else argument_niz.file.name
    if len(podaci) > 16384 or not 1 <= len(ime.encode('utf-8')) <= 63 or '\n' in ime or '\r' in ime:
        analizator.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    oblast_VALUE = '.elf' if podaci[:4] == b'\x7fELF' else argument_niz.file.suffix
    if argument_niz.linux and oblast_VALUE != '.elf': analizator.error('--linux는 ELF 바이너리에만 사용합니다.')
    if oblast_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizator.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_niz.arguments) > 7 or any(len(niska_podaci.encode('utf-8')) > 255 or '\n' in niska_podaci or '\r' in niska_podaci for niska_podaci in argument_niz.arguments):
        analizator.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcije = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_niz.vnc: Opcije += ['-vnc', argument_niz.vnc]
    Proces = subprocess.Popen(komanda() + Opcije, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač = selectors.DefaultSelector(); birač.register(Proces.stdout, selectors.EVENT_READ)
    def primiti_poruka(označivač, 시간제한=45):
        출력결과 = bytearray(); završiti_razgovor_Pomak = time.monotonic() + 시간제한
        while označivač not in 출력결과:
            if time.monotonic() > završiti_razgovor_Pomak: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in birač.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def poslati(red, označivač=b'jkoros-native> '):
        Proces.stdin.write(red.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return primiti_poruka(označivač)
    def Izvrši_komanda(red):
        출력결과 = poslati(red); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        primiti_poruka(b'jkoros-native> ')
        Datoteka_Lista = []
        for uključiti in argument_niz.include:
            if uključiti.is_dir():
                Datoteka_Lista += [(str(podaci_pozicija.relative_to(uključiti).with_suffix('')).replace('/', '.') + '.class', podaci_pozicija.read_bytes()) for podaci_pozicija in sorted(uključiti.rglob('*.class'))]
            else:
                Datoteka_Lista.append((uključiti.name, uključiti.read_bytes()))
        Datoteka_Lista = [(stavka_COUNT, odredište_podaci) for stavka_COUNT, odredište_podaci in Datoteka_Lista if stavka_COUNT != ime] + [(ime, podaci)]
        for Otprema_ime, Otprema_podaci in Datoteka_Lista:
            if len(Otprema_podaci) > 16384 or len(Otprema_ime.encode('utf-8')) > 63 or '\n' in Otprema_ime or '\r' in Otprema_ime:
                raise ValueError('dodati_stavka 파일의 ime/promeniti_veličinu 제한 초과: ' + Otprema_ime)
            poslati('load ' + shlex.quote(Otprema_ime), b'hex> ')
            for 순번 in range(0, len(Otprema_podaci), 64): poslati(Otprema_podaci[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in poslati('.'): raise RuntimeError('upload failed: ' + Otprema_ime)
            갈무리자료 = poslati('hex ' + shlex.quote(Otprema_ime))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Otprema_podaci: raise RuntimeError('upload verification failed')
        if oblast_VALUE == '.java' and Izvrši_komanda('javac ' + shlex.quote(ime)) != 0: return 1
        실행가능파일 = argument_niz.file.stem + '.elf'
        if oblast_VALUE == '.c' and Izvrši_komanda('cc ' + shlex.quote(ime) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_niz.class_name or argument_niz.file.stem) if oblast_VALUE in ('.java', '.class') else ('python ' if oblast_VALUE == '.py' else 'run ') + shlex.quote(ime)
        if oblast_VALUE == '.jar': program = 'java -jar ' + shlex.quote(ime)
        if oblast_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_niz.linux: program = 'run --linux ' + shlex.quote(ime)
        if argument_niz.arguments: program += ' ' + ' '.join(shlex.quote(niska_podaci) for niska_podaci in argument_niz.arguments)
        return 0 if Izvrši_komanda(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        birač.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(koristiti())
