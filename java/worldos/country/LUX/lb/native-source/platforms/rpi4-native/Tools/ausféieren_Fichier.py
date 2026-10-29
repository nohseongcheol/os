#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. Host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ausféieren_Befeel import Befeel


def Laf():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Numm(예: validéieren.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fichier 또는 class 디렉터리(패키지 Numm 유지)')
    Argument_ARRAY = 인수해석기.parse_args()
    Daten = Argument_ARRAY.file.read_bytes()
    if Argument_ARRAY.class_name and Argument_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Numm = Argument_ARRAY.class_name + '.class' if Argument_ARRAY.class_name else Argument_ARRAY.file.name
    if len(Daten) > 16384 or not 1 <= len(Numm.encode('utf-8')) <= 63 or '\n' in Numm or '\r' in Numm:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Kategorie_VALUE = '.elf' if Daten[:4] == b'\x7fELF' else Argument_ARRAY.file.suffix
    if Argument_ARRAY.linux and Kategorie_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Kategorie_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(Argument_ARRAY.arguments) > 7 or any(len(Zeechefolleg_Daten.encode('utf-8')) > 255 or '\n' in Zeechefolleg_Daten or '\r' in Zeechefolleg_Daten for Zeechefolleg_Daten in Argument_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Optiounen = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if Argument_ARRAY.vnc: Optiounen += ['-vnc', Argument_ARRAY.vnc]
    Prozess = subprocess.Popen(Befeel() + Optiounen, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selekteur = selectors.DefaultSelector(); Selekteur.register(Prozess.stdout, selectors.EVENT_READ)
    def 수신하기(Markéierung, 시간제한=45):
        출력결과 = bytearray(); bëennegen_OFFSET = time.monotonic() + 시간제한
        while Markéierung not in 출력결과:
            if time.monotonic() > bëennegen_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in Selekteur.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Prozess.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def mailen(Zeil, Markéierung=b'jkoros-native> '):
        Prozess.stdin.write(Zeil.encode('utf-8') + b'\n'); Prozess.stdin.flush()
        return 수신하기(Markéierung)
    def ausféieren_Befeel(Zeil):
        출력결과 = mailen(Zeil); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        Fichier_Lëscht = []
        for 포함항목 in Argument_ARRAY.include:
            if 포함항목.is_dir():
                Fichier_Lëscht += [(str(Daten_positionéieren.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', Daten_positionéieren.read_bytes()) for Daten_positionéieren in sorted(포함항목.rglob('*.class'))]
            else:
                Fichier_Lëscht.append((포함항목.name, 포함항목.read_bytes()))
        Fichier_Lëscht = [(Element_COUNT, Zil_Daten) for Element_COUNT, Zil_Daten in Fichier_Lëscht if Element_COUNT != Numm] + [(Numm, Daten)]
        for eroplueden_Numm, eroplueden_Daten in Fichier_Lëscht:
            if len(eroplueden_Daten) > 16384 or len(eroplueden_Numm.encode('utf-8')) > 63 or '\n' in eroplueden_Numm or '\r' in eroplueden_Numm:
                raise ValueError('추가 파일의 Numm/d_Gréisst_veränneren 제한 초과: ' + eroplueden_Numm)
            mailen('load ' + shlex.quote(eroplueden_Numm), b'hex> ')
            for 순번 in range(0, len(eroplueden_Daten), 64): mailen(eroplueden_Daten[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in mailen('.'): raise RuntimeError('upload failed: ' + eroplueden_Numm)
            갈무리자료 = mailen('hex ' + shlex.quote(eroplueden_Numm))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != eroplueden_Daten: raise RuntimeError('upload verification failed')
        if Kategorie_VALUE == '.java' and ausféieren_Befeel('javac ' + shlex.quote(Numm)) != 0: return 1
        실행가능파일 = Argument_ARRAY.file.stem + '.elf'
        if Kategorie_VALUE == '.c' and ausféieren_Befeel('cc ' + shlex.quote(Numm) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        App = 'java ' + shlex.quote(Argument_ARRAY.class_name or Argument_ARRAY.file.stem) if Kategorie_VALUE in ('.java', '.class') else ('python ' if Kategorie_VALUE == '.py' else 'run ') + shlex.quote(Numm)
        if Kategorie_VALUE == '.jar': App = 'java -jar ' + shlex.quote(Numm)
        if Kategorie_VALUE == '.c': App = 'run ' + shlex.quote(실행가능파일)
        if Argument_ARRAY.linux: App = 'run --linux ' + shlex.quote(Numm)
        if Argument_ARRAY.arguments: App += ' ' + ' '.join(shlex.quote(Zeechefolleg_Daten) for Zeechefolleg_Daten in Argument_ARRAY.arguments)
        return 0 if ausféieren_Befeel(App) == 0 else 1
    finally:
        if Prozess.poll() is None:
            Prozess.terminate()
            try: Prozess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prozess.kill(); Prozess.wait(timeout=5)
        Selekteur.close(); Prozess.stdin.close(); Prozess.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Laf())
