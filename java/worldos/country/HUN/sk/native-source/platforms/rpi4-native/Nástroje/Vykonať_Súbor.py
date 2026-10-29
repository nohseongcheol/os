#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hostiteľ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Vykonať_príkaz import Príkaz


def Spustiť_2():
    analyzátor = argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('file', type=Path)
    analyzátor.add_argument('arguments', nargs='*')
    analyzátor.add_argument('--class-name', help='패키지가 있는 .class의 전체 Názov(예: overiť_5fb2b747.test_zväzok)')
    analyzátor.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI používať_VALUE')
    analyzátor.add_argument('--vnc', help='예: 127.0.0.1:2')
    analyzátor.add_argument('--include', action='append', type=Path, default=[], help='Pripojiť_položka class Súbor 또는 class 디렉터리(패키지 Názov 유지)')
    argument_pole = analyzátor.parse_args()
    údaje = argument_pole.file.read_bytes()
    if argument_pole.class_name and argument_pole.file.suffix != '.class': analyzátor.error('--class-name은 .class 입력에서 사용합니다.')
    Názov = argument_pole.class_name + '.class' if argument_pole.class_name else argument_pole.file.name
    if len(údaje) > 16384 or not 1 <= len(Názov.encode('utf-8')) <= 63 or '\n' in Názov or '\r' in Názov:
        analyzátor.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    oblasť_VALUE = '.elf' if údaje[:4] == b'\x7fELF' else argument_pole.file.suffix
    if argument_pole.linux and oblasť_VALUE != '.elf': analyzátor.error('--linux는 ELF 바이너리에만 사용합니다.')
    if oblasť_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analyzátor.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_pole.arguments) > 7 or any(len(reťazec_údaje.encode('utf-8')) > 255 or '\n' in reťazec_údaje or '\r' in reťazec_údaje for reťazec_údaje in argument_pole.arguments):
        analyzátor.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Možnosti = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_pole.vnc: Možnosti += ['-vnc', argument_pole.vnc]
    Proces = subprocess.Popen(Príkaz() + Možnosti, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
    def dostať_e_mail(fixka, 시간제한=45):
        출력결과 = bytearray(); ukončiť_hovor_Posun = time.monotonic() + 시간제한
        while fixka not in 출력결과:
            if time.monotonic() > ukončiť_hovor_Posun: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in selektor.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def odoslať(riadok, fixka=b'jkoros-native> '):
        Proces.stdin.write(riadok.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return dostať_e_mail(fixka)
    def Vykonať_príkaz(riadok):
        출력결과 = odoslať(riadok); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        dostať_e_mail(b'jkoros-native> ')
        Súbor_Zoznam = []
        for zahrnúť in argument_pole.include:
            if zahrnúť.is_dir():
                Súbor_Zoznam += [(str(údaje_pozícia.relative_to(zahrnúť).with_suffix('')).replace('/', '.') + '.class', údaje_pozícia.read_bytes()) for údaje_pozícia in sorted(zahrnúť.rglob('*.class'))]
            else:
                Súbor_Zoznam.append((zahrnúť.name, zahrnúť.read_bytes()))
        Súbor_Zoznam = [(položka_COUNT, cieľ_údaje) for položka_COUNT, cieľ_údaje in Súbor_Zoznam if položka_COUNT != Názov] + [(Názov, údaje)]
        for nahrať_názov, nahrať_údaje in Súbor_Zoznam:
            if len(nahrať_údaje) > 16384 or len(nahrať_názov.encode('utf-8')) > 63 or '\n' in nahrať_názov or '\r' in nahrať_názov:
                raise ValueError('Pripojiť_položka 파일의 Názov/Veľkosť 제한 초과: ' + nahrať_názov)
            odoslať('load ' + shlex.quote(nahrať_názov), b'hex> ')
            for 순번 in range(0, len(nahrať_údaje), 64): odoslať(nahrať_údaje[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in odoslať('.'): raise RuntimeError('upload failed: ' + nahrať_názov)
            갈무리자료 = odoslať('hex ' + shlex.quote(nahrať_názov))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != nahrať_údaje: raise RuntimeError('upload verification failed')
        if oblasť_VALUE == '.java' and Vykonať_príkaz('javac ' + shlex.quote(Názov)) != 0: return 1
        spustiteľný_súbor_IMAGE = argument_pole.file.stem + '.elf'
        if oblasť_VALUE == '.c' and Vykonať_príkaz('cc ' + shlex.quote(Názov) + ' -o ' + shlex.quote(spustiteľný_súbor_IMAGE)) != 0: return 1
        program = 'java ' + shlex.quote(argument_pole.class_name or argument_pole.file.stem) if oblasť_VALUE in ('.java', '.class') else ('python ' if oblasť_VALUE == '.py' else 'run ') + shlex.quote(Názov)
        if oblasť_VALUE == '.jar': program = 'java -jar ' + shlex.quote(Názov)
        if oblasť_VALUE == '.c': program = 'run ' + shlex.quote(spustiteľný_súbor_IMAGE)
        if argument_pole.linux: program = 'run --linux ' + shlex.quote(Názov)
        if argument_pole.arguments: program += ' ' + ' '.join(shlex.quote(reťazec_údaje) for reťazec_údaje in argument_pole.arguments)
        return 0 if Vykonať_príkaz(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selektor.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Spustiť_2())
