#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. vært 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Udfør_kommando import Kommando


def Kør_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Navn(예: bekræfte_5fb2b747.test_bundt)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI brug_VÆRDI')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='tilføj_post class Fil 또는 class 디렉터리(패키지 Navn 유지)')
    argument_MATRIX = parser.parse_args()
    data = argument_MATRIX.file.read_bytes()
    if argument_MATRIX.class_name and argument_MATRIX.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Navn = argument_MATRIX.class_name + '.class' if argument_MATRIX.class_name else argument_MATRIX.file.name
    if len(data) > 16384 or not 1 <= len(Navn.encode('utf-8')) <= 63 or '\n' in Navn or '\r' in Navn:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    område_VÆRDI = '.elf' if data[:4] == b'\x7fELF' else argument_MATRIX.file.suffix
    if argument_MATRIX.linux and område_VÆRDI != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if område_VÆRDI not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_MATRIX.arguments) > 7 or any(len(streng_data.encode('utf-8')) > 255 or '\n' in streng_data or '\r' in streng_data for streng_data in argument_MATRIX.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Indstillinger_7f769d16 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_MATRIX.vnc: Indstillinger_7f769d16 += ['-vnc', argument_MATRIX.vnc]
    Proces = subprocess.Popen(Kommando() + Indstillinger_7f769d16, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
    def modtage_mail(mærke, udførelse_TIMEOUT=45):
        produktoutput = bytearray(); afslutte_et_opkald_FORSKYDNING = time.monotonic() + udførelse_TIMEOUT
        while mærke not in produktoutput:
            if time.monotonic() > afslutte_et_opkald_FORSKYDNING: raise RuntimeError('UART timeout: ' + produktoutput.decode('utf-8', 'replace'))
            for 누름값, _ in selektor.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: produktoutput.extend(조각)
            if b'PANIC:' in produktoutput or b'FAIL ' in produktoutput: raise RuntimeError(produktoutput.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + produktoutput.decode('utf-8', 'replace'))
        return bytes(produktoutput)
    def maile(Linje, mærke=b'jkoros-native> '):
        Proces.stdin.write(Linje.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return modtage_mail(mærke)
    def Udfør_kommando(Linje):
        produktoutput = maile(Linje); sys.stdout.buffer.write(produktoutput); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', produktoutput)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        modtage_mail(b'jkoros-native> ')
        filliste = []
        for inkludere in argument_MATRIX.include:
            if inkludere.is_dir():
                filliste += [(str(data_placere.relative_to(inkludere).with_suffix('')).replace('/', '.') + '.class', data_placere.read_bytes()) for data_placere in sorted(inkludere.rglob('*.class'))]
            else:
                filliste.append((inkludere.name, inkludere.read_bytes()))
        filliste = [(vare_TÆL, destination_data) for vare_TÆL, destination_data in filliste if vare_TÆL != Navn] + [(Navn, data)]
        for Upload_navn, Upload_data in filliste:
            if len(Upload_data) > 16384 or len(Upload_navn.encode('utf-8')) > 63 or '\n' in Upload_navn or '\r' in Upload_navn:
                raise ValueError('tilføj_post 파일의 Navn/Størrelse 제한 초과: ' + Upload_navn)
            maile('load ' + shlex.quote(Upload_navn), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): maile(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in maile('.'): raise RuntimeError('upload failed: ' + Upload_navn)
            갈무리자료 = maile('hex ' + shlex.quote(Upload_navn))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if område_VÆRDI == '.java' and Udfør_kommando('javac ' + shlex.quote(Navn)) != 0: return 1
        eksekverbar_fil_Image = argument_MATRIX.file.stem + '.elf'
        if område_VÆRDI == '.c' and Udfør_kommando('cc ' + shlex.quote(Navn) + ' -o ' + shlex.quote(eksekverbar_fil_Image)) != 0: return 1
        app = 'java ' + shlex.quote(argument_MATRIX.class_name or argument_MATRIX.file.stem) if område_VÆRDI in ('.java', '.class') else ('python ' if område_VÆRDI == '.py' else 'run ') + shlex.quote(Navn)
        if område_VÆRDI == '.jar': app = 'java -jar ' + shlex.quote(Navn)
        if område_VÆRDI == '.c': app = 'run ' + shlex.quote(eksekverbar_fil_Image)
        if argument_MATRIX.linux: app = 'run --linux ' + shlex.quote(Navn)
        if argument_MATRIX.arguments: app += ' ' + ' '.join(shlex.quote(streng_data) for streng_data in argument_MATRIX.arguments)
        return 0 if Udfør_kommando(app) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selektor.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Kør_2())
