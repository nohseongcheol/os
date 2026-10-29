#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. singatha 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from yenza_umyalo import Umlayelo


def Sebenzisa():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Igama(예: qinisekisa.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Ihele 또는 class 디렉터리(패키지 Igama 유지)')
    i_agumenti_AMALUNGU_AFANAYO = 인수해석기.parse_args()
    imininingwane = i_agumenti_AMALUNGU_AFANAYO.file.read_bytes()
    if i_agumenti_AMALUNGU_AFANAYO.class_name and i_agumenti_AMALUNGU_AFANAYO.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Igama = i_agumenti_AMALUNGU_AFANAYO.class_name + '.class' if i_agumenti_AMALUNGU_AFANAYO.class_name else i_agumenti_AMALUNGU_AFANAYO.file.name
    if len(imininingwane) > 16384 or not 1 <= len(Igama.encode('utf-8')) <= 63 or '\n' in Igama or '\r' in Igama:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    umunxa_inani = '.elf' if imininingwane[:4] == b'\x7fELF' else i_agumenti_AMALUNGU_AFANAYO.file.suffix
    if i_agumenti_AMALUNGU_AFANAYO.linux and umunxa_inani != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if umunxa_inani not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(i_agumenti_AMALUNGU_AFANAYO.arguments) > 7 or any(len(uchunge_imininingwane.encode('utf-8')) > 255 or '\n' in uchunge_imininingwane or '\r' in uchunge_imininingwane for uchunge_imininingwane in i_agumenti_AMALUNGU_AFANAYO.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Izinketho = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if i_agumenti_AMALUNGU_AFANAYO.vnc: Izinketho += ['-vnc', i_agumenti_AMALUNGU_AFANAYO.vnc]
    Inqubo = subprocess.Popen(Umlayelo() + Izinketho, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    isiqoki = selectors.DefaultSelector(); isiqoki.register(Inqubo.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); yekisa_I_ofisethi = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > yekisa_I_ofisethi: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in isiqoki.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Inqubo.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def Thumela(umugqa, 확인표시=b'jkoros-native> '):
        Inqubo.stdin.write(umugqa.encode('utf-8') + b'\n'); Inqubo.stdin.flush()
        return 수신하기(확인표시)
    def yenza_umyalo(umugqa):
        출력결과 = Thumela(umugqa); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ifayela_Uhlu = []
        for 포함항목 in i_agumenti_AMALUNGU_AFANAYO.include:
            if 포함항목.is_dir():
                ifayela_Uhlu += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ifayela_Uhlu.append((포함항목.name, 포함항목.read_bytes()))
        ifayela_Uhlu = [(개수, isikhumulo_imininingwane) for 개수, isikhumulo_imininingwane in ifayela_Uhlu if 개수 != Igama] + [(Igama, imininingwane)]
        for layisha_igama, layisha_imininingwane in ifayela_Uhlu:
            if len(layisha_imininingwane) > 16384 or len(layisha_igama.encode('utf-8')) > 63 or '\n' in layisha_igama or '\r' in layisha_igama:
                raise ValueError('추가 파일의 Igama/Ubungako 제한 초과: ' + layisha_igama)
            Thumela('load ' + shlex.quote(layisha_igama), b'hex> ')
            for 순번 in range(0, len(layisha_imininingwane), 64): Thumela(layisha_imininingwane[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in Thumela('.'): raise RuntimeError('upload failed: ' + layisha_igama)
            갈무리자료 = Thumela('hex ' + shlex.quote(layisha_igama))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != layisha_imininingwane: raise RuntimeError('upload verification failed')
        if umunxa_inani == '.java' and yenza_umyalo('javac ' + shlex.quote(Igama)) != 0: return 1
        실행가능파일 = i_agumenti_AMALUNGU_AFANAYO.file.stem + '.elf'
        if umunxa_inani == '.c' and yenza_umyalo('cc ' + shlex.quote(Igama) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        i_app = 'java ' + shlex.quote(i_agumenti_AMALUNGU_AFANAYO.class_name or i_agumenti_AMALUNGU_AFANAYO.file.stem) if umunxa_inani in ('.java', '.class') else ('python ' if umunxa_inani == '.py' else 'run ') + shlex.quote(Igama)
        if umunxa_inani == '.jar': i_app = 'java -jar ' + shlex.quote(Igama)
        if umunxa_inani == '.c': i_app = 'run ' + shlex.quote(실행가능파일)
        if i_agumenti_AMALUNGU_AFANAYO.linux: i_app = 'run --linux ' + shlex.quote(Igama)
        if i_agumenti_AMALUNGU_AFANAYO.arguments: i_app += ' ' + ' '.join(shlex.quote(uchunge_imininingwane) for uchunge_imininingwane in i_agumenti_AMALUNGU_AFANAYO.arguments)
        return 0 if yenza_umyalo(i_app) == 0 else 1
    finally:
        if Inqubo.poll() is None:
            Inqubo.terminate()
            try: Inqubo.wait(timeout=5)
            except subprocess.TimeoutExpired: Inqubo.kill(); Inqubo.wait(timeout=5)
        isiqoki.close(); Inqubo.stdin.close(); Inqubo.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Sebenzisa())
