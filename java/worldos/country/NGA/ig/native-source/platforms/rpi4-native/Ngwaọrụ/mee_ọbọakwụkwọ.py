#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. usu 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from mee_nnyemiwu import Ntiiwu


def Bido():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Aha(예: mee_ịbanihe.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Faịlụ 또는 class 디렉터리(패키지 Aha 유지)')
    agụment_MKPOKỌTA = 인수해석기.parse_args()
    datà = agụment_MKPOKỌTA.file.read_bytes()
    if agụment_MKPOKỌTA.class_name and agụment_MKPOKỌTA.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Aha = agụment_MKPOKỌTA.class_name + '.class' if agụment_MKPOKỌTA.class_name else agụment_MKPOKỌTA.file.name
    if len(datà) > 16384 or not 1 <= len(Aha.encode('utf-8')) <= 63 or '\n' in Aha or '\r' in Aha:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    otu_valuu_4b6d6445 = '.elf' if datà[:4] == b'\x7fELF' else agụment_MKPOKỌTA.file.suffix
    if agụment_MKPOKỌTA.linux and otu_valuu_4b6d6445 != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if otu_valuu_4b6d6445 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(agụment_MKPOKỌTA.arguments) > 7 or any(len(ùsòròokwū_datà.encode('utf-8')) > 255 or '\n' in ùsòròokwū_datà or '\r' in ùsòròokwū_datà for ùsòròokwū_datà in agụment_MKPOKỌTA.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Ihenhọrọga = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if agụment_MKPOKỌTA.vnc: Ihenhọrọga += ['-vnc', agụment_MKPOKỌTA.vnc]
    ùsòrò = subprocess.Popen(Ntiiwu() + Ihenhọrọga, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ihe_nhọpụta = selectors.DefaultSelector(); ihe_nhọpụta.register(ùsòrò.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); mèdebe_Nnokwata = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > mèdebe_Nnokwata: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ihe_nhọpụta.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ùsòrò.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def zìga(ahịrī, 확인표시=b'jkoros-native> '):
        ùsòrò.stdin.write(ahịrī.encode('utf-8') + b'\n'); ùsòrò.stdin.flush()
        return 수신하기(확인표시)
    def mee_nnyemiwu(ahịrī):
        출력결과 = zìga(ahịrī); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ọbọakwụkwọ_ndepụta = []
        for 포함항목 in agụment_MKPOKỌTA.include:
            if 포함항목.is_dir():
                ọbọakwụkwọ_ndepụta += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ọbọakwụkwọ_ndepụta.append((포함항목.name, 포함항목.read_bytes()))
        ọbọakwụkwọ_ndepụta = [(개수, ebemwèga_datà) for 개수, ebemwèga_datà in ọbọakwụkwọ_ndepụta if 개수 != Aha] + [(Aha, datà)]
        for bùlie_akara_ahà, bùlie_datà in ọbọakwụkwọ_ndepụta:
            if len(bùlie_datà) > 16384 or len(bùlie_akara_ahà.encode('utf-8')) > 63 or '\n' in bùlie_akara_ahà or '\r' in bùlie_akara_ahà:
                raise ValueError('추가 파일의 Aha/Ụhara 제한 초과: ' + bùlie_akara_ahà)
            zìga('load ' + shlex.quote(bùlie_akara_ahà), b'hex> ')
            for 순번 in range(0, len(bùlie_datà), 64): zìga(bùlie_datà[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in zìga('.'): raise RuntimeError('upload failed: ' + bùlie_akara_ahà)
            갈무리자료 = zìga('hex ' + shlex.quote(bùlie_akara_ahà))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != bùlie_datà: raise RuntimeError('upload verification failed')
        if otu_valuu_4b6d6445 == '.java' and mee_nnyemiwu('javac ' + shlex.quote(Aha)) != 0: return 1
        실행가능파일 = agụment_MKPOKỌTA.file.stem + '.elf'
        if otu_valuu_4b6d6445 == '.c' and mee_nnyemiwu('cc ' + shlex.quote(Aha) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        app = 'java ' + shlex.quote(agụment_MKPOKỌTA.class_name or agụment_MKPOKỌTA.file.stem) if otu_valuu_4b6d6445 in ('.java', '.class') else ('python ' if otu_valuu_4b6d6445 == '.py' else 'run ') + shlex.quote(Aha)
        if otu_valuu_4b6d6445 == '.jar': app = 'java -jar ' + shlex.quote(Aha)
        if otu_valuu_4b6d6445 == '.c': app = 'run ' + shlex.quote(실행가능파일)
        if agụment_MKPOKỌTA.linux: app = 'run --linux ' + shlex.quote(Aha)
        if agụment_MKPOKỌTA.arguments: app += ' ' + ' '.join(shlex.quote(ùsòròokwū_datà) for ùsòròokwū_datà in agụment_MKPOKỌTA.arguments)
        return 0 if mee_nnyemiwu(app) == 0 else 1
    finally:
        if ùsòrò.poll() is None:
            ùsòrò.terminate()
            try: ùsòrò.wait(timeout=5)
            except subprocess.TimeoutExpired: ùsòrò.kill(); ùsòrò.wait(timeout=5)
        ihe_nhọpụta.close(); ùsòrò.stdin.close(); ùsòrò.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Bido())
