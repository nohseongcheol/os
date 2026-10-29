#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. pinagare 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from diragatsa_Taelo import Taelo


def dirisa():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 leina(예: netefatsa_5fb2b747.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class faele 또는 class 디렉터리(패키지 leina 유지)')
    Thulaganyo_setlhopha = 인수해석기.parse_args()
    tshedimosetso = Thulaganyo_setlhopha.file.read_bytes()
    if Thulaganyo_setlhopha.class_name and Thulaganyo_setlhopha.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    leina = Thulaganyo_setlhopha.class_name + '.class' if Thulaganyo_setlhopha.class_name else Thulaganyo_setlhopha.file.name
    if len(tshedimosetso) > 16384 or not 1 <= len(leina.encode('utf-8')) <= 63 or '\n' in leina or '\r' in leina:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    setlhopha_Boleng_4b6d6445 = '.elf' if tshedimosetso[:4] == b'\x7fELF' else Thulaganyo_setlhopha.file.suffix
    if Thulaganyo_setlhopha.linux and setlhopha_Boleng_4b6d6445 != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if setlhopha_Boleng_4b6d6445 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(Thulaganyo_setlhopha.arguments) > 7 or any(len(dikwalwa_tshedimosetso.encode('utf-8')) > 255 or '\n' in dikwalwa_tshedimosetso or '\r' in dikwalwa_tshedimosetso for dikwalwa_tshedimosetso in Thulaganyo_setlhopha.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Diitlhophelwa = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if Thulaganyo_setlhopha.vnc: Diitlhophelwa += ['-vnc', Thulaganyo_setlhopha.vnc]
    Thulaganyo = subprocess.Popen(Taelo() + Diitlhophelwa, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    setlhophi = selectors.DefaultSelector(); setlhophi.register(Thulaganyo.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); kgaola_Baya_ka_Tekatekanyo = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > kgaola_Baya_ka_Tekatekanyo: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in setlhophi.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Thulaganyo.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def romela(Mola, 확인표시=b'jkoros-native> '):
        Thulaganyo.stdin.write(Mola.encode('utf-8') + b'\n'); Thulaganyo.stdin.flush()
        return 수신하기(확인표시)
    def diragatsa_Taelo(Mola):
        출력결과 = romela(Mola); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        faele_lenaane = []
        for 포함항목 in Thulaganyo_setlhopha.include:
            if 포함항목.is_dir():
                faele_lenaane += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                faele_lenaane.append((포함항목.name, 포함항목.read_bytes()))
        faele_lenaane = [(개수, bogorogelo_tshedimosetso) for 개수, bogorogelo_tshedimosetso in faele_lenaane if 개수 != leina] + [(leina, tshedimosetso)]
        for laisa_leina, laisa_tshedimosetso in faele_lenaane:
            if len(laisa_tshedimosetso) > 16384 or len(laisa_leina.encode('utf-8')) > 63 or '\n' in laisa_leina or '\r' in laisa_leina:
                raise ValueError('추가 파일의 leina/lekanya 제한 초과: ' + laisa_leina)
            romela('load ' + shlex.quote(laisa_leina), b'hex> ')
            for 순번 in range(0, len(laisa_tshedimosetso), 64): romela(laisa_tshedimosetso[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in romela('.'): raise RuntimeError('upload failed: ' + laisa_leina)
            갈무리자료 = romela('hex ' + shlex.quote(laisa_leina))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != laisa_tshedimosetso: raise RuntimeError('upload verification failed')
        if setlhopha_Boleng_4b6d6445 == '.java' and diragatsa_Taelo('javac ' + shlex.quote(leina)) != 0: return 1
        실행가능파일 = Thulaganyo_setlhopha.file.stem + '.elf'
        if setlhopha_Boleng_4b6d6445 == '.c' and diragatsa_Taelo('cc ' + shlex.quote(leina) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        Tiriso = 'java ' + shlex.quote(Thulaganyo_setlhopha.class_name or Thulaganyo_setlhopha.file.stem) if setlhopha_Boleng_4b6d6445 in ('.java', '.class') else ('python ' if setlhopha_Boleng_4b6d6445 == '.py' else 'run ') + shlex.quote(leina)
        if setlhopha_Boleng_4b6d6445 == '.jar': Tiriso = 'java -jar ' + shlex.quote(leina)
        if setlhopha_Boleng_4b6d6445 == '.c': Tiriso = 'run ' + shlex.quote(실행가능파일)
        if Thulaganyo_setlhopha.linux: Tiriso = 'run --linux ' + shlex.quote(leina)
        if Thulaganyo_setlhopha.arguments: Tiriso += ' ' + ' '.join(shlex.quote(dikwalwa_tshedimosetso) for dikwalwa_tshedimosetso in Thulaganyo_setlhopha.arguments)
        return 0 if diragatsa_Taelo(Tiriso) == 0 else 1
    finally:
        if Thulaganyo.poll() is None:
            Thulaganyo.terminate()
            try: Thulaganyo.wait(timeout=5)
            except subprocess.TimeoutExpired: Thulaganyo.kill(); Thulaganyo.wait(timeout=5)
        setlhophi.close(); Thulaganyo.stdin.close(); Thulaganyo.stdout.close()


if __name__ == '__main__':
    raise SystemExit(dirisa())
