#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. värd 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from köra_kommando import kommando


def Kör():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Namn(예: validera.test_bunt)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI använda_värde')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='Lägga_till_post class filnamn 또는 class 디렉터리(패키지 Namn 유지)')
    argument_MATRIS = parser.parse_args()
    data = argument_MATRIS.file.read_bytes()
    if argument_MATRIS.class_name and argument_MATRIS.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Namn = argument_MATRIS.class_name + '.class' if argument_MATRIS.class_name else argument_MATRIS.file.name
    if len(data) > 16384 or not 1 <= len(Namn.encode('utf-8')) <= 63 or '\n' in Namn or '\r' in Namn:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    område_värde = '.elf' if data[:4] == b'\x7fELF' else argument_MATRIS.file.suffix
    if argument_MATRIS.linux and område_värde != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if område_värde not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_MATRIS.arguments) > 7 or any(len(sträng_data.encode('utf-8')) > 255 or '\n' in sträng_data or '\r' in sträng_data for sträng_data in argument_MATRIS.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Alternativ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_MATRIS.vnc: Alternativ += ['-vnc', argument_MATRIS.vnc]
    Process = subprocess.Popen(kommando() + Alternativ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    väljare = selectors.DefaultSelector(); väljare.register(Process.stdout, selectors.EVENT_READ)
    def få_dokument(markör_8b722c5f, körning_TIMEOUT=45):
        utleverans = bytearray(); avsluta_FÖRSKJUTNING = time.monotonic() + körning_TIMEOUT
        while markör_8b722c5f not in utleverans:
            if time.monotonic() > avsluta_FÖRSKJUTNING: raise RuntimeError('UART timeout: ' + utleverans.decode('utf-8', 'replace'))
            for 누름값, _ in väljare.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: utleverans.extend(조각)
            if b'PANIC:' in utleverans or b'FAIL ' in utleverans: raise RuntimeError(utleverans.decode('utf-8', 'replace'))
            if Process.poll() is not None: raise RuntimeError('QEMU exited: ' + utleverans.decode('utf-8', 'replace'))
        return bytes(utleverans)
    def skicka(inmatningsrad, markör_8b722c5f=b'jkoros-native> '):
        Process.stdin.write(inmatningsrad.encode('utf-8') + b'\n'); Process.stdin.flush()
        return få_dokument(markör_8b722c5f)
    def köra_kommando(inmatningsrad):
        utleverans = skicka(inmatningsrad); sys.stdout.buffer.write(utleverans); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', utleverans)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        få_dokument(b'jkoros-native> ')
        fillista = []
        for ta_med in argument_MATRIS.include:
            if ta_med.is_dir():
                fillista += [(str(data_placera.relative_to(ta_med).with_suffix('')).replace('/', '.') + '.class', data_placera.read_bytes()) for data_placera in sorted(ta_med.rglob('*.class'))]
            else:
                fillista.append((ta_med.name, ta_med.read_bytes()))
        fillista = [(objekt_ANTAL, mål_data) for objekt_ANTAL, mål_data in fillista if objekt_ANTAL != Namn] + [(Namn, data)]
        for Upload_namn, Upload_data in fillista:
            if len(Upload_data) > 16384 or len(Upload_namn.encode('utf-8')) > 63 or '\n' in Upload_namn or '\r' in Upload_namn:
                raise ValueError('Lägga_till_post 파일의 Namn/Storlek 제한 초과: ' + Upload_namn)
            skicka('load ' + shlex.quote(Upload_namn), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): skicka(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in skicka('.'): raise RuntimeError('upload failed: ' + Upload_namn)
            갈무리자료 = skicka('hex ' + shlex.quote(Upload_namn))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if område_värde == '.java' and köra_kommando('javac ' + shlex.quote(Namn)) != 0: return 1
        körbar_fil_BILD = argument_MATRIS.file.stem + '.elf'
        if område_värde == '.c' and köra_kommando('cc ' + shlex.quote(Namn) + ' -o ' + shlex.quote(körbar_fil_BILD)) != 0: return 1
        app = 'java ' + shlex.quote(argument_MATRIS.class_name or argument_MATRIS.file.stem) if område_värde in ('.java', '.class') else ('python ' if område_värde == '.py' else 'run ') + shlex.quote(Namn)
        if område_värde == '.jar': app = 'java -jar ' + shlex.quote(Namn)
        if område_värde == '.c': app = 'run ' + shlex.quote(körbar_fil_BILD)
        if argument_MATRIS.linux: app = 'run --linux ' + shlex.quote(Namn)
        if argument_MATRIS.arguments: app += ' ' + ' '.join(shlex.quote(sträng_data) for sträng_data in argument_MATRIS.arguments)
        return 0 if köra_kommando(app) == 0 else 1
    finally:
        if Process.poll() is None:
            Process.terminate()
            try: Process.wait(timeout=5)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait(timeout=5)
        väljare.close(); Process.stdin.close(); Process.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Kör())
