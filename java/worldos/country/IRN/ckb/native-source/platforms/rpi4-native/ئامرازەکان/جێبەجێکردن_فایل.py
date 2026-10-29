#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. جێدەر 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from جێبەجێکردن_فەرمان import فەرمان


def ڕادان():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ناو(예: ڕەوایی.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class فایل 또는 class 디렉터리(패키지 ناو 유지)')
    ئارگیومێنت_ڕیزی_داتا = 인수해석기.parse_args()
    دەیتا = ئارگیومێنت_ڕیزی_داتا.file.read_bytes()
    if ئارگیومێنت_ڕیزی_داتا.class_name and ئارگیومێنت_ڕیزی_داتا.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ناو = ئارگیومێنت_ڕیزی_داتا.class_name + '.class' if ئارگیومێنت_ڕیزی_داتا.class_name else ئارگیومێنت_ڕیزی_داتا.file.name
    if len(دەیتا) > 16384 or not 1 <= len(ناو.encode('utf-8')) <= 63 or '\n' in ناو or '\r' in ناو:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    پۆل_نرخ = '.elf' if دەیتا[:4] == b'\x7fELF' else ئارگیومێنت_ڕیزی_داتا.file.suffix
    if ئارگیومێنت_ڕیزی_داتا.linux and پۆل_نرخ != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if پۆل_نرخ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ئارگیومێنت_ڕیزی_داتا.arguments) > 7 or any(len(رست_دەیتا.encode('utf-8')) > 255 or '\n' in رست_دەیتا or '\r' in رست_دەیتا for رست_دەیتا in ئارگیومێنت_ڕیزی_داتا.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    بەربژارەکان = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ئارگیومێنت_ڕیزی_داتا.vnc: بەربژارەکان += ['-vnc', ئارگیومێنت_ڕیزی_داتا.vnc]
    پرۆسە = subprocess.Popen(فەرمان() + بەربژارەکان, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    هەڵبژێرەر = selectors.DefaultSelector(); هەڵبژێرەر.register(پرۆسە.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); دوایی_کردن_ئۆفسێت = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > دوایی_کردن_ئۆفسێت: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in هەڵبژێرەر.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if پرۆسە.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ناردن(دێڕ, 확인표시=b'jkoros-native> '):
        پرۆسە.stdin.write(دێڕ.encode('utf-8') + b'\n'); پرۆسە.stdin.flush()
        return 수신하기(확인표시)
    def جێبەجێکردن_فەرمان(دێڕ):
        출력결과 = ناردن(دێڕ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        فایل_لیست = []
        for 포함항목 in ئارگیومێنت_ڕیزی_داتا.include:
            if 포함항목.is_dir():
                فایل_لیست += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                فایل_لیست.append((포함항목.name, 포함항목.read_bytes()))
        فایل_لیست = [(개수, جێمەبەست_دەیتا) for 개수, جێمەبەست_دەیتا in فایل_لیست if 개수 != ناو] + [(ناو, دەیتا)]
        for بار_کردن_ناو, بار_کردن_دەیتا in فایل_لیست:
            if len(بار_کردن_دەیتا) > 16384 or len(بار_کردن_ناو.encode('utf-8')) > 63 or '\n' in بار_کردن_ناو or '\r' in بار_کردن_ناو:
                raise ValueError('추가 파일의 ناو/گۆڕینی_ئەندازە 제한 초과: ' + بار_کردن_ناو)
            ناردن('load ' + shlex.quote(بار_کردن_ناو), b'hex> ')
            for 순번 in range(0, len(بار_کردن_دەیتا), 64): ناردن(بار_کردن_دەیتا[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ناردن('.'): raise RuntimeError('upload failed: ' + بار_کردن_ناو)
            갈무리자료 = ناردن('hex ' + shlex.quote(بار_کردن_ناو))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != بار_کردن_دەیتا: raise RuntimeError('upload verification failed')
        if پۆل_نرخ == '.java' and جێبەجێکردن_فەرمان('javac ' + shlex.quote(ناو)) != 0: return 1
        실행가능파일 = ئارگیومێنت_ڕیزی_داتا.file.stem + '.elf'
        if پۆل_نرخ == '.c' and جێبەجێکردن_فەرمان('cc ' + shlex.quote(ناو) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        بەرنامە = 'java ' + shlex.quote(ئارگیومێنت_ڕیزی_داتا.class_name or ئارگیومێنت_ڕیزی_داتا.file.stem) if پۆل_نرخ in ('.java', '.class') else ('python ' if پۆل_نرخ == '.py' else 'run ') + shlex.quote(ناو)
        if پۆل_نرخ == '.jar': بەرنامە = 'java -jar ' + shlex.quote(ناو)
        if پۆل_نرخ == '.c': بەرنامە = 'run ' + shlex.quote(실행가능파일)
        if ئارگیومێنت_ڕیزی_داتا.linux: بەرنامە = 'run --linux ' + shlex.quote(ناو)
        if ئارگیومێنت_ڕیزی_داتا.arguments: بەرنامە += ' ' + ' '.join(shlex.quote(رست_دەیتا) for رست_دەیتا in ئارگیومێنت_ڕیزی_داتا.arguments)
        return 0 if جێبەجێکردن_فەرمان(بەرنامە) == 0 else 1
    finally:
        if پرۆسە.poll() is None:
            پرۆسە.terminate()
            try: پرۆسە.wait(timeout=5)
            except subprocess.TimeoutExpired: پرۆسە.kill(); پرۆسە.wait(timeout=5)
        هەڵبژێرەر.close(); پرۆسە.stdin.close(); پرۆسە.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ڕادان())
