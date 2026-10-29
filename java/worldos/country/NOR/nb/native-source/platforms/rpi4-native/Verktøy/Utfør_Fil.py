#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. vert 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Utfør_kommando import Kommando


def Kjør_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Navn(예: bekrefte_5fb2b747.test_bunt)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI bruk_VERDI')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='Tilføye_oppføring class Fil 또는 class 디렉터리(패키지 Navn 유지)')
    argument_MATRISE = parser.parse_args()
    data = argument_MATRISE.file.read_bytes()
    if argument_MATRISE.class_name and argument_MATRISE.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Navn = argument_MATRISE.class_name + '.class' if argument_MATRISE.class_name else argument_MATRISE.file.name
    if len(data) > 16384 or not 1 <= len(Navn.encode('utf-8')) <= 63 or '\n' in Navn or '\r' in Navn:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    område_VERDI = '.elf' if data[:4] == b'\x7fELF' else argument_MATRISE.file.suffix
    if argument_MATRISE.linux and område_VERDI != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if område_VERDI not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_MATRISE.arguments) > 7 or any(len(streng_data.encode('utf-8')) > 255 or '\n' in streng_data or '\r' in streng_data for streng_data in argument_MATRISE.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Alternativer = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_MATRISE.vnc: Alternativer += ['-vnc', argument_MATRISE.vnc]
    Prosess = subprocess.Popen(Kommando() + Alternativer, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    velger = selectors.DefaultSelector(); velger.register(Prosess.stdout, selectors.EVENT_READ)
    def motta_e_post(tusj, kjøring_TIMEOUT=45):
        produksjon = bytearray(); avslutte_en_samtale_FORSKYVNING = time.monotonic() + kjøring_TIMEOUT
        while tusj not in produksjon:
            if time.monotonic() > avslutte_en_samtale_FORSKYVNING: raise RuntimeError('UART timeout: ' + produksjon.decode('utf-8', 'replace'))
            for 누름값, _ in velger.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: produksjon.extend(조각)
            if b'PANIC:' in produksjon or b'FAIL ' in produksjon: raise RuntimeError(produksjon.decode('utf-8', 'replace'))
            if Prosess.poll() is not None: raise RuntimeError('QEMU exited: ' + produksjon.decode('utf-8', 'replace'))
        return bytes(produksjon)
    def sende(Linje, tusj=b'jkoros-native> '):
        Prosess.stdin.write(Linje.encode('utf-8') + b'\n'); Prosess.stdin.flush()
        return motta_e_post(tusj)
    def Utfør_kommando(Linje):
        produksjon = sende(Linje); sys.stdout.buffer.write(produksjon); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', produksjon)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        motta_e_post(b'jkoros-native> ')
        filliste = []
        for inkludere in argument_MATRISE.include:
            if inkludere.is_dir():
                filliste += [(str(data_plassere.relative_to(inkludere).with_suffix('')).replace('/', '.') + '.class', data_plassere.read_bytes()) for data_plassere in sorted(inkludere.rglob('*.class'))]
            else:
                filliste.append((inkludere.name, inkludere.read_bytes()))
        filliste = [(vare_ANTALL, mål_data) for vare_ANTALL, mål_data in filliste if vare_ANTALL != Navn] + [(Navn, data)]
        for Upload_navn, Upload_data in filliste:
            if len(Upload_data) > 16384 or len(Upload_navn.encode('utf-8')) > 63 or '\n' in Upload_navn or '\r' in Upload_navn:
                raise ValueError('Tilføye_oppføring 파일의 Navn/Størrelse 제한 초과: ' + Upload_navn)
            sende('load ' + shlex.quote(Upload_navn), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): sende(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in sende('.'): raise RuntimeError('upload failed: ' + Upload_navn)
            갈무리자료 = sende('hex ' + shlex.quote(Upload_navn))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if område_VERDI == '.java' and Utfør_kommando('javac ' + shlex.quote(Navn)) != 0: return 1
        kjørbar_fil_BILDE = argument_MATRISE.file.stem + '.elf'
        if område_VERDI == '.c' and Utfør_kommando('cc ' + shlex.quote(Navn) + ' -o ' + shlex.quote(kjørbar_fil_BILDE)) != 0: return 1
        app = 'java ' + shlex.quote(argument_MATRISE.class_name or argument_MATRISE.file.stem) if område_VERDI in ('.java', '.class') else ('python ' if område_VERDI == '.py' else 'run ') + shlex.quote(Navn)
        if område_VERDI == '.jar': app = 'java -jar ' + shlex.quote(Navn)
        if område_VERDI == '.c': app = 'run ' + shlex.quote(kjørbar_fil_BILDE)
        if argument_MATRISE.linux: app = 'run --linux ' + shlex.quote(Navn)
        if argument_MATRISE.arguments: app += ' ' + ' '.join(shlex.quote(streng_data) for streng_data in argument_MATRISE.arguments)
        return 0 if Utfør_kommando(app) == 0 else 1
    finally:
        if Prosess.poll() is None:
            Prosess.terminate()
            try: Prosess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait(timeout=5)
        velger.close(); Prosess.stdin.close(); Prosess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Kjør_2())
