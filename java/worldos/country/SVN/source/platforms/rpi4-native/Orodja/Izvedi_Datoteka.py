#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. gostiti 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Izvedi_ukaz import Ukaz


def Zaženi():
    razčlenjevalnik = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik.add_argument('file', type=Path)
    razčlenjevalnik.add_argument('arguments', nargs='*')
    razčlenjevalnik.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ime(예: preveriti_veljavnost.preskusiti_sveženj)')
    razčlenjevalnik.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI uporaba_VALUE')
    razčlenjevalnik.add_argument('--vnc', help='예: 127.0.0.1:2')
    razčlenjevalnik.add_argument('--include', action='append', type=Path, default=[], help='dodati_vnos class Datoteka 또는 class 디렉터리(패키지 Ime 유지)')
    argument_ARRAY = razčlenjevalnik.parse_args()
    podatki = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': razčlenjevalnik.error('--class-name은 .class 입력에서 사용합니다.')
    Ime = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(podatki) > 16384 or not 1 <= len(Ime.encode('utf-8')) <= 63 or '\n' in Ime or '\r' in Ime:
        razčlenjevalnik.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    območje_VALUE = '.elf' if podatki[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and območje_VALUE != '.elf': razčlenjevalnik.error('--linux는 ELF 바이너리에만 사용합니다.')
    if območje_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        razčlenjevalnik.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(niz_podatki.encode('utf-8')) > 255 or '\n' in niz_podatki or '\r' in niz_podatki for niz_podatki in argument_ARRAY.arguments):
        razčlenjevalnik.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Možnosti = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Možnosti += ['-vnc', argument_ARRAY.vnc]
    Opravilo = subprocess.Popen(Ukaz() + Možnosti, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    izbirnik = selectors.DefaultSelector(); izbirnik.register(Opravilo.stdout, selectors.EVENT_READ)
    def sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka, 시간제한=45):
        출력결과 = bytearray(); končati_klic_odmik = time.monotonic() + 시간제한
        while oznaka not in 출력결과:
            if time.monotonic() > končati_klic_odmik: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in izbirnik.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Opravilo.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def poslati(Črtni, oznaka=b'jkoros-native> '):
        Opravilo.stdin.write(Črtni.encode('utf-8') + b'\n'); Opravilo.stdin.flush()
        return sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka)
    def Izvedi_ukaz(Črtni):
        출력결과 = poslati(Črtni); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ')
        Datoteka_Seznam = []
        for vključevati in argument_ARRAY.include:
            if vključevati.is_dir():
                Datoteka_Seznam += [(str(podatki_položaj.relative_to(vključevati).with_suffix('')).replace('/', '.') + '.class', podatki_položaj.read_bytes()) for podatki_položaj in sorted(vključevati.rglob('*.class'))]
            else:
                Datoteka_Seznam.append((vključevati.name, vključevati.read_bytes()))
        Datoteka_Seznam = [(element_COUNT, cilj_podatki) for element_COUNT, cilj_podatki in Datoteka_Seznam if element_COUNT != Ime] + [(Ime, podatki)]
        for Upload_ime, Upload_podatki in Datoteka_Seznam:
            if len(Upload_podatki) > 16384 or len(Upload_ime.encode('utf-8')) > 63 or '\n' in Upload_ime or '\r' in Upload_ime:
                raise ValueError('dodati_vnos 파일의 Ime/Velikost 제한 초과: ' + Upload_ime)
            poslati('load ' + shlex.quote(Upload_ime), b'hex> ')
            for 순번 in range(0, len(Upload_podatki), 64): poslati(Upload_podatki[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in poslati('.'): raise RuntimeError('upload failed: ' + Upload_ime)
            갈무리자료 = poslati('hex ' + shlex.quote(Upload_ime))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_podatki: raise RuntimeError('upload verification failed')
        if območje_VALUE == '.java' and Izvedi_ukaz('javac ' + shlex.quote(Ime)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if območje_VALUE == '.c' and Izvedi_ukaz('cc ' + shlex.quote(Ime) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        aplikacija = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if območje_VALUE in ('.java', '.class') else ('python ' if območje_VALUE == '.py' else 'run ') + shlex.quote(Ime)
        if območje_VALUE == '.jar': aplikacija = 'java -jar ' + shlex.quote(Ime)
        if območje_VALUE == '.c': aplikacija = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: aplikacija = 'run --linux ' + shlex.quote(Ime)
        if argument_ARRAY.arguments: aplikacija += ' ' + ' '.join(shlex.quote(niz_podatki) for niz_podatki in argument_ARRAY.arguments)
        return 0 if Izvedi_ukaz(aplikacija) == 0 else 1
    finally:
        if Opravilo.poll() is None:
            Opravilo.terminate()
            try: Opravilo.wait(timeout=5)
            except subprocess.TimeoutExpired: Opravilo.kill(); Opravilo.wait(timeout=5)
        izbirnik.close(); Opravilo.stdin.close(); Opravilo.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Zaženi())
