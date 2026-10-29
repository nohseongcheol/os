#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. njaatigi 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import ginol


def huutoraade():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 innde(예: 검증.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class fiilde 또는 class 디렉터리(패키지 innde 유지)')
    인수배열 = 인수해석기.parse_args()
    keɓe = 인수배열.file.read_bytes()
    if 인수배열.class_name and 인수배열.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    innde = 인수배열.class_name + '.class' if 인수배열.class_name else 인수배열.file.name
    if len(keɓe) > 16384 or not 1 <= len(innde.encode('utf-8')) <= 63 or '\n' in innde or '\r' in innde:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategorii_njaru = '.elf' if keɓe[:4] == b'\x7fELF' else 인수배열.file.suffix
    if 인수배열.linux and kategorii_njaru != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategorii_njaru not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(인수배열.arguments) > 7 or any(len(ɓoggol_keɓe.encode('utf-8')) > 255 or '\n' in ɓoggol_keɓe or '\r' in ɓoggol_keɓe for ɓoggol_keɓe in 인수배열.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Cuɓe = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if 인수배열.vnc: Cuɓe += ['-vnc', 인수배열.vnc]
    Yuɓɓo_golle = subprocess.Popen(ginol() + Cuɓe, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Yuɓɓo_golle.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Yuɓɓo_golle.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def neldude(diidol, 확인표시=b'jkoros-native> '):
        Yuɓɓo_golle.stdin.write(diidol.encode('utf-8') + b'\n'); Yuɓɓo_golle.stdin.flush()
        return 수신하기(확인표시)
    def 실행(diidol):
        출력결과 = neldude(diidol); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fiilde_Doggol = []
        for 포함항목 in 인수배열.include:
            if 포함항목.is_dir():
                fiilde_Doggol += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                fiilde_Doggol.append((포함항목.name, 포함항목.read_bytes()))
        fiilde_Doggol = [(개수, tiindaare_keɓe) for 개수, tiindaare_keɓe in fiilde_Doggol if 개수 != innde] + [(innde, keɓe)]
        for fampaade_innde, fampaade_keɓe in fiilde_Doggol:
            if len(fampaade_keɓe) > 16384 or len(fampaade_innde.encode('utf-8')) > 63 or '\n' in fampaade_innde or '\r' in fampaade_innde:
                raise ValueError('추가 파일의 innde/waylude_etannde 제한 초과: ' + fampaade_innde)
            neldude('load ' + shlex.quote(fampaade_innde), b'hex> ')
            for 순번 in range(0, len(fampaade_keɓe), 64): neldude(fampaade_keɓe[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in neldude('.'): raise RuntimeError('upload failed: ' + fampaade_innde)
            갈무리자료 = neldude('hex ' + shlex.quote(fampaade_innde))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != fampaade_keɓe: raise RuntimeError('upload verification failed')
        if kategorii_njaru == '.java' and 실행('javac ' + shlex.quote(innde)) != 0: return 1
        실행가능파일 = 인수배열.file.stem + '.elf'
        if kategorii_njaru == '.c' and 실행('cc ' + shlex.quote(innde) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        tafirde = 'java ' + shlex.quote(인수배열.class_name or 인수배열.file.stem) if kategorii_njaru in ('.java', '.class') else ('python ' if kategorii_njaru == '.py' else 'run ') + shlex.quote(innde)
        if kategorii_njaru == '.jar': tafirde = 'java -jar ' + shlex.quote(innde)
        if kategorii_njaru == '.c': tafirde = 'run ' + shlex.quote(실행가능파일)
        if 인수배열.linux: tafirde = 'run --linux ' + shlex.quote(innde)
        if 인수배열.arguments: tafirde += ' ' + ' '.join(shlex.quote(ɓoggol_keɓe) for ɓoggol_keɓe in 인수배열.arguments)
        return 0 if 실행(tafirde) == 0 else 1
    finally:
        if Yuɓɓo_golle.poll() is None:
            Yuɓɓo_golle.terminate()
            try: Yuɓɓo_golle.wait(timeout=5)
            except subprocess.TimeoutExpired: Yuɓɓo_golle.kill(); Yuɓɓo_golle.wait(timeout=5)
        준비선택기.close(); Yuɓɓo_golle.stdin.close(); Yuɓɓo_golle.stdout.close()


if __name__ == '__main__':
    raise SystemExit(huutoraade())
