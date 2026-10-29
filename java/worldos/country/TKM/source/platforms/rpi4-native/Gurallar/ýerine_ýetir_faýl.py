#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. esasy 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ýerine_ýetir_buýruk import buýruk


def Bitir():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ad(예: tassykla.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Faýl 또는 class 디렉터리(패키지 Ad 유지)')
    argument_ARRAY = 인수해석기.parse_args()
    maglumat = argument_ARRAY.file.read_bytes()
    if argument_ARRAY.class_name and argument_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Ad = argument_ARRAY.class_name + '.class' if argument_ARRAY.class_name else argument_ARRAY.file.name
    if len(maglumat) > 16384 or not 1 <= len(Ad.encode('utf-8')) <= 63 or '\n' in Ad or '\r' in Ad:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategoriýa_baha = '.elf' if maglumat[:4] == b'\x7fELF' else argument_ARRAY.file.suffix
    if argument_ARRAY.linux and kategoriýa_baha != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategoriýa_baha not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argument_ARRAY.arguments) > 7 or any(len(setir_maglumat.encode('utf-8')) > 255 or '\n' in setir_maglumat or '\r' in setir_maglumat for setir_maglumat in argument_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opsiýalar = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argument_ARRAY.vnc: Opsiýalar += ['-vnc', argument_ARRAY.vnc]
    Proses = subprocess.Popen(buýruk() + Opsiýalar, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    saýlaýjy = selectors.DefaultSelector(); saýlaýjy.register(Proses.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); tamamla_Süýşüriş = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > tamamla_Süýşüriş: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in saýlaýjy.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def iber(setir, 확인표시=b'jkoros-native> '):
        Proses.stdin.write(setir.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return 수신하기(확인표시)
    def ýerine_ýetir_buýruk(setir):
        출력결과 = iber(setir); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        faýl_Sanaw = []
        for 포함항목 in argument_ARRAY.include:
            if 포함항목.is_dir():
                faýl_Sanaw += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                faýl_Sanaw.append((포함항목.name, 포함항목.read_bytes()))
        faýl_Sanaw = [(개수, barylmaly_ýer_maglumat) for 개수, barylmaly_ýer_maglumat in faýl_Sanaw if 개수 != Ad] + [(Ad, maglumat)]
        for ýükle_at, ýükle_maglumat in faýl_Sanaw:
            if len(ýükle_maglumat) > 16384 or len(ýükle_at.encode('utf-8')) > 63 or '\n' in ýükle_at or '\r' in ýükle_at:
                raise ValueError('추가 파일의 Ad/Ululyk 제한 초과: ' + ýükle_at)
            iber('load ' + shlex.quote(ýükle_at), b'hex> ')
            for 순번 in range(0, len(ýükle_maglumat), 64): iber(ýükle_maglumat[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in iber('.'): raise RuntimeError('upload failed: ' + ýükle_at)
            갈무리자료 = iber('hex ' + shlex.quote(ýükle_at))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ýükle_maglumat: raise RuntimeError('upload verification failed')
        if kategoriýa_baha == '.java' and ýerine_ýetir_buýruk('javac ' + shlex.quote(Ad)) != 0: return 1
        실행가능파일 = argument_ARRAY.file.stem + '.elf'
        if kategoriýa_baha == '.c' and ýerine_ýetir_buýruk('cc ' + shlex.quote(Ad) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programma = 'java ' + shlex.quote(argument_ARRAY.class_name or argument_ARRAY.file.stem) if kategoriýa_baha in ('.java', '.class') else ('python ' if kategoriýa_baha == '.py' else 'run ') + shlex.quote(Ad)
        if kategoriýa_baha == '.jar': programma = 'java -jar ' + shlex.quote(Ad)
        if kategoriýa_baha == '.c': programma = 'run ' + shlex.quote(실행가능파일)
        if argument_ARRAY.linux: programma = 'run --linux ' + shlex.quote(Ad)
        if argument_ARRAY.arguments: programma += ' ' + ' '.join(shlex.quote(setir_maglumat) for setir_maglumat in argument_ARRAY.arguments)
        return 0 if ýerine_ýetir_buýruk(programma) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        saýlaýjy.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Bitir())
