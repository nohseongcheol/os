#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. organizuoti 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Vykdyti_komanda import Komanda


def Paleisti():
    analizatorius = argparse.ArgumentParser(description=__doc__)
    analizatorius.add_argument('file', type=Path)
    analizatorius.add_argument('arguments', nargs='*')
    analizatorius.add_argument('--class-name', help='패키지가 있는 .class의 전체 Pavadinimas_2(예: tikrinti.꾸러미시험)')
    analizatorius.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI naudoti_VALUE')
    analizatorius.add_argument('--vnc', help='예: 127.0.0.1:2')
    analizatorius.add_argument('--include', action='append', type=Path, default=[], help='sujungti_įrašas class Failas 또는 class 디렉터리(패키지 Pavadinimas_2 유지)')
    argumentas_ARRAY = analizatorius.parse_args()
    duomenys = argumentas_ARRAY.file.read_bytes()
    if argumentas_ARRAY.class_name and argumentas_ARRAY.file.suffix != '.class': analizatorius.error('--class-name은 .class 입력에서 사용합니다.')
    Pavadinimas_2 = argumentas_ARRAY.class_name + '.class' if argumentas_ARRAY.class_name else argumentas_ARRAY.file.name
    if len(duomenys) > 16384 or not 1 <= len(Pavadinimas_2.encode('utf-8')) <= 63 or '\n' in Pavadinimas_2 or '\r' in Pavadinimas_2:
        analizatorius.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    sritis_VALUE = '.elf' if duomenys[:4] == b'\x7fELF' else argumentas_ARRAY.file.suffix
    if argumentas_ARRAY.linux and sritis_VALUE != '.elf': analizatorius.error('--linux는 ELF 바이너리에만 사용합니다.')
    if sritis_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        analizatorius.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumentas_ARRAY.arguments) > 7 or any(len(eilutė_duomenys.encode('utf-8')) > 255 or '\n' in eilutė_duomenys or '\r' in eilutė_duomenys for eilutė_duomenys in argumentas_ARRAY.arguments):
        analizatorius.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Parinktys = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumentas_ARRAY.vnc: Parinktys += ['-vnc', argumentas_ARRAY.vnc]
    Procesas = subprocess.Popen(Komanda() + Parinktys, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    išrinkiklis = selectors.DefaultSelector(); išrinkiklis.register(Procesas.stdout, selectors.EVENT_READ)
    def gauti_žinutė(žymeklis, 시간제한=45):
        išeiga = bytearray(); baigti_pokalbį_OFFSET = time.monotonic() + 시간제한
        while žymeklis not in išeiga:
            if time.monotonic() > baigti_pokalbį_OFFSET: raise RuntimeError('UART timeout: ' + išeiga.decode('utf-8', 'replace'))
            for 누름값, _ in išrinkiklis.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: išeiga.extend(조각)
            if b'PANIC:' in išeiga or b'FAIL ' in išeiga: raise RuntimeError(išeiga.decode('utf-8', 'replace'))
            if Procesas.poll() is not None: raise RuntimeError('QEMU exited: ' + išeiga.decode('utf-8', 'replace'))
        return bytes(išeiga)
    def siųsti(Eilutė, žymeklis=b'jkoros-native> '):
        Procesas.stdin.write(Eilutė.encode('utf-8') + b'\n'); Procesas.stdin.flush()
        return gauti_žinutė(žymeklis)
    def Vykdyti_komanda(Eilutė):
        išeiga = siųsti(Eilutė); sys.stdout.buffer.write(išeiga); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', išeiga)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        gauti_žinutė(b'jkoros-native> ')
        Failas_Sąrašas = []
        for apimti in argumentas_ARRAY.include:
            if apimti.is_dir():
                Failas_Sąrašas += [(str(duomenys_padėtis.relative_to(apimti).with_suffix('')).replace('/', '.') + '.class', duomenys_padėtis.read_bytes()) for duomenys_padėtis in sorted(apimti.rglob('*.class'))]
            else:
                Failas_Sąrašas.append((apimti.name, apimti.read_bytes()))
        Failas_Sąrašas = [(prekė_COUNT, vieta_duomenys) for prekė_COUNT, vieta_duomenys in Failas_Sąrašas if prekė_COUNT != Pavadinimas_2] + [(Pavadinimas_2, duomenys)]
        for Upload_pavadinimas, Upload_duomenys in Failas_Sąrašas:
            if len(Upload_duomenys) > 16384 or len(Upload_pavadinimas.encode('utf-8')) > 63 or '\n' in Upload_pavadinimas or '\r' in Upload_pavadinimas:
                raise ValueError('sujungti_įrašas 파일의 Pavadinimas_2/Dydis 제한 초과: ' + Upload_pavadinimas)
            siųsti('load ' + shlex.quote(Upload_pavadinimas), b'hex> ')
            for 순번 in range(0, len(Upload_duomenys), 64): siųsti(Upload_duomenys[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in siųsti('.'): raise RuntimeError('upload failed: ' + Upload_pavadinimas)
            갈무리자료 = siųsti('hex ' + shlex.quote(Upload_pavadinimas))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_duomenys: raise RuntimeError('upload verification failed')
        if sritis_VALUE == '.java' and Vykdyti_komanda('javac ' + shlex.quote(Pavadinimas_2)) != 0: return 1
        실행가능파일 = argumentas_ARRAY.file.stem + '.elf'
        if sritis_VALUE == '.c' and Vykdyti_komanda('cc ' + shlex.quote(Pavadinimas_2) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programa = 'java ' + shlex.quote(argumentas_ARRAY.class_name or argumentas_ARRAY.file.stem) if sritis_VALUE in ('.java', '.class') else ('python ' if sritis_VALUE == '.py' else 'run ') + shlex.quote(Pavadinimas_2)
        if sritis_VALUE == '.jar': programa = 'java -jar ' + shlex.quote(Pavadinimas_2)
        if sritis_VALUE == '.c': programa = 'run ' + shlex.quote(실행가능파일)
        if argumentas_ARRAY.linux: programa = 'run --linux ' + shlex.quote(Pavadinimas_2)
        if argumentas_ARRAY.arguments: programa += ' ' + ' '.join(shlex.quote(eilutė_duomenys) for eilutė_duomenys in argumentas_ARRAY.arguments)
        return 0 if Vykdyti_komanda(programa) == 0 else 1
    finally:
        if Procesas.poll() is None:
            Procesas.terminate()
            try: Procesas.wait(timeout=5)
            except subprocess.TimeoutExpired: Procesas.kill(); Procesas.wait(timeout=5)
        išrinkiklis.close(); Procesas.stdin.close(); Procesas.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Paleisti())
