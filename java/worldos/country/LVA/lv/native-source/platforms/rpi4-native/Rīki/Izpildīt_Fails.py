#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. viesot 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Izpildīt_komanda import Komanda


def Palaist():
    parsētājs = argparse.ArgumentParser(description=__doc__)
    parsētājs.add_argument('file', type=Path)
    parsētājs.add_argument('arguments', nargs='*')
    parsētājs.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nosaukums(예: validēt.꾸러미시험)')
    parsētājs.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI lietot_VALUE')
    parsētājs.add_argument('--vnc', help='예: 127.0.0.1:2')
    parsētājs.add_argument('--include', action='append', type=Path, default=[], help='Pievienot_ievade class Fails 또는 class 디렉터리(패키지 Nosaukums 유지)')
    arg_ARRAY = parsētājs.parse_args()
    dati = arg_ARRAY.file.read_bytes()
    if arg_ARRAY.class_name and arg_ARRAY.file.suffix != '.class': parsētājs.error('--class-name은 .class 입력에서 사용합니다.')
    Nosaukums = arg_ARRAY.class_name + '.class' if arg_ARRAY.class_name else arg_ARRAY.file.name
    if len(dati) > 16384 or not 1 <= len(Nosaukums.encode('utf-8')) <= 63 or '\n' in Nosaukums or '\r' in Nosaukums:
        parsētājs.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    joma_VALUE = '.elf' if dati[:4] == b'\x7fELF' else arg_ARRAY.file.suffix
    if arg_ARRAY.linux and joma_VALUE != '.elf': parsētājs.error('--linux는 ELF 바이너리에만 사용합니다.')
    if joma_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parsētājs.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arg_ARRAY.arguments) > 7 or any(len(virkne_dati.encode('utf-8')) > 255 or '\n' in virkne_dati or '\r' in virkne_dati for virkne_dati in arg_ARRAY.arguments):
        parsētājs.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcijas = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arg_ARRAY.vnc: Opcijas += ['-vnc', arg_ARRAY.vnc]
    Process = subprocess.Popen(Komanda() + Opcijas, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    atlasītājs = selectors.DefaultSelector(); atlasītājs.register(Process.stdout, selectors.EVENT_READ)
    def saņemt_ziņa(marķieris, 시간제한=45):
        ražojums = bytearray(); beigt_zvanu_Nobīde = time.monotonic() + 시간제한
        while marķieris not in ražojums:
            if time.monotonic() > beigt_zvanu_Nobīde: raise RuntimeError('UART timeout: ' + ražojums.decode('utf-8', 'replace'))
            for 누름값, _ in atlasītājs.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: ražojums.extend(조각)
            if b'PANIC:' in ražojums or b'FAIL ' in ražojums: raise RuntimeError(ražojums.decode('utf-8', 'replace'))
            if Process.poll() is not None: raise RuntimeError('QEMU exited: ' + ražojums.decode('utf-8', 'replace'))
        return bytes(ražojums)
    def sūtīt(Līniju, marķieris=b'jkoros-native> '):
        Process.stdin.write(Līniju.encode('utf-8') + b'\n'); Process.stdin.flush()
        return saņemt_ziņa(marķieris)
    def Izpildīt_komanda(Līniju):
        ražojums = sūtīt(Līniju); sys.stdout.buffer.write(ražojums); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', ražojums)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        saņemt_ziņa(b'jkoros-native> ')
        Fails_Saraksts = []
        for iekļaut in arg_ARRAY.include:
            if iekļaut.is_dir():
                Fails_Saraksts += [(str(dati_amats.relative_to(iekļaut).with_suffix('')).replace('/', '.') + '.class', dati_amats.read_bytes()) for dati_amats in sorted(iekļaut.rglob('*.class'))]
            else:
                Fails_Saraksts.append((iekļaut.name, iekļaut.read_bytes()))
        Fails_Saraksts = [(krājums_COUNT, mērķis_dati) for krājums_COUNT, mērķis_dati in Fails_Saraksts if krājums_COUNT != Nosaukums] + [(Nosaukums, dati)]
        for Upload_nosaukums, Upload_dati in Fails_Saraksts:
            if len(Upload_dati) > 16384 or len(Upload_nosaukums.encode('utf-8')) > 63 or '\n' in Upload_nosaukums or '\r' in Upload_nosaukums:
                raise ValueError('Pievienot_ievade 파일의 Nosaukums/Izmērs 제한 초과: ' + Upload_nosaukums)
            sūtīt('load ' + shlex.quote(Upload_nosaukums), b'hex> ')
            for 순번 in range(0, len(Upload_dati), 64): sūtīt(Upload_dati[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in sūtīt('.'): raise RuntimeError('upload failed: ' + Upload_nosaukums)
            갈무리자료 = sūtīt('hex ' + shlex.quote(Upload_nosaukums))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_dati: raise RuntimeError('upload verification failed')
        if joma_VALUE == '.java' and Izpildīt_komanda('javac ' + shlex.quote(Nosaukums)) != 0: return 1
        izpildāms_fails_IMAGE = arg_ARRAY.file.stem + '.elf'
        if joma_VALUE == '.c' and Izpildīt_komanda('cc ' + shlex.quote(Nosaukums) + ' -o ' + shlex.quote(izpildāms_fails_IMAGE)) != 0: return 1
        programma = 'java ' + shlex.quote(arg_ARRAY.class_name or arg_ARRAY.file.stem) if joma_VALUE in ('.java', '.class') else ('python ' if joma_VALUE == '.py' else 'run ') + shlex.quote(Nosaukums)
        if joma_VALUE == '.jar': programma = 'java -jar ' + shlex.quote(Nosaukums)
        if joma_VALUE == '.c': programma = 'run ' + shlex.quote(izpildāms_fails_IMAGE)
        if arg_ARRAY.linux: programma = 'run --linux ' + shlex.quote(Nosaukums)
        if arg_ARRAY.arguments: programma += ' ' + ' '.join(shlex.quote(virkne_dati) for virkne_dati in arg_ARRAY.arguments)
        return 0 if Izpildīt_komanda(programma) == 0 else 1
    finally:
        if Process.poll() is None:
            Process.terminate()
            try: Process.wait(timeout=5)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait(timeout=5)
        atlasītājs.close(); Process.stdin.close(); Process.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Palaist())
