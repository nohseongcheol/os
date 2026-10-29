#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. go_nea_ditirelo 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from phethagatša_taelo import Taelo


def Diriša():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Leina(예: kgonthiša_5fb2b747.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Faele 또는 class 디렉터리(패키지 Leina 유지)')
    akumente_arei = 인수해석기.parse_args()
    data = akumente_arei.file.read_bytes()
    if akumente_arei.class_name and akumente_arei.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Leina = akumente_arei.class_name + '.class' if akumente_arei.class_name else akumente_arei.file.name
    if len(data) > 16384 or not 1 <= len(Leina.encode('utf-8')) <= 63 or '\n' in Leina or '\r' in Leina:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    legoro_boleng = '.elf' if data[:4] == b'\x7fELF' else akumente_arei.file.suffix
    if akumente_arei.linux and legoro_boleng != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if legoro_boleng not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(akumente_arei.arguments) > 7 or any(len(molokoloko_data.encode('utf-8')) > 255 or '\n' in molokoloko_data or '\r' in molokoloko_data for molokoloko_data in akumente_arei.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Dikgetho = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if akumente_arei.vnc: Dikgetho += ['-vnc', akumente_arei.vnc]
    tiragalo_a7054519 = subprocess.Popen(Taelo() + Dikgetho, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    sekgethi = selectors.DefaultSelector(); sekgethi.register(tiragalo_a7054519.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); fetša_E_Šetšego = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > fetša_E_Šetšego: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in sekgethi.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if tiragalo_a7054519.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def Romela(mothaladi, 확인표시=b'jkoros-native> '):
        tiragalo_a7054519.stdin.write(mothaladi.encode('utf-8') + b'\n'); tiragalo_a7054519.stdin.flush()
        return 수신하기(확인표시)
    def phethagatša_taelo(mothaladi):
        출력결과 = Romela(mothaladi); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        faele_Lenaneo = []
        for 포함항목 in akumente_arei.include:
            if 포함항목.is_dir():
                faele_Lenaneo += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                faele_Lenaneo.append((포함항목.name, 포함항목.read_bytes()))
        faele_Lenaneo = [(개수, boyo_data) for 개수, boyo_data in faele_Lenaneo if 개수 != Leina] + [(Leina, data)]
        for apolouto_leina, apolouto_data in faele_Lenaneo:
            if len(apolouto_data) > 16384 or len(apolouto_leina.encode('utf-8')) > 63 or '\n' in apolouto_leina or '\r' in apolouto_leina:
                raise ValueError('추가 파일의 Leina/Bogolo 제한 초과: ' + apolouto_leina)
            Romela('load ' + shlex.quote(apolouto_leina), b'hex> ')
            for 순번 in range(0, len(apolouto_data), 64): Romela(apolouto_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in Romela('.'): raise RuntimeError('upload failed: ' + apolouto_leina)
            갈무리자료 = Romela('hex ' + shlex.quote(apolouto_leina))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != apolouto_data: raise RuntimeError('upload verification failed')
        if legoro_boleng == '.java' and phethagatša_taelo('javac ' + shlex.quote(Leina)) != 0: return 1
        실행가능파일 = akumente_arei.file.stem + '.elf'
        if legoro_boleng == '.c' and phethagatša_taelo('cc ' + shlex.quote(Leina) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        tirišo = 'java ' + shlex.quote(akumente_arei.class_name or akumente_arei.file.stem) if legoro_boleng in ('.java', '.class') else ('python ' if legoro_boleng == '.py' else 'run ') + shlex.quote(Leina)
        if legoro_boleng == '.jar': tirišo = 'java -jar ' + shlex.quote(Leina)
        if legoro_boleng == '.c': tirišo = 'run ' + shlex.quote(실행가능파일)
        if akumente_arei.linux: tirišo = 'run --linux ' + shlex.quote(Leina)
        if akumente_arei.arguments: tirišo += ' ' + ' '.join(shlex.quote(molokoloko_data) for molokoloko_data in akumente_arei.arguments)
        return 0 if phethagatša_taelo(tirišo) == 0 else 1
    finally:
        if tiragalo_a7054519.poll() is None:
            tiragalo_a7054519.terminate()
            try: tiragalo_a7054519.wait(timeout=5)
            except subprocess.TimeoutExpired: tiragalo_a7054519.kill(); tiragalo_a7054519.wait(timeout=5)
        sekgethi.close(); tiragalo_a7054519.stdin.close(); tiragalo_a7054519.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Diriša())
