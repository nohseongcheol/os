#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. باقار 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ئىجرا_قىلىش_بۇيرۇق import بۇيرۇق


def ئىجرا_قىل_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ئاتى(예: دەلىللەش.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ھۆججەت 또는 class 디렉터리(패키지 ئاتى 유지)')
    دەلىل_رەت = 인수해석기.parse_args()
    مەلۇمات = دەلىل_رەت.file.read_bytes()
    if دەلىل_رەت.class_name and دەلىل_رەت.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ئاتى = دەلىل_رەت.class_name + '.class' if دەلىل_رەت.class_name else دەلىل_رەت.file.name
    if len(مەلۇمات) > 16384 or not 1 <= len(ئاتى.encode('utf-8')) <= 63 or '\n' in ئاتى or '\r' in ئاتى:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    تۈر_قىممىتى = '.elf' if مەلۇمات[:4] == b'\x7fELF' else دەلىل_رەت.file.suffix
    if دەلىل_رەت.linux and تۈر_قىممىتى != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if تۈر_قىممىتى not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(دەلىل_رەت.arguments) > 7 or any(len(ھەرپ_تىزمىسى_مەلۇمات.encode('utf-8')) > 255 or '\n' in ھەرپ_تىزمىسى_مەلۇمات or '\r' in ھەرپ_تىزمىسى_مەلۇمات for ھەرپ_تىزمىسى_مەلۇمات in دەلىل_رەت.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    تاللانمىلار = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if دەلىل_رەت.vnc: تاللانمىلار += ['-vnc', دەلىل_رەت.vnc]
    جەريان = subprocess.Popen(بۇيرۇق() + تاللانمىلار, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    تاللىغۇچ = selectors.DefaultSelector(); تاللىغۇچ.register(جەريان.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); تاماملىماق_ئاغما = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > تاماملىماق_ئاغما: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in تاللىغۇچ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if جەريان.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ئەۋەتمەك(قۇر, 확인표시=b'jkoros-native> '):
        جەريان.stdin.write(قۇر.encode('utf-8') + b'\n'); جەريان.stdin.flush()
        return 수신하기(확인표시)
    def ئىجرا_قىلىش_بۇيرۇق(قۇر):
        출력결과 = ئەۋەتمەك(قۇر); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ھۆججەت_تىزىم = []
        for 포함항목 in دەلىل_رەت.include:
            if 포함항목.is_dir():
                ھۆججەت_تىزىم += [(str(مەلۇمات_ئورۇنلاشتۇرۇش.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', مەلۇمات_ئورۇنلاشتۇرۇش.read_bytes()) for مەلۇمات_ئورۇنلاشتۇرۇش in sorted(포함항목.rglob('*.class'))]
            else:
                ھۆججەت_تىزىم.append((포함항목.name, 포함항목.read_bytes()))
        ھۆججەت_تىزىم = [(개수, نىشان_مەلۇمات) for 개수, نىشان_مەلۇمات in ھۆججەت_تىزىم if 개수 != ئاتى] + [(ئاتى, مەلۇمات)]
        for يۈكلىمەك_نامى, يۈكلىمەك_مەلۇمات in ھۆججەت_تىزىم:
            if len(يۈكلىمەك_مەلۇمات) > 16384 or len(يۈكلىمەك_نامى.encode('utf-8')) > 63 or '\n' in يۈكلىمەك_نامى or '\r' in يۈكلىمەك_نامى:
                raise ValueError('추가 파일의 ئاتى/چوڭلۇقى 제한 초과: ' + يۈكلىمەك_نامى)
            ئەۋەتمەك('load ' + shlex.quote(يۈكلىمەك_نامى), b'hex> ')
            for 순번 in range(0, len(يۈكلىمەك_مەلۇمات), 64): ئەۋەتمەك(يۈكلىمەك_مەلۇمات[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ئەۋەتمەك('.'): raise RuntimeError('upload failed: ' + يۈكلىمەك_نامى)
            갈무리자료 = ئەۋەتمەك('hex ' + shlex.quote(يۈكلىمەك_نامى))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != يۈكلىمەك_مەلۇمات: raise RuntimeError('upload verification failed')
        if تۈر_قىممىتى == '.java' and ئىجرا_قىلىش_بۇيرۇق('javac ' + shlex.quote(ئاتى)) != 0: return 1
        실행가능파일 = دەلىل_رەت.file.stem + '.elf'
        if تۈر_قىممىتى == '.c' and ئىجرا_قىلىش_بۇيرۇق('cc ' + shlex.quote(ئاتى) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ئەپ = 'java ' + shlex.quote(دەلىل_رەت.class_name or دەلىل_رەت.file.stem) if تۈر_قىممىتى in ('.java', '.class') else ('python ' if تۈر_قىممىتى == '.py' else 'run ') + shlex.quote(ئاتى)
        if تۈر_قىممىتى == '.jar': ئەپ = 'java -jar ' + shlex.quote(ئاتى)
        if تۈر_قىممىتى == '.c': ئەپ = 'run ' + shlex.quote(실행가능파일)
        if دەلىل_رەت.linux: ئەپ = 'run --linux ' + shlex.quote(ئاتى)
        if دەلىل_رەت.arguments: ئەپ += ' ' + ' '.join(shlex.quote(ھەرپ_تىزمىسى_مەلۇمات) for ھەرپ_تىزمىسى_مەلۇمات in دەلىل_رەت.arguments)
        return 0 if ئىجرا_قىلىش_بۇيرۇق(ئەپ) == 0 else 1
    finally:
        if جەريان.poll() is None:
            جەريان.terminate()
            try: جەريان.wait(timeout=5)
            except subprocess.TimeoutExpired: جەريان.kill(); جەريان.wait(timeout=5)
        تاللىغۇچ.close(); جەريان.stdin.close(); جەريان.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ئىجرا_قىل_2())
