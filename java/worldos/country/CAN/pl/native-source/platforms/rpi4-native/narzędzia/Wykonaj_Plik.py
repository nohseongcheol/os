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
from Wykonaj_polecenie import polecenie


def Uruchom_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nazwa(예: walidować.test_pakiet)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI używać_WARTOŚĆ')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='dołączać_wpis class nazwa_pliku 또는 class 디렉터리(패키지 Nazwa 유지)')
    argument_TABLICA = parser.parse_args()
    dane = argument_TABLICA.file.read_bytes()
    if argument_TABLICA.class_name and argument_TABLICA.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nazwa = argument_TABLICA.class_name + '.class' if argument_TABLICA.class_name else argument_TABLICA.file.name
    if len(dane) > 16384 or not 1 <= len(Nazwa.encode('utf-8')) <= 63 or '\n' in Nazwa or '\r' in Nazwa:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    obszar_WARTOŚĆ = '.elf' if dane[:4] == b'\x7fELF' else argument_TABLICA.file.suffix
    if argument_TABLICA.linux and obszar_WARTOŚĆ != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if obszar_WARTOŚĆ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_TABLICA.arguments) > 7 or any(len(ciąg_dane.encode('utf-8')) > 255 or '\n' in ciąg_dane or '\r' in ciąg_dane for ciąg_dane in argument_TABLICA.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opcje = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_TABLICA.vnc: Opcje += ['-vnc', argument_TABLICA.vnc]
    Proces = subprocess.Popen(polecenie() + Opcje, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
    def odbierać_e_mail(pisak, wykonanie_TIMEOUT=45):
        produkt_wyjściowy = bytearray(); Koniec_przesunąć = time.monotonic() + wykonanie_TIMEOUT
        while pisak not in produkt_wyjściowy:
            if time.monotonic() > Koniec_przesunąć: raise RuntimeError('UART timeout: ' + produkt_wyjściowy.decode('utf-8', 'replace'))
            for 누름값, _ in selektor.select(0.1):
                fragment_WARTOŚĆ_652d4b53 = 누름값.fileobj.read(4096)
                if fragment_WARTOŚĆ_652d4b53: produkt_wyjściowy.extend(fragment_WARTOŚĆ_652d4b53)
            if b'PANIC:' in produkt_wyjściowy or b'FAIL ' in produkt_wyjściowy: raise RuntimeError(produkt_wyjściowy.decode('utf-8', 'replace'))
            if Proces.poll() is not None: raise RuntimeError('QEMU exited: ' + produkt_wyjściowy.decode('utf-8', 'replace'))
        return bytes(produkt_wyjściowy)
    def wysłać(wiersz_wejścia, pisak=b'jkoros-native> '):
        Proces.stdin.write(wiersz_wejścia.encode('utf-8') + b'\n'); Proces.stdin.flush()
        return odbierać_e_mail(pisak)
    def Wykonaj_polecenie(wiersz_wejścia):
        produkt_wyjściowy = wysłać(wiersz_wejścia); sys.stdout.buffer.write(produkt_wyjściowy); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', produkt_wyjściowy)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        odbierać_e_mail(b'jkoros-native> ')
        lista_plików = []
        for 포함항목 in argument_TABLICA.include:
            if 포함항목.is_dir():
                lista_plików += [(str(dane_stanowisko.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', dane_stanowisko.read_bytes()) for dane_stanowisko in sorted(포함항목.rglob('*.class'))]
            else:
                lista_plików.append((포함항목.name, 포함항목.read_bytes()))
        lista_plików = [(towar_ILE_LICZB, cel_dane) for towar_ILE_LICZB, cel_dane in lista_plików if towar_ILE_LICZB != Nazwa] + [(Nazwa, dane)]
        for Upload_nazwa, Upload_dane in lista_plików:
            if len(Upload_dane) > 16384 or len(Upload_nazwa.encode('utf-8')) > 63 or '\n' in Upload_nazwa or '\r' in Upload_nazwa:
                raise ValueError('dołączać_wpis 파일의 Nazwa/Rozmiar 제한 초과: ' + Upload_nazwa)
            wysłać('load ' + shlex.quote(Upload_nazwa), b'hex> ')
            for 순번 in range(0, len(Upload_dane), 64): wysłać(Upload_dane[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in wysłać('.'): raise RuntimeError('upload failed: ' + Upload_nazwa)
            갈무리자료 = wysłać('hex ' + shlex.quote(Upload_nazwa))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_dane: raise RuntimeError('upload verification failed')
        if obszar_WARTOŚĆ == '.java' and Wykonaj_polecenie('javac ' + shlex.quote(Nazwa)) != 0: return 1
        wykonywalny_OBRAZ = argument_TABLICA.file.stem + '.elf'
        if obszar_WARTOŚĆ == '.c' and Wykonaj_polecenie('cc ' + shlex.quote(Nazwa) + ' -o ' + shlex.quote(wykonywalny_OBRAZ)) != 0: return 1
        program = 'java ' + shlex.quote(argument_TABLICA.class_name or argument_TABLICA.file.stem) if obszar_WARTOŚĆ in ('.java', '.class') else ('python ' if obszar_WARTOŚĆ == '.py' else 'run ') + shlex.quote(Nazwa)
        if obszar_WARTOŚĆ == '.jar': program = 'java -jar ' + shlex.quote(Nazwa)
        if obszar_WARTOŚĆ == '.c': program = 'run ' + shlex.quote(wykonywalny_OBRAZ)
        if argument_TABLICA.linux: program = 'run --linux ' + shlex.quote(Nazwa)
        if argument_TABLICA.arguments: program += ' ' + ' '.join(shlex.quote(ciąg_dane) for ciąg_dane in argument_TABLICA.arguments)
        return 0 if Wykonaj_polecenie(program) == 0 else 1
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait(timeout=5)
        selektor.close(); Proces.stdin.close(); Proces.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Uruchom_2())
