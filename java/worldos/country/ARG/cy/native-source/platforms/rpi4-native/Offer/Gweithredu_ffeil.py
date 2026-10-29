#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. lletya 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Gweithredu_gorchymyn import Gorchymyn


def Gweithredu_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Enw(예: dilysu_5fb2b747.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Ffeil 또는 class 디렉터리(패키지 Enw 유지)')
    arg_ARAE = 인수해석기.parse_args()
    data = arg_ARAE.file.read_bytes()
    if arg_ARAE.class_name and arg_ARAE.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Enw = arg_ARAE.class_name + '.class' if arg_ARAE.class_name else arg_ARAE.file.name
    if len(data) > 16384 or not 1 <= len(Enw.encode('utf-8')) <= 63 or '\n' in Enw or '\r' in Enw:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ardal_VALUE = '.elf' if data[:4] == b'\x7fELF' else arg_ARAE.file.suffix
    if arg_ARAE.linux and ardal_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ardal_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arg_ARAE.arguments) > 7 or any(len(testun_data.encode('utf-8')) > 255 or '\n' in testun_data or '\r' in testun_data for testun_data in arg_ARAE.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Dewisiadau = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arg_ARAE.vnc: Dewisiadau += ['-vnc', arg_ARAE.vnc]
    Proses = subprocess.Popen(Gorchymyn() + Dewisiadau, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    dewisydd = selectors.DefaultSelector(); dewisydd.register(Proses.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); gorffen_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > gorffen_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in dewisydd.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def anfon(llinell, 확인표시=b'jkoros-native> '):
        Proses.stdin.write(llinell.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return 수신하기(확인표시)
    def Gweithredu_gorchymyn(llinell):
        출력결과 = anfon(llinell); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ffeil_Rhestr = []
        for 포함항목 in arg_ARAE.include:
            if 포함항목.is_dir():
                ffeil_Rhestr += [(str(data_safle.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_safle.read_bytes()) for data_safle in sorted(포함항목.rglob('*.class'))]
            else:
                ffeil_Rhestr.append((포함항목.name, 포함항목.read_bytes()))
        ffeil_Rhestr = [(eitem_COUNT, cyrchfan_data) for eitem_COUNT, cyrchfan_data in ffeil_Rhestr if eitem_COUNT != Enw] + [(Enw, data)]
        for Upload_enw, Upload_data in ffeil_Rhestr:
            if len(Upload_data) > 16384 or len(Upload_enw.encode('utf-8')) > 63 or '\n' in Upload_enw or '\r' in Upload_enw:
                raise ValueError('추가 파일의 Enw/Maint 제한 초과: ' + Upload_enw)
            anfon('load ' + shlex.quote(Upload_enw), b'hex> ')
            for 순번 in range(0, len(Upload_data), 64): anfon(Upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in anfon('.'): raise RuntimeError('upload failed: ' + Upload_enw)
            갈무리자료 = anfon('hex ' + shlex.quote(Upload_enw))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_data: raise RuntimeError('upload verification failed')
        if ardal_VALUE == '.java' and Gweithredu_gorchymyn('javac ' + shlex.quote(Enw)) != 0: return 1
        실행가능파일 = arg_ARAE.file.stem + '.elf'
        if ardal_VALUE == '.c' and Gweithredu_gorchymyn('cc ' + shlex.quote(Enw) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        Rhaglen = 'java ' + shlex.quote(arg_ARAE.class_name or arg_ARAE.file.stem) if ardal_VALUE in ('.java', '.class') else ('python ' if ardal_VALUE == '.py' else 'run ') + shlex.quote(Enw)
        if ardal_VALUE == '.jar': Rhaglen = 'java -jar ' + shlex.quote(Enw)
        if ardal_VALUE == '.c': Rhaglen = 'run ' + shlex.quote(실행가능파일)
        if arg_ARAE.linux: Rhaglen = 'run --linux ' + shlex.quote(Enw)
        if arg_ARAE.arguments: Rhaglen += ' ' + ' '.join(shlex.quote(testun_data) for testun_data in arg_ARAE.arguments)
        return 0 if Gweithredu_gorchymyn(Rhaglen) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        dewisydd.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Gweithredu_2())
