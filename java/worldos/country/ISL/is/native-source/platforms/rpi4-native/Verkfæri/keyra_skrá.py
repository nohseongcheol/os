#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. hýsa 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from keyra_skipun import Skipun


def Keyra_2():
    þáttari = argparse.ArgumentParser(description=__doc__)
    þáttari.add_argument('file', type=Path)
    þáttari.add_argument('arguments', nargs='*')
    þáttari.add_argument('--class-name', help='패키지가 있는 .class의 전체 Heiti(예: staðfesta.꾸러미시험)')
    þáttari.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    þáttari.add_argument('--vnc', help='예: 127.0.0.1:2')
    þáttari.add_argument('--include', action='append', type=Path, default=[], help='추가 class Skrá 또는 class 디렉터리(패키지 Heiti 유지)')
    frumbreyta_ARRAY = þáttari.parse_args()
    gögn = frumbreyta_ARRAY.file.read_bytes()
    if frumbreyta_ARRAY.class_name and frumbreyta_ARRAY.file.suffix != '.class': þáttari.error('--class-name은 .class 입력에서 사용합니다.')
    Heiti = frumbreyta_ARRAY.class_name + '.class' if frumbreyta_ARRAY.class_name else frumbreyta_ARRAY.file.name
    if len(gögn) > 16384 or not 1 <= len(Heiti.encode('utf-8')) <= 63 or '\n' in Heiti or '\r' in Heiti:
        þáttari.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    tegund_VALUE = '.elf' if gögn[:4] == b'\x7fELF' else frumbreyta_ARRAY.file.suffix
    if frumbreyta_ARRAY.linux and tegund_VALUE != '.elf': þáttari.error('--linux는 ELF 바이너리에만 사용합니다.')
    if tegund_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        þáttari.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(frumbreyta_ARRAY.arguments) > 7 or any(len(strengur_gögn.encode('utf-8')) > 255 or '\n' in strengur_gögn or '\r' in strengur_gögn for strengur_gögn in frumbreyta_ARRAY.arguments):
        þáttari.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    valkostir = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if frumbreyta_ARRAY.vnc: valkostir += ['-vnc', frumbreyta_ARRAY.vnc]
    Ferli = subprocess.Popen(Skipun() + valkostir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    val = selectors.DefaultSelector(); val.register(Ferli.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        úttak_54cd5e1d = bytearray(); ljúka_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in úttak_54cd5e1d:
            if time.monotonic() > ljúka_OFFSET: raise RuntimeError('UART timeout: ' + úttak_54cd5e1d.decode('utf-8', 'replace'))
            for 누름값, _ in val.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: úttak_54cd5e1d.extend(조각)
            if b'PANIC:' in úttak_54cd5e1d or b'FAIL ' in úttak_54cd5e1d: raise RuntimeError(úttak_54cd5e1d.decode('utf-8', 'replace'))
            if Ferli.poll() is not None: raise RuntimeError('QEMU exited: ' + úttak_54cd5e1d.decode('utf-8', 'replace'))
        return bytes(úttak_54cd5e1d)
    def senda(Lína, 확인표시=b'jkoros-native> '):
        Ferli.stdin.write(Lína.encode('utf-8') + b'\n'); Ferli.stdin.flush()
        return 수신하기(확인표시)
    def keyra_skipun(Lína):
        úttak_54cd5e1d = senda(Lína); sys.stdout.buffer.write(úttak_54cd5e1d); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', úttak_54cd5e1d)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        skrá_Listi = []
        for 포함항목 in frumbreyta_ARRAY.include:
            if 포함항목.is_dir():
                skrá_Listi += [(str(gögn_staða.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', gögn_staða.read_bytes()) for gögn_staða in sorted(포함항목.rglob('*.class'))]
            else:
                skrá_Listi.append((포함항목.name, 포함항목.read_bytes()))
        skrá_Listi = [(vara_COUNT, endastaður_gögn) for vara_COUNT, endastaður_gögn in skrá_Listi if vara_COUNT != Heiti] + [(Heiti, gögn)]
        for hlaða_upp_heiti, hlaða_upp_gögn in skrá_Listi:
            if len(hlaða_upp_gögn) > 16384 or len(hlaða_upp_heiti.encode('utf-8')) > 63 or '\n' in hlaða_upp_heiti or '\r' in hlaða_upp_heiti:
                raise ValueError('추가 파일의 Heiti/Stærð 제한 초과: ' + hlaða_upp_heiti)
            senda('load ' + shlex.quote(hlaða_upp_heiti), b'hex> ')
            for 순번 in range(0, len(hlaða_upp_gögn), 64): senda(hlaða_upp_gögn[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in senda('.'): raise RuntimeError('upload failed: ' + hlaða_upp_heiti)
            갈무리자료 = senda('hex ' + shlex.quote(hlaða_upp_heiti))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != hlaða_upp_gögn: raise RuntimeError('upload verification failed')
        if tegund_VALUE == '.java' and keyra_skipun('javac ' + shlex.quote(Heiti)) != 0: return 1
        실행가능파일 = frumbreyta_ARRAY.file.stem + '.elf'
        if tegund_VALUE == '.c' and keyra_skipun('cc ' + shlex.quote(Heiti) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        forrit = 'java ' + shlex.quote(frumbreyta_ARRAY.class_name or frumbreyta_ARRAY.file.stem) if tegund_VALUE in ('.java', '.class') else ('python ' if tegund_VALUE == '.py' else 'run ') + shlex.quote(Heiti)
        if tegund_VALUE == '.jar': forrit = 'java -jar ' + shlex.quote(Heiti)
        if tegund_VALUE == '.c': forrit = 'run ' + shlex.quote(실행가능파일)
        if frumbreyta_ARRAY.linux: forrit = 'run --linux ' + shlex.quote(Heiti)
        if frumbreyta_ARRAY.arguments: forrit += ' ' + ' '.join(shlex.quote(strengur_gögn) for strengur_gögn in frumbreyta_ARRAY.arguments)
        return 0 if keyra_skipun(forrit) == 0 else 1
    finally:
        if Ferli.poll() is None:
            Ferli.terminate()
            try: Ferli.wait(timeout=5)
            except subprocess.TimeoutExpired: Ferli.kill(); Ferli.wait(timeout=5)
        val.close(); Ferli.stdin.close(); Ferli.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Keyra_2())
