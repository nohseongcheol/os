#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from icra_etmək_əmr import Əmr


def İcra_Et():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ad(예: təsdiqlə.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='추가 class FAYL 또는 class 디렉터리(패키지 Ad 유지)')
    arqument_ARRAY = parser.parse_args()
    verilənlər = arqument_ARRAY.file.read_bytes()
    if arqument_ARRAY.class_name and arqument_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    Ad = arqument_ARRAY.class_name + '.class' if arqument_ARRAY.class_name else arqument_ARRAY.file.name
    if len(verilənlər) > 16384 or not 1 <= len(Ad.encode('utf-8')) <= 63 or '\n' in Ad or '\r' in Ad:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    sahə_VALUE = '.elf' if verilənlər[:4] == b'\x7fELF' else arqument_ARRAY.file.suffix
    if arqument_ARRAY.linux and sahə_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if sahə_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(arqument_ARRAY.arguments) > 7 or any(len(sətir_verilənlər.encode('utf-8')) > 255 or '\n' in sətir_verilənlər or '\r' in sətir_verilənlər for sətir_verilənlər in arqument_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Seçimlər = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if arqument_ARRAY.vnc: Seçimlər += ['-vnc', arqument_ARRAY.vnc]
    Proses = subprocess.Popen(Əmr() + Seçimlər, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici = selectors.DefaultSelector(); seçici.register(Proses.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); bitirmək_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > bitirmək_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in seçici.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proses.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def göndərmək(Giriş, 확인표시=b'jkoros-native> '):
        Proses.stdin.write(Giriş.encode('utf-8') + b'\n'); Proses.stdin.flush()
        return 수신하기(확인표시)
    def icra_etmək_əmr(Giriş):
        출력결과 = göndərmək(Giriş); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fayl_Siyahı = []
        for 포함항목 in arqument_ARRAY.include:
            if 포함항목.is_dir():
                fayl_Siyahı += [(str(verilənlər_yerinə_qoymaq.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', verilənlər_yerinə_qoymaq.read_bytes()) for verilənlər_yerinə_qoymaq in sorted(포함항목.rglob('*.class'))]
            else:
                fayl_Siyahı.append((포함항목.name, 포함항목.read_bytes()))
        fayl_Siyahı = [(element_COUNT, təyinat_verilənlər) for element_COUNT, təyinat_verilənlər in fayl_Siyahı if element_COUNT != Ad] + [(Ad, verilənlər)]
        for Upload_ad, Upload_verilənlər in fayl_Siyahı:
            if len(Upload_verilənlər) > 16384 or len(Upload_ad.encode('utf-8')) > 63 or '\n' in Upload_ad or '\r' in Upload_ad:
                raise ValueError('추가 파일의 Ad/Böyüklük 제한 초과: ' + Upload_ad)
            göndərmək('load ' + shlex.quote(Upload_ad), b'hex> ')
            for 순번 in range(0, len(Upload_verilənlər), 64): göndərmək(Upload_verilənlər[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in göndərmək('.'): raise RuntimeError('upload failed: ' + Upload_ad)
            갈무리자료 = göndərmək('hex ' + shlex.quote(Upload_ad))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_verilənlər: raise RuntimeError('upload verification failed')
        if sahə_VALUE == '.java' and icra_etmək_əmr('javac ' + shlex.quote(Ad)) != 0: return 1
        실행가능파일 = arqument_ARRAY.file.stem + '.elf'
        if sahə_VALUE == '.c' and icra_etmək_əmr('cc ' + shlex.quote(Ad) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        proqram = 'java ' + shlex.quote(arqument_ARRAY.class_name or arqument_ARRAY.file.stem) if sahə_VALUE in ('.java', '.class') else ('python ' if sahə_VALUE == '.py' else 'run ') + shlex.quote(Ad)
        if sahə_VALUE == '.jar': proqram = 'java -jar ' + shlex.quote(Ad)
        if sahə_VALUE == '.c': proqram = 'run ' + shlex.quote(실행가능파일)
        if arqument_ARRAY.linux: proqram = 'run --linux ' + shlex.quote(Ad)
        if arqument_ARRAY.arguments: proqram += ' ' + ' '.join(shlex.quote(sətir_verilənlər) for sətir_verilənlər in arqument_ARRAY.arguments)
        return 0 if icra_etmək_əmr(proqram) == 0 else 1
    finally:
        if Proses.poll() is None:
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait(timeout=5)
        seçici.close(); Proses.stdin.close(); Proses.stdout.close()


if __name__ == '__main__':
    raise SystemExit(İcra_Et())
