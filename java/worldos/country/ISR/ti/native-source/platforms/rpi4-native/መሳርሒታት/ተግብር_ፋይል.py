#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. አዐንግድ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ተግብር_ትእዛዝ import ትእዛዝ


def ኣኺድ():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ሽም(예: አረጋግፅ.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ፋይል 또는 class 디렉터리(패키지 ሽም 유지)')
    ሓባሪ_ቁጽሪ_ተርታ = 인수해석기.parse_args()
    ሓበሬታ = ሓባሪ_ቁጽሪ_ተርታ.file.read_bytes()
    if ሓባሪ_ቁጽሪ_ተርታ.class_name and ሓባሪ_ቁጽሪ_ተርታ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ሽም = ሓባሪ_ቁጽሪ_ተርታ.class_name + '.class' if ሓባሪ_ቁጽሪ_ተርታ.class_name else ሓባሪ_ቁጽሪ_ተርታ.file.name
    if len(ሓበሬታ) > 16384 or not 1 <= len(ሽም.encode('utf-8')) <= 63 or '\n' in ሽም or '\r' in ሽም:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    መደብ_ዋጋ = '.elf' if ሓበሬታ[:4] == b'\x7fELF' else ሓባሪ_ቁጽሪ_ተርታ.file.suffix
    if ሓባሪ_ቁጽሪ_ተርታ.linux and መደብ_ዋጋ != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if መደብ_ዋጋ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ሓባሪ_ቁጽሪ_ተርታ.arguments) > 7 or any(len(ሕብረ_ቁምፊ_ሓበሬታ.encode('utf-8')) > 255 or '\n' in ሕብረ_ቁምፊ_ሓበሬታ or '\r' in ሕብረ_ቁምፊ_ሓበሬታ for ሕብረ_ቁምፊ_ሓበሬታ in ሓባሪ_ቁጽሪ_ተርታ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ኣማራጽታት = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ሓባሪ_ቁጽሪ_ተርታ.vnc: ኣማራጽታት += ['-vnc', ሓባሪ_ቁጽሪ_ተርታ.vnc]
    መስርሕ = subprocess.Popen(ትእዛዝ() + ኣማራጽታት, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራፂ = selectors.DefaultSelector(); መራፂ.register(መስርሕ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ኣቑም_ሽፋን = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ኣቑም_ሽፋን: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in መራፂ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if መስርሕ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ለኣኽ(መስመር, 확인표시=b'jkoros-native> '):
        መስርሕ.stdin.write(መስመር.encode('utf-8') + b'\n'); መስርሕ.stdin.flush()
        return 수신하기(확인표시)
    def ተግብር_ትእዛዝ(መስመር):
        출력결과 = ለኣኽ(መስመር); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ፋይል_ዝርዝር = []
        for 포함항목 in ሓባሪ_ቁጽሪ_ተርታ.include:
            if 포함항목.is_dir():
                ፋይል_ዝርዝር += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ፋይል_ዝርዝር.append((포함항목.name, 포함항목.read_bytes()))
        ፋይል_ዝርዝር = [(개수, መዓልቦ_ሓበሬታ) for 개수, መዓልቦ_ሓበሬታ in ፋይል_ዝርዝር if 개수 != ሽም] + [(ሽም, ሓበሬታ)]
        for ስቐል_ሽም, ስቐል_ሓበሬታ in ፋይል_ዝርዝር:
            if len(ስቐል_ሓበሬታ) > 16384 or len(ስቐል_ሽም.encode('utf-8')) > 63 or '\n' in ስቐል_ሽም or '\r' in ስቐል_ሽም:
                raise ValueError('추가 파일의 ሽም/መጠን 제한 초과: ' + ስቐል_ሽም)
            ለኣኽ('load ' + shlex.quote(ስቐል_ሽም), b'hex> ')
            for 순번 in range(0, len(ስቐል_ሓበሬታ), 64): ለኣኽ(ስቐል_ሓበሬታ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ለኣኽ('.'): raise RuntimeError('upload failed: ' + ስቐል_ሽም)
            갈무리자료 = ለኣኽ('hex ' + shlex.quote(ስቐል_ሽም))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ስቐል_ሓበሬታ: raise RuntimeError('upload verification failed')
        if መደብ_ዋጋ == '.java' and ተግብር_ትእዛዝ('javac ' + shlex.quote(ሽም)) != 0: return 1
        실행가능파일 = ሓባሪ_ቁጽሪ_ተርታ.file.stem + '.elf'
        if መደብ_ዋጋ == '.c' and ተግብር_ትእዛዝ('cc ' + shlex.quote(ሽም) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        መተግበሪ = 'java ' + shlex.quote(ሓባሪ_ቁጽሪ_ተርታ.class_name or ሓባሪ_ቁጽሪ_ተርታ.file.stem) if መደብ_ዋጋ in ('.java', '.class') else ('python ' if መደብ_ዋጋ == '.py' else 'run ') + shlex.quote(ሽም)
        if መደብ_ዋጋ == '.jar': መተግበሪ = 'java -jar ' + shlex.quote(ሽም)
        if መደብ_ዋጋ == '.c': መተግበሪ = 'run ' + shlex.quote(실행가능파일)
        if ሓባሪ_ቁጽሪ_ተርታ.linux: መተግበሪ = 'run --linux ' + shlex.quote(ሽም)
        if ሓባሪ_ቁጽሪ_ተርታ.arguments: መተግበሪ += ' ' + ' '.join(shlex.quote(ሕብረ_ቁምፊ_ሓበሬታ) for ሕብረ_ቁምፊ_ሓበሬታ in ሓባሪ_ቁጽሪ_ተርታ.arguments)
        return 0 if ተግብር_ትእዛዝ(መተግበሪ) == 0 else 1
    finally:
        if መስርሕ.poll() is None:
            መስርሕ.terminate()
            try: መስርሕ.wait(timeout=5)
            except subprocess.TimeoutExpired: መስርሕ.kill(); መስርሕ.wait(timeout=5)
        መራፂ.close(); መስርሕ.stdin.close(); መስርሕ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ኣኺድ())
