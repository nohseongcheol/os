#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. umsingathi 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ukwenza_umyalelo import Umyalelo


def Phumeza():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Igama(예: qinisekisa.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class iFayili 또는 class 디렉터리(패키지 Igama 유지)')
    isiniki_myalelo_ULUHLU = 인수해석기.parse_args()
    iingcombolo = isiniki_myalelo_ULUHLU.file.read_bytes()
    if isiniki_myalelo_ULUHLU.class_name and isiniki_myalelo_ULUHLU.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Igama = isiniki_myalelo_ULUHLU.class_name + '.class' if isiniki_myalelo_ULUHLU.class_name else isiniki_myalelo_ULUHLU.file.name
    if len(iingcombolo) > 16384 or not 1 <= len(Igama.encode('utf-8')) <= 63 or '\n' in Igama or '\r' in Igama:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    udidi_ixabiso = '.elf' if iingcombolo[:4] == b'\x7fELF' else isiniki_myalelo_ULUHLU.file.suffix
    if isiniki_myalelo_ULUHLU.linux and udidi_ixabiso != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if udidi_ixabiso not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(isiniki_myalelo_ULUHLU.arguments) > 7 or any(len(uluhlu_lweekharektha_iingcombolo.encode('utf-8')) > 255 or '\n' in uluhlu_lweekharektha_iingcombolo or '\r' in uluhlu_lweekharektha_iingcombolo for uluhlu_lweekharektha_iingcombolo in isiniki_myalelo_ULUHLU.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    uKhetho = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if isiniki_myalelo_ULUHLU.vnc: uKhetho += ['-vnc', isiniki_myalelo_ULUHLU.vnc]
    Inkqubo = subprocess.Popen(Umyalelo() + uKhetho, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    umkhethi = selectors.DefaultSelector(); umkhethi.register(Inkqubo.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); phela_Ukulinganisa = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > phela_Ukulinganisa: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in umkhethi.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Inkqubo.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def thumela(umgca, 확인표시=b'jkoros-native> '):
        Inkqubo.stdin.write(umgca.encode('utf-8') + b'\n'); Inkqubo.stdin.flush()
        return 수신하기(확인표시)
    def ukwenza_umyalelo(umgca):
        출력결과 = thumela(umgca); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ifayile_uludwe = []
        for 포함항목 in isiniki_myalelo_ULUHLU.include:
            if 포함항목.is_dir():
                ifayile_uludwe += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ifayile_uludwe.append((포함항목.name, 포함항목.read_bytes()))
        ifayile_uludwe = [(개수, indawo_ekuyiwa_kuyo_iingcombolo) for 개수, indawo_ekuyiwa_kuyo_iingcombolo in ifayile_uludwe if 개수 != Igama] + [(Igama, iingcombolo)]
        for layisha_igama, layisha_iingcombolo in ifayile_uludwe:
            if len(layisha_iingcombolo) > 16384 or len(layisha_igama.encode('utf-8')) > 63 or '\n' in layisha_igama or '\r' in layisha_igama:
                raise ValueError('추가 파일의 Igama/Ubukhulu 제한 초과: ' + layisha_igama)
            thumela('load ' + shlex.quote(layisha_igama), b'hex> ')
            for 순번 in range(0, len(layisha_iingcombolo), 64): thumela(layisha_iingcombolo[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in thumela('.'): raise RuntimeError('upload failed: ' + layisha_igama)
            갈무리자료 = thumela('hex ' + shlex.quote(layisha_igama))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != layisha_iingcombolo: raise RuntimeError('upload verification failed')
        if udidi_ixabiso == '.java' and ukwenza_umyalelo('javac ' + shlex.quote(Igama)) != 0: return 1
        실행가능파일 = isiniki_myalelo_ULUHLU.file.stem + '.elf'
        if udidi_ixabiso == '.c' and ukwenza_umyalelo('cc ' + shlex.quote(Igama) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        inkqubo = 'java ' + shlex.quote(isiniki_myalelo_ULUHLU.class_name or isiniki_myalelo_ULUHLU.file.stem) if udidi_ixabiso in ('.java', '.class') else ('python ' if udidi_ixabiso == '.py' else 'run ') + shlex.quote(Igama)
        if udidi_ixabiso == '.jar': inkqubo = 'java -jar ' + shlex.quote(Igama)
        if udidi_ixabiso == '.c': inkqubo = 'run ' + shlex.quote(실행가능파일)
        if isiniki_myalelo_ULUHLU.linux: inkqubo = 'run --linux ' + shlex.quote(Igama)
        if isiniki_myalelo_ULUHLU.arguments: inkqubo += ' ' + ' '.join(shlex.quote(uluhlu_lweekharektha_iingcombolo) for uluhlu_lweekharektha_iingcombolo in isiniki_myalelo_ULUHLU.arguments)
        return 0 if ukwenza_umyalelo(inkqubo) == 0 else 1
    finally:
        if Inkqubo.poll() is None:
            Inkqubo.terminate()
            try: Inkqubo.wait(timeout=5)
            except subprocess.TimeoutExpired: Inkqubo.kill(); Inkqubo.wait(timeout=5)
        umkhethi.close(); Inkqubo.stdin.close(); Inkqubo.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Phumeza())
