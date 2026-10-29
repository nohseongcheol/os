#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. مهمان 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from تعميل_ڪرڻ_حڪم import حڪم


def هلائڻ():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 نالو(예: ڪارگر_ڪريو.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class فائل 또는 class 디렉터리(패키지 نالو 유지)')
    دليل_ترتيب = 인수해석기.parse_args()
    ڪوائف = دليل_ترتيب.file.read_bytes()
    if دليل_ترتيب.class_name and دليل_ترتيب.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    نالو = دليل_ترتيب.class_name + '.class' if دليل_ترتيب.class_name else دليل_ترتيب.file.name
    if len(ڪوائف) > 16384 or not 1 <= len(نالو.encode('utf-8')) <= 63 or '\n' in نالو or '\r' in نالو:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    قسم_قدر_4b6d6445 = '.elf' if ڪوائف[:4] == b'\x7fELF' else دليل_ترتيب.file.suffix
    if دليل_ترتيب.linux and قسم_قدر_4b6d6445 != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if قسم_قدر_4b6d6445 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(دليل_ترتيب.arguments) > 7 or any(len(اسٽرنگ_ڪوائف.encode('utf-8')) > 255 or '\n' in اسٽرنگ_ڪوائف or '\r' in اسٽرنگ_ڪوائف for اسٽرنگ_ڪوائف in دليل_ترتيب.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    اختيار = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if دليل_ترتيب.vnc: اختيار += ['-vnc', دليل_ترتيب.vnc]
    عمل_a7054519 = subprocess.Popen(حڪم() + اختيار, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    چونڊيندڙ = selectors.DefaultSelector(); چونڊيندڙ.register(عمل_a7054519.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ختم_ڪريو_آف_سيٽ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ختم_ڪريو_آف_سيٽ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in چونڊيندڙ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if عمل_a7054519.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def اي_ميل(لڪير, 확인표시=b'jkoros-native> '):
        عمل_a7054519.stdin.write(لڪير.encode('utf-8') + b'\n'); عمل_a7054519.stdin.flush()
        return 수신하기(확인표시)
    def تعميل_ڪرڻ_حڪم(لڪير):
        출력결과 = اي_ميل(لڪير); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        فائل_فهرست = []
        for 포함항목 in دليل_ترتيب.include:
            if 포함항목.is_dir():
                فائل_فهرست += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                فائل_فهرست.append((포함항목.name, 포함항목.read_bytes()))
        فائل_فهرست = [(개수, منزل_مقصود_ڪوائف) for 개수, منزل_مقصود_ڪوائف in فائل_فهرست if 개수 != نالو] + [(نالو, ڪوائف)]
        for اپ_لوڊ_ڪريو_نالو, اپ_لوڊ_ڪريو_ڪوائف in فائل_فهرست:
            if len(اپ_لوڊ_ڪريو_ڪوائف) > 16384 or len(اپ_لوڊ_ڪريو_نالو.encode('utf-8')) > 63 or '\n' in اپ_لوڊ_ڪريو_نالو or '\r' in اپ_لوڊ_ڪريو_نالو:
                raise ValueError('추가 파일의 نالو/سائيز 제한 초과: ' + اپ_لوڊ_ڪريو_نالو)
            اي_ميل('load ' + shlex.quote(اپ_لوڊ_ڪريو_نالو), b'hex> ')
            for 순번 in range(0, len(اپ_لوڊ_ڪريو_ڪوائف), 64): اي_ميل(اپ_لوڊ_ڪريو_ڪوائف[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in اي_ميل('.'): raise RuntimeError('upload failed: ' + اپ_لوڊ_ڪريو_نالو)
            갈무리자료 = اي_ميل('hex ' + shlex.quote(اپ_لوڊ_ڪريو_نالو))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != اپ_لوڊ_ڪريو_ڪوائف: raise RuntimeError('upload verification failed')
        if قسم_قدر_4b6d6445 == '.java' and تعميل_ڪرڻ_حڪم('javac ' + shlex.quote(نالو)) != 0: return 1
        실행가능파일 = دليل_ترتيب.file.stem + '.elf'
        if قسم_قدر_4b6d6445 == '.c' and تعميل_ڪرڻ_حڪم('cc ' + shlex.quote(نالو) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ائپ = 'java ' + shlex.quote(دليل_ترتيب.class_name or دليل_ترتيب.file.stem) if قسم_قدر_4b6d6445 in ('.java', '.class') else ('python ' if قسم_قدر_4b6d6445 == '.py' else 'run ') + shlex.quote(نالو)
        if قسم_قدر_4b6d6445 == '.jar': ائپ = 'java -jar ' + shlex.quote(نالو)
        if قسم_قدر_4b6d6445 == '.c': ائپ = 'run ' + shlex.quote(실행가능파일)
        if دليل_ترتيب.linux: ائپ = 'run --linux ' + shlex.quote(نالو)
        if دليل_ترتيب.arguments: ائپ += ' ' + ' '.join(shlex.quote(اسٽرنگ_ڪوائف) for اسٽرنگ_ڪوائف in دليل_ترتيب.arguments)
        return 0 if تعميل_ڪرڻ_حڪم(ائپ) == 0 else 1
    finally:
        if عمل_a7054519.poll() is None:
            عمل_a7054519.terminate()
            try: عمل_a7054519.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل_a7054519.kill(); عمل_a7054519.wait(timeout=5)
        چونڊيندڙ.close(); عمل_a7054519.stdin.close(); عمل_a7054519.stdout.close()


if __name__ == '__main__':
    raise SystemExit(هلائڻ())
