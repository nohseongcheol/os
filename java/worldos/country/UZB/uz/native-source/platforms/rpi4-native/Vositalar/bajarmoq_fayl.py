#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. tashkilotchi 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from bajarmoq_buyruq import Buyruq


def Bajarish():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Nomi(예: tasdiqlash.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fayl 또는 class 디렉터리(패키지 Nomi 유지)')
    dalil_ARRAY = parser.parse_args()
    ma_lumotlar = dalil_ARRAY.file.read_bytes()
    if dalil_ARRAY.class_name and dalil_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Nomi = dalil_ARRAY.class_name + '.class' if dalil_ARRAY.class_name else dalil_ARRAY.file.name
    if len(ma_lumotlar) > 16384 or not 1 <= len(Nomi.encode('utf-8')) <= 63 or '\n' in Nomi or '\r' in Nomi:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    toifa_VALUE = '.elf' if ma_lumotlar[:4] == b'\x7fELF' else dalil_ARRAY.file.suffix
    if dalil_ARRAY.linux and toifa_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if toifa_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(dalil_ARRAY.arguments) > 7 or any(len(satr_ma_lumotlar.encode('utf-8')) > 255 or '\n' in satr_ma_lumotlar or '\r' in satr_ma_lumotlar for satr_ma_lumotlar in dalil_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Opsiyalar = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if dalil_ARRAY.vnc: Opsiyalar += ['-vnc', dalil_ARRAY.vnc]
    Jarayon = subprocess.Popen(Buyruq() + Opsiyalar, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tanlagich = selectors.DefaultSelector(); tanlagich.register(Jarayon.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); to_xtatmoq_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > to_xtatmoq_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in tanlagich.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Jarayon.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def yuborish(satr, 확인표시=b'jkoros-native> '):
        Jarayon.stdin.write(satr.encode('utf-8') + b'\n'); Jarayon.stdin.flush()
        return 수신하기(확인표시)
    def bajarmoq_buyruq(satr):
        출력결과 = yuborish(satr); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fayl_Ro_yxat = []
        for 포함항목 in dalil_ARRAY.include:
            if 포함항목.is_dir():
                fayl_Ro_yxat += [(str(ma_lumotlar_holat.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ma_lumotlar_holat.read_bytes()) for ma_lumotlar_holat in sorted(포함항목.rglob('*.class'))]
            else:
                fayl_Ro_yxat.append((포함항목.name, 포함항목.read_bytes()))
        fayl_Ro_yxat = [(element_COUNT, ko_chirish_joyi_ma_lumotlar) for element_COUNT, ko_chirish_joyi_ma_lumotlar in fayl_Ro_yxat if element_COUNT != Nomi] + [(Nomi, ma_lumotlar)]
        for uzatmoq_nom, uzatmoq_ma_lumotlar in fayl_Ro_yxat:
            if len(uzatmoq_ma_lumotlar) > 16384 or len(uzatmoq_nom.encode('utf-8')) > 63 or '\n' in uzatmoq_nom or '\r' in uzatmoq_nom:
                raise ValueError('추가 파일의 Nomi/Hajmi 제한 초과: ' + uzatmoq_nom)
            yuborish('load ' + shlex.quote(uzatmoq_nom), b'hex> ')
            for 순번 in range(0, len(uzatmoq_ma_lumotlar), 64): yuborish(uzatmoq_ma_lumotlar[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in yuborish('.'): raise RuntimeError('upload failed: ' + uzatmoq_nom)
            갈무리자료 = yuborish('hex ' + shlex.quote(uzatmoq_nom))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != uzatmoq_ma_lumotlar: raise RuntimeError('upload verification failed')
        if toifa_VALUE == '.java' and bajarmoq_buyruq('javac ' + shlex.quote(Nomi)) != 0: return 1
        실행가능파일 = dalil_ARRAY.file.stem + '.elf'
        if toifa_VALUE == '.c' and bajarmoq_buyruq('cc ' + shlex.quote(Nomi) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ilova = 'java ' + shlex.quote(dalil_ARRAY.class_name or dalil_ARRAY.file.stem) if toifa_VALUE in ('.java', '.class') else ('python ' if toifa_VALUE == '.py' else 'run ') + shlex.quote(Nomi)
        if toifa_VALUE == '.jar': ilova = 'java -jar ' + shlex.quote(Nomi)
        if toifa_VALUE == '.c': ilova = 'run ' + shlex.quote(실행가능파일)
        if dalil_ARRAY.linux: ilova = 'run --linux ' + shlex.quote(Nomi)
        if dalil_ARRAY.arguments: ilova += ' ' + ' '.join(shlex.quote(satr_ma_lumotlar) for satr_ma_lumotlar in dalil_ARRAY.arguments)
        return 0 if bajarmoq_buyruq(ilova) == 0 else 1
    finally:
        if Jarayon.poll() is None:
            Jarayon.terminate()
            try: Jarayon.wait(timeout=5)
            except subprocess.TimeoutExpired: Jarayon.kill(); Jarayon.wait(timeout=5)
        tanlagich.close(); Jarayon.stdin.close(); Jarayon.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Bajarish())
