#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Ostalari 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from exekutatu_komando import Komandoa


def Exekutatu_2():
    analizatzaile = argparse.ArgumentParser(description=__doc__)
    analizatzaile.add_argument('file', type=Path)
    analizatzaile.add_argument('arguments', nargs='*')
    analizatzaile.add_argument('--class-name', help='패키지가 있는 .class의 전체 Izena(예: baliozkotu.꾸러미시험)')
    analizatzaile.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    analizatzaile.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizatzaile.add_argument('--include', action='append', type=Path, default=[], help='Erantsi_sarrera class Fitxategia 또는 class 디렉터리(패키지 Izena 유지)')
    arg_matrize = analizatzaile.parse_args()
    datuak = arg_matrize.file.read_bytes()
    if arg_matrize.class_name and arg_matrize.file.suffix != '.class': analizatzaile.error('--class-name은 .class 입력에서 사용합니다.')
    Izena = arg_matrize.class_name + '.class' if arg_matrize.class_name else arg_matrize.file.name
    if len(datuak) > 16384 or not 1 <= len(Izena.encode('utf-8')) <= 63 or '\n' in Izena or '\r' in Izena:
        analizatzaile.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Kategoria_balio = '.elf' if datuak[:4] == b'\x7fELF' else arg_matrize.file.suffix
    if arg_matrize.linux and Kategoria_balio != '.elf': analizatzaile.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Kategoria_balio not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizatzaile.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arg_matrize.arguments) > 7 or any(len(kate_datuak.encode('utf-8')) > 255 or '\n' in kate_datuak or '\r' in kate_datuak for kate_datuak in arg_matrize.arguments):
        analizatzaile.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    aukerak = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arg_matrize.vnc: aukerak += ['-vnc', arg_matrize.vnc]
    Prozesua = subprocess.Popen(Komandoa() + aukerak, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Prozesua.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); amaitu_Geruzak = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > amaitu_Geruzak: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Prozesua.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def bidali(Marra, 확인표시=b'jkoros-native> '):
        Prozesua.stdin.write(Marra.encode('utf-8') + b'\n'); Prozesua.stdin.flush()
        return 수신하기(확인표시)
    def exekutatu_komando(Marra):
        출력결과 = bidali(Marra); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fitxategi_Zerrenda = []
        for 포함항목 in arg_matrize.include:
            if 포함항목.is_dir():
                fitxategi_Zerrenda += [(str(datuak_kargu.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', datuak_kargu.read_bytes()) for datuak_kargu in sorted(포함항목.rglob('*.class'))]
            else:
                fitxategi_Zerrenda.append((포함항목.name, 포함항목.read_bytes()))
        fitxategi_Zerrenda = [(elementu_ZENBATU, helburu_datuak) for elementu_ZENBATU, helburu_datuak in fitxategi_Zerrenda if elementu_ZENBATU != Izena] + [(Izena, datuak)]
        for Upload_izen, Upload_datuak in fitxategi_Zerrenda:
            if len(Upload_datuak) > 16384 or len(Upload_izen.encode('utf-8')) > 63 or '\n' in Upload_izen or '\r' in Upload_izen:
                raise ValueError('Erantsi_sarrera 파일의 Izena/Tamaina 제한 초과: ' + Upload_izen)
            bidali('load ' + shlex.quote(Upload_izen), b'hex> ')
            for 순번 in range(0, len(Upload_datuak), 64): bidali(Upload_datuak[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in bidali('.'): raise RuntimeError('upload failed: ' + Upload_izen)
            갈무리자료 = bidali('hex ' + shlex.quote(Upload_izen))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_datuak: raise RuntimeError('upload verification failed')
        if Kategoria_balio == '.java' and exekutatu_komando('javac ' + shlex.quote(Izena)) != 0: return 1
        실행가능파일 = arg_matrize.file.stem + '.elf'
        if Kategoria_balio == '.c' and exekutatu_komando('cc ' + shlex.quote(Izena) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        aplik = 'java ' + shlex.quote(arg_matrize.class_name or arg_matrize.file.stem) if Kategoria_balio in ('.java', '.class') else ('python ' if Kategoria_balio == '.py' else 'run ') + shlex.quote(Izena)
        if Kategoria_balio == '.jar': aplik = 'java -jar ' + shlex.quote(Izena)
        if Kategoria_balio == '.c': aplik = 'run ' + shlex.quote(실행가능파일)
        if arg_matrize.linux: aplik = 'run --linux ' + shlex.quote(Izena)
        if arg_matrize.arguments: aplik += ' ' + ' '.join(shlex.quote(kate_datuak) for kate_datuak in arg_matrize.arguments)
        return 0 if exekutatu_komando(aplik) == 0 else 1
    finally:
        if Prozesua.poll() is None:
            Prozesua.terminate()
            try: Prozesua.wait(timeout=5)
            except subprocess.TimeoutExpired: Prozesua.kill(); Prozesua.wait(timeout=5)
        준비선택기.close(); Prozesua.stdin.close(); Prozesua.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Exekutatu_2())
