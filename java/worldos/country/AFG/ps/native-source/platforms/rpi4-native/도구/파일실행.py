#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. کوربه 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import بولۍ


def ځغلول():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 نوم(예: 검증.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class دوتنه 또는 class 디렉터리(패키지 نوم 유지)')
    ارزښتوړى_لړوند = 인수해석기.parse_args()
    اومتوک = ارزښتوړى_لړوند.file.read_bytes()
    if ارزښتوړى_لړوند.class_name and ارزښتوړى_لړوند.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    نوم = ارزښتوړى_لړوند.class_name + '.class' if ارزښتوړى_لړوند.class_name else ارزښتوړى_لړوند.file.name
    if len(اومتوک) > 16384 or not 1 <= len(نوم.encode('utf-8')) <= 63 or '\n' in نوم or '\r' in نوم:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ټولۍ_ارزښت = '.elf' if اومتوک[:4] == b'\x7fELF' else ارزښتوړى_لړوند.file.suffix
    if ارزښتوړى_لړوند.linux and ټولۍ_ارزښت != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ټولۍ_ارزښت not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ارزښتوړى_لړوند.arguments) > 7 or any(len(مزى_اومتوک.encode('utf-8')) > 255 or '\n' in مزى_اومتوک or '\r' in مزى_اومتوک for مزى_اومتوک in ارزښتوړى_لړوند.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    غوراوي = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ارزښتوړى_لړوند.vnc: غوراوي += ['-vnc', ارزښتوړى_لړوند.vnc]
    بهير = subprocess.Popen(بولۍ() + غوراوي, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(بهير.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if بهير.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def استول(ليکه, 확인표시=b'jkoros-native> '):
        بهير.stdin.write(ليکه.encode('utf-8') + b'\n'); بهير.stdin.flush()
        return 수신하기(확인표시)
    def 실행(ليکه):
        출력결과 = استول(ليکه); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        파일목록 = []
        for 포함항목 in ارزښتوړى_لړوند.include:
            if 포함항목.is_dir():
                파일목록 += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                파일목록.append((포함항목.name, 포함항목.read_bytes()))
        파일목록 = [(개수, موخه_اومتوک) for 개수, موخه_اومتوک in 파일목록 if 개수 != نوم] + [(نوم, اومتوک)]
        for 올릴이름, ورلېښل_اومتوک in 파일목록:
            if len(ورلېښل_اومتوک) > 16384 or len(올릴이름.encode('utf-8')) > 63 or '\n' in 올릴이름 or '\r' in 올릴이름:
                raise ValueError('추가 파일의 نوم/کچ 제한 초과: ' + 올릴이름)
            استول('load ' + shlex.quote(올릴이름), b'hex> ')
            for 순번 in range(0, len(ورلېښل_اومتوک), 64): استول(ورلېښل_اومتوک[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in استول('.'): raise RuntimeError('upload failed: ' + 올릴이름)
            갈무리자료 = استول('hex ' + shlex.quote(올릴이름))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ورلېښل_اومتوک: raise RuntimeError('upload verification failed')
        if ټولۍ_ارزښت == '.java' and 실행('javac ' + shlex.quote(نوم)) != 0: return 1
        실행가능파일 = ارزښتوړى_لړوند.file.stem + '.elf'
        if ټولۍ_ارزښت == '.c' and 실행('cc ' + shlex.quote(نوم) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        کاريال = 'java ' + shlex.quote(ارزښتوړى_لړوند.class_name or ارزښتوړى_لړوند.file.stem) if ټولۍ_ارزښت in ('.java', '.class') else ('python ' if ټولۍ_ارزښت == '.py' else 'run ') + shlex.quote(نوم)
        if ټولۍ_ارزښت == '.jar': کاريال = 'java -jar ' + shlex.quote(نوم)
        if ټولۍ_ارزښت == '.c': کاريال = 'run ' + shlex.quote(실행가능파일)
        if ارزښتوړى_لړوند.linux: کاريال = 'run --linux ' + shlex.quote(نوم)
        if ارزښتوړى_لړوند.arguments: کاريال += ' ' + ' '.join(shlex.quote(مزى_اومتوک) for مزى_اومتوک in ارزښتوړى_لړوند.arguments)
        return 0 if 실행(کاريال) == 0 else 1
    finally:
        if بهير.poll() is None:
            بهير.terminate()
            try: بهير.wait(timeout=5)
            except subprocess.TimeoutExpired: بهير.kill(); بهير.wait(timeout=5)
        준비선택기.close(); بهير.stdin.close(); بهير.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ځغلول())
