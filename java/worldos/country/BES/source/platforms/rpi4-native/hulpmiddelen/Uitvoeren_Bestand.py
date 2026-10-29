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
from Uitvoeren_opdracht import opdracht


def starten():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Naam(예: valideren.test_bundel)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI gebruik_WAARDE')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='toevoegen_invoer class bestand 또는 class 디렉터리(패키지 Naam behouden_WAARDE)')
    argument_MATRIX = parser.parse_args()
    gegevens = argument_MATRIX.file.read_bytes()
    if argument_MATRIX.class_name and argument_MATRIX.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Naam = argument_MATRIX.class_name + '.class' if argument_MATRIX.class_name else argument_MATRIX.file.name
    if len(gegevens) > 16384 or not 1 <= len(Naam.encode('utf-8')) <= 63 or '\n' in Naam or '\r' in Naam:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    gebied_WAARDE = '.elf' if gegevens[:4] == b'\x7fELF' else argument_MATRIX.file.suffix
    if argument_MATRIX.linux and gebied_WAARDE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if gebied_WAARDE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_MATRIX.arguments) > 7 or any(len(tekenreeks_gegevens.encode('utf-8')) > 255 or '\n' in tekenreeks_gegevens or '\r' in tekenreeks_gegevens for tekenreeks_gegevens in argument_MATRIX.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opties = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_MATRIX.vnc: Opties += ['-vnc', argument_MATRIX.vnc]
    Proces = subprocess.Popen(opdracht() + Opties, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector = selectors.DefaultSelector(); selector.register(Proces.stdout, selectors.EVENT_READ)
    def ontvangen_e_mail(markering, uitvoerbewerking_TIMEOUT=45):
        uitvoer = bytearray(); beëindigen_VERSCHUIVING = time.monotonic() + uitvoerbewerking_TIMEOUT
        while markering not in uitvoer:
            if time.monotonic() > beëindigen_VERSCHUIVING: raise RuntimeError('UART timeout: ' + uitvoer.decode('utf-8', 'replace'))
            for 누름값, _ in selector.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: uitvoer.extend(조각)
            if b'PANIC:' in uitvoer or b'FAIL ' in uitvoer: raise RuntimeError(uitvoer.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + uitvoer.decode('utf-8', 'replace'))
        return bytes(uitvoer)
    def e_mailen(invoerregel, markering=b'jkoros-native> '):
        Proces.stdin.write(invoerregel.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return ontvangen_e_mail(markering)
    def Uitvoeren_opdracht(invoerregel):
        uitvoer = e_mailen(invoerregel); sys.stdout.buffer.write(uitvoer); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', uitvoer)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        ontvangen_e_mail(b'jkoros-native> ')
        bestandslijst = []
        for bevatten in argument_MATRIX.include:
            if bevatten.is_dir():
                bestandslijst += [(str(gegevens_functie.relative_to(bevatten).with_suffix('')).replace('/', '.') + '.class', gegevens_functie.read_bytes()) for gegevens_functie in sorted(bevatten.rglob('*.class'))]
            else:
                bestandslijst.append((bevatten.name, bevatten.read_bytes()))
        bestandslijst = [(item_AANTAL, doel_gegevens) for item_AANTAL, doel_gegevens in bestandslijst if item_AANTAL != Naam] + [(Naam, gegevens)]
        for Upload_naam, Upload_gegevens in bestandslijst:
            if len(Upload_gegevens) > 16384 or len(Upload_naam.encode('utf-8')) > 63 or '\n' in Upload_naam or '\r' in Upload_naam:
                raise ValueError('toevoegen_invoer 파일의 Naam/Grootte 제한 초과: ' + Upload_naam)
            e_mailen('load ' + shlex.quote(Upload_naam), b'hex> ')
            for 순번 in range(0, len(Upload_gegevens), 64): e_mailen(Upload_gegevens[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in e_mailen('.'): raise RuntimeError('upload failed: ' + Upload_naam)
            갈무리자료 = e_mailen('hex ' + shlex.quote(Upload_naam))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_gegevens: raise RuntimeError('upload verification failed')
        if gebied_WAARDE == '.java' and Uitvoeren_opdracht('javac ' + shlex.quote(Naam)) != 0: return 1
        uitvoerbaar_kopie = argument_MATRIX.file.stem + '.elf'
        if gebied_WAARDE == '.c' and Uitvoeren_opdracht('cc ' + shlex.quote(Naam) + ' -o ' + shlex.quote(uitvoerbaar_kopie)) != 0: return 1
        app = 'java ' + shlex.quote(argument_MATRIX.class_name or argument_MATRIX.file.stem) if gebied_WAARDE in ('.java', '.class') else ('python ' if gebied_WAARDE == '.py' else 'run ') + shlex.quote(Naam)
        if gebied_WAARDE == '.jar': app = 'java -jar ' + shlex.quote(Naam)
        if gebied_WAARDE == '.c': app = 'run ' + shlex.quote(uitvoerbaar_kopie)
        if argument_MATRIX.linux: app = 'run --linux ' + shlex.quote(Naam)
        if argument_MATRIX.arguments: app += ' ' + ' '.join(shlex.quote(tekenreeks_gegevens) for tekenreeks_gegevens in argument_MATRIX.arguments)
        return 0 if Uitvoeren_opdracht(app) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selector.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(starten())
