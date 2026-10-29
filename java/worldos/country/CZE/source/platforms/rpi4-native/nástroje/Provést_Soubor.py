#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hostit 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Provést_příkaz import příkaz


def Spustit_2():
    analyzátor = argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('file', type=Path)
    analyzátor.add_argument('arguments', nargs='*')
    analyzátor.add_argument('--class-name', help='패키지가 있는 .class의 전체 Název(예: ověřit_5fb2b747.test_sada)')
    analyzátor.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI použít_HODNOTA')
    analyzátor.add_argument('--vnc', help='예: 127.0.0.1:2')
    analyzátor.add_argument('--include', action='append', type=Path, default=[], help='Připojit_položka class název_souboru 또는 class 디렉터리(패키지 Název 유지)')
    argument_pole = analyzátor.parse_args()
    data = argument_pole.file.read_bytes()
    if argument_pole.class_name and argument_pole.file.suffix != '.class': analyzátor.error('--class-name은 .class 입력에서 사용합니다.')
    Název = argument_pole.class_name + '.class' if argument_pole.class_name else argument_pole.file.name
    if len(data) > 16384 or not 1 <= len(Název.encode('utf-8')) <= 63 or '\n' in Název or '\r' in Název:
        analyzátor.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    oblast_HODNOTA = '.elf' if data[:4] == b'\x7fELF' else argument_pole.file.suffix
    if argument_pole.linux and oblast_HODNOTA != '.elf': analyzátor.error('--linux는 ELF 바이너리에만 사용합니다.')
    if oblast_HODNOTA not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analyzátor.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_pole.arguments) > 7 or any(len(řetězec_data.encode('utf-8')) > 255 or '\n' in řetězec_data or '\r' in řetězec_data for řetězec_data in argument_pole.arguments):
        analyzátor.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Možnosti = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_pole.vnc: Možnosti += ['-vnc', argument_pole.vnc]
    Proces = subprocess.Popen(příkaz() + Možnosti, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
    def dostat_e_mail(značka, spuštění_TIMEOUT=45):
        výstup = bytearray(); konec_POSUN = time.monotonic() + spuštění_TIMEOUT
        while značka not in výstup:
            if time.monotonic() > konec_POSUN: raise RuntimeError('UART timeout: ' + výstup.decode('utf-8', 'replace'))
            for 누름값, _ in selektor.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: výstup.extend(조각)
            if b'PANIC:' in výstup or b'FAIL ' in výstup: raise RuntimeError(výstup.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + výstup.decode('utf-8', 'replace'))
        return bytes(výstup)
    def poslat(vstupní_řádek, značka=b'jkoros-native> '):
        Proces.stdin.write(vstupní_řádek.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return dostat_e_mail(značka)
    def Provést_příkaz(vstupní_řádek):
        výstup = poslat(vstupní_řádek); sys.stdout.buffer.write(výstup); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', výstup)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        dostat_e_mail(b'jkoros-native> ')
        seznam_souborů = []
        for zahrnout in argument_pole.include:
            if zahrnout.is_dir():
                seznam_souborů += [(str(data_pozice.relative_to(zahrnout).with_suffix('')).replace('/', '.') + '.class', data_pozice.read_bytes()) for data_pozice in sorted(zahrnout.rglob('*.class'))]
            else:
                seznam_souborů.append((zahrnout.name, zahrnout.read_bytes()))
        seznam_souborů = [(zboží_POČET, cíl_data) for zboží_POČET, cíl_data in seznam_souborů if zboží_POČET != Název] + [(Název, data)]
        for Upload_název, Upload_data in seznam_souborů:
            if len(Upload_data) > 16384 or len(Upload_název.encode('utf-8')) > 63 or '\n' in Upload_název or '\r' in Upload_název:
                raise ValueError('Připojit_položka 파일의 Název/Velikost 제한 초과: ' + Upload_název)
            poslat('load ' + shlex.quote(Upload_název), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): poslat(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in poslat('.'): raise RuntimeError('upload failed: ' + Upload_název)
            갈무리자료 = poslat('hex ' + shlex.quote(Upload_název))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if oblast_HODNOTA == '.java' and Provést_příkaz('javac ' + shlex.quote(Název)) != 0: return 1
        spustitelný_image = argument_pole.file.stem + '.elf'
        if oblast_HODNOTA == '.c' and Provést_příkaz('cc ' + shlex.quote(Název) + ' -o ' + shlex.quote(spustitelný_image)) != 0: return 1
        program = 'java ' + shlex.quote(argument_pole.class_name or argument_pole.file.stem) if oblast_HODNOTA in ('.java', '.class') else ('python ' if oblast_HODNOTA == '.py' else 'run ') + shlex.quote(Název)
        if oblast_HODNOTA == '.jar': program = 'java -jar ' + shlex.quote(Název)
        if oblast_HODNOTA == '.c': program = 'run ' + shlex.quote(spustitelný_image)
        if argument_pole.linux: program = 'run --linux ' + shlex.quote(Název)
        if argument_pole.arguments: program += ' ' + ' '.join(shlex.quote(řetězec_data) for řetězec_data in argument_pole.arguments)
        return 0 if Provést_příkaz(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selektor.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Spustit_2())
