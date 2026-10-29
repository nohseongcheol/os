#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. tuttarvik 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import piqujijjut


def 시작():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 atiq(예: naammannirarli.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ini 또는 class 디렉터리(패키지 atiq 유지)')
    aturniqarnirainiq_array = 인수해석기.parse_args()
    titiqqat = aturniqarnirainiq_array.file.read_bytes()
    if aturniqarnirainiq_array.class_name and aturniqarnirainiq_array.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    atiq = aturniqarnirainiq_array.class_name + '.class' if aturniqarnirainiq_array.class_name else aturniqarnirainiq_array.file.name
    if len(titiqqat) > 16384 or not 1 <= len(atiq.encode('utf-8')) <= 63 or '\n' in atiq or '\r' in atiq:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Ataqatigiivvik_atuutilik = '.elf' if titiqqat[:4] == b'\x7fELF' else aturniqarnirainiq_array.file.suffix
    if aturniqarnirainiq_array.linux and Ataqatigiivvik_atuutilik != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Ataqatigiivvik_atuutilik not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(aturniqarnirainiq_array.arguments) > 7 or any(len(qimiaq_titiqqat.encode('utf-8')) > 255 or '\n' in qimiaq_titiqqat or '\r' in qimiaq_titiqqat for qimiaq_titiqqat in aturniqarnirainiq_array.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Qanuqtuurutit = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if aturniqarnirainiq_array.vnc: Qanuqtuurutit += ['-vnc', aturniqarnirainiq_array.vnc]
    Pivallianiq = subprocess.Popen(piqujijjut() + Qanuqtuurutit, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Pivallianiq.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Pivallianiq.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def nassiutili(titikutaak, 확인표시=b'jkoros-native> '):
        Pivallianiq.stdin.write(titikutaak.encode('utf-8') + b'\n'); Pivallianiq.stdin.flush()
        return 수신하기(확인표시)
    def 실행(titikutaak):
        출력결과 = nassiutili(titikutaak); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ini_Titiqpalliagaq = []
        for 포함항목 in aturniqarnirainiq_array.include:
            if 포함항목.is_dir():
                ini_Titiqpalliagaq += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ini_Titiqpalliagaq.append((포함항목.name, 포함항목.read_bytes()))
        ini_Titiqpalliagaq = [(개수, namunngarvik_titiqqat) for 개수, namunngarvik_titiqqat in ini_Titiqpalliagaq if 개수 != atiq] + [(atiq, titiqqat)]
        for inimit_aullaaqtiriniq_atiq, inimit_aullaaqtiriniq_titiqqat in ini_Titiqpalliagaq:
            if len(inimit_aullaaqtiriniq_titiqqat) > 16384 or len(inimit_aullaaqtiriniq_atiq.encode('utf-8')) > 63 or '\n' in inimit_aullaaqtiriniq_atiq or '\r' in inimit_aullaaqtiriniq_atiq:
                raise ValueError('추가 파일의 atiq/anininga 제한 초과: ' + inimit_aullaaqtiriniq_atiq)
            nassiutili('load ' + shlex.quote(inimit_aullaaqtiriniq_atiq), b'hex> ')
            for 순번 in range(0, len(inimit_aullaaqtiriniq_titiqqat), 64): nassiutili(inimit_aullaaqtiriniq_titiqqat[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in nassiutili('.'): raise RuntimeError('upload failed: ' + inimit_aullaaqtiriniq_atiq)
            갈무리자료 = nassiutili('hex ' + shlex.quote(inimit_aullaaqtiriniq_atiq))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != inimit_aullaaqtiriniq_titiqqat: raise RuntimeError('upload verification failed')
        if Ataqatigiivvik_atuutilik == '.java' and 실행('javac ' + shlex.quote(atiq)) != 0: return 1
        실행가능파일 = aturniqarnirainiq_array.file.stem + '.elf'
        if Ataqatigiivvik_atuutilik == '.c' and 실행('cc ' + shlex.quote(atiq) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        pilirijjut = 'java ' + shlex.quote(aturniqarnirainiq_array.class_name or aturniqarnirainiq_array.file.stem) if Ataqatigiivvik_atuutilik in ('.java', '.class') else ('python ' if Ataqatigiivvik_atuutilik == '.py' else 'run ') + shlex.quote(atiq)
        if Ataqatigiivvik_atuutilik == '.jar': pilirijjut = 'java -jar ' + shlex.quote(atiq)
        if Ataqatigiivvik_atuutilik == '.c': pilirijjut = 'run ' + shlex.quote(실행가능파일)
        if aturniqarnirainiq_array.linux: pilirijjut = 'run --linux ' + shlex.quote(atiq)
        if aturniqarnirainiq_array.arguments: pilirijjut += ' ' + ' '.join(shlex.quote(qimiaq_titiqqat) for qimiaq_titiqqat in aturniqarnirainiq_array.arguments)
        return 0 if 실행(pilirijjut) == 0 else 1
    finally:
        if Pivallianiq.poll() is None:
            Pivallianiq.terminate()
            try: Pivallianiq.wait(timeout=5)
            except subprocess.TimeoutExpired: Pivallianiq.kill(); Pivallianiq.wait(timeout=5)
        준비선택기.close(); Pivallianiq.stdin.close(); Pivallianiq.stdout.close()


if __name__ == '__main__':
    raise SystemExit(시작())
