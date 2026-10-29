#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. domaćin 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Izvrši_naredba import Naredba


def Pokreni():
    analizator = argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('file', type=Path)
    analizator.add_argument('arguments', nargs='*')
    analizator.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ime(예: potvrditi.꾸러미시험)')
    analizator.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI uporaba_VALUE')
    analizator.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizator.add_argument('--include', action='append', type=Path, default=[], help='dodati_unos class Datoteka 또는 class 디렉터리(패키지 Ime 유지)')
    argument_ARRAY = analizator.parse_args()
    podaci = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': analizator.error('--class-name은 .class 입력에서 사용합니다.')
    Ime = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(podaci) > 16384 or not 1 <= len(Ime.encode('utf-8')) <= 63 or '\n' in Ime or '\r' in Ime:
        analizator.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    područje_VALUE = '.elf' if podaci[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and područje_VALUE != '.elf': analizator.error('--linux는 ELF 바이너리에만 사용합니다.')
    if područje_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizator.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(niz_podaci.encode('utf-8')) > 255 or '\n' in niz_podaci or '\r' in niz_podaci for niz_podaci in argument_ARRAY.arguments):
        analizator.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Mogućnosti = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Mogućnosti += ['-vnc', argument_ARRAY.vnc]
    Proces = subprocess.Popen(Naredba() + Mogućnosti, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    odabirač = selectors.DefaultSelector(); odabirač.register(Proces.stdout, selectors.EVENT_READ)
    def primiti_poruka(marker, 시간제한=45):
        출력결과 = bytearray(); završiti_razgovor_pomak = time.monotonic() + 시간제한
        while marker not in 출력결과:
            if time.monotonic() > završiti_razgovor_pomak: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in odabirač.select(0.1):
                fragment_VALUE = 누름값.fileobj.read(4096)
                if fragment_VALUE: 출력결과.extend(fragment_VALUE)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def slati(red, marker=b'jkoros-native> '):
        Proces.stdin.write(red.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return primiti_poruka(marker)
    def Izvrši_naredba(red):
        출력결과 = slati(red); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        primiti_poruka(b'jkoros-native> ')
        Datoteka_Popis = []
        for obuhvaćati in argument_ARRAY.include:
            if obuhvaćati.is_dir():
                Datoteka_Popis += [(str(podaci_položaj.relative_to(obuhvaćati).with_suffix('')).replace('/', '.') + '.class', podaci_položaj.read_bytes()) for podaci_položaj in sorted(obuhvaćati.rglob('*.class'))]
            else:
                Datoteka_Popis.append((obuhvaćati.name, obuhvaćati.read_bytes()))
        Datoteka_Popis = [(artikl_COUNT, odredište_podaci) for artikl_COUNT, odredište_podaci in Datoteka_Popis if artikl_COUNT != Ime] + [(Ime, podaci)]
        for Prijenos_naziv_3f24218e, Prijenos_podaci in Datoteka_Popis:
            if len(Prijenos_podaci) > 16384 or len(Prijenos_naziv_3f24218e.encode('utf-8')) > 63 or '\n' in Prijenos_naziv_3f24218e or '\r' in Prijenos_naziv_3f24218e:
                raise ValueError('dodati_unos 파일의 Ime/Veličina 제한 초과: ' + Prijenos_naziv_3f24218e)
            slati('load ' + shlex.quote(Prijenos_naziv_3f24218e), b'hex> ')
            for 순번 in range(0, len(Prijenos_podaci), 64): slati(Prijenos_podaci[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in slati('.'): raise RuntimeError('upload failed: ' + Prijenos_naziv_3f24218e)
            갈무리자료 = slati('hex ' + shlex.quote(Prijenos_naziv_3f24218e))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Prijenos_podaci: raise RuntimeError('upload verification failed')
        if područje_VALUE == '.java' and Izvrši_naredba('javac ' + shlex.quote(Ime)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if područje_VALUE == '.c' and Izvrši_naredba('cc ' + shlex.quote(Ime) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        program = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if područje_VALUE in ('.java', '.class') else ('python ' if područje_VALUE == '.py' else 'run ') + shlex.quote(Ime)
        if područje_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Ime)
        if područje_VALUE == '.c': program = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: program = 'run --linux ' + shlex.quote(Ime)
        if argument_ARRAY.arguments: program += ' ' + ' '.join(shlex.quote(niz_podaci) for niz_podaci in argument_ARRAY.arguments)
        return 0 if Izvrši_naredba(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        odabirač.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Pokreni())
