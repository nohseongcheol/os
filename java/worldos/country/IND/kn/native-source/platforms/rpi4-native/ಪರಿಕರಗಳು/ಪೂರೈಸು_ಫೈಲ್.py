#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ಹೋಸ್ಟ್ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ಪೂರೈಸು_ಆದೇಶ import ಆಜ್ಞೆ


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್ = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್.add_argument('file', type=Path)
    ಪಾರ್ಸರ್.add_argument('arguments', nargs='*')
    ಪಾರ್ಸರ್.add_argument('--class-name', help='패키지가 있는 .class의 전체 ಹೆಸರು(예: ಸಕ್ರಮೀಕರಿಸು.꾸러미시험)')
    ಪಾರ್ಸರ್.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    ಪಾರ್ಸರ್.add_argument('--vnc', help='예: 127.0.0.1:2')
    ಪಾರ್ಸರ್.add_argument('--include', action='append', type=Path, default=[], help='추가 class ಕಡತ 또는 class 디렉터리(패키지 ಹೆಸರು 유지)')
    ವಾದ_ಅರೇ = ಪಾರ್ಸರ್.parse_args()
    ಡೇಟಾ = ವಾದ_ಅರೇ.file.read_bytes()
    if ವಾದ_ಅರೇ.class_name and ವಾದ_ಅರೇ.file.suffix != '.class': ಪಾರ್ಸರ್.error('--class-name은 .class 입력에서 사용합니다.')
    ಹೆಸರು = ವಾದ_ಅರೇ.class_name + '.class' if ವಾದ_ಅರೇ.class_name else ವಾದ_ಅರೇ.file.name
    if len(ಡೇಟಾ) > 16384 or not 1 <= len(ಹೆಸರು.encode('utf-8')) <= 63 or '\n' in ಹೆಸರು or '\r' in ಹೆಸರು:
        ಪಾರ್ಸರ್.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ವರ್ಗ_ಮೌಲ್ಯ = '.elf' if ಡೇಟಾ[:4] == b'\x7fELF' else ವಾದ_ಅರೇ.file.suffix
    if ವಾದ_ಅರೇ.linux and ವರ್ಗ_ಮೌಲ್ಯ != '.elf': ಪಾರ್ಸರ್.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ವರ್ಗ_ಮೌಲ್ಯ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ಪಾರ್ಸರ್.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ವಾದ_ಅರೇ.arguments) > 7 or any(len(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ.encode('utf-8')) > 255 or '\n' in ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ or '\r' in ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ for ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ in ವಾದ_ಅರೇ.arguments):
        ಪಾರ್ಸರ್.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ಆಯ್ಕೆಗಳು = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ವಾದ_ಅರೇ.vnc: ಆಯ್ಕೆಗಳು += ['-vnc', ವಾದ_ಅರೇ.vnc]
    ಪ್ರಕ್ರಿಯೆ = subprocess.Popen(ಆಜ್ಞೆ() + ಆಯ್ಕೆಗಳು, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ಸೆಲೆಕ್ಟರ್ = selectors.DefaultSelector(); ಸೆಲೆಕ್ಟರ್.register(ಪ್ರಕ್ರಿಯೆ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ಸೆಲೆಕ್ಟರ್.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ಪ್ರಕ್ರಿಯೆ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ಕಳುಹಿಸಿ(ಸಾಲು, 확인표시=b'jkoros-native> '):
        ಪ್ರಕ್ರಿಯೆ.stdin.write(ಸಾಲು.encode('utf-8') + b'\n'); ಪ್ರಕ್ರಿಯೆ.stdin.flush()
        return 수신하기(확인표시)
    def ಪೂರೈಸು_ಆದೇಶ(ಸಾಲು):
        출력결과 = ಕಳುಹಿಸಿ(ಸಾಲು); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ಫೈಲ್_ಪಟ್ಟಿ = []
        for 포함항목 in ವಾದ_ಅರೇ.include:
            if 포함항목.is_dir():
                ಫೈಲ್_ಪಟ್ಟಿ += [(str(ಡೇಟಾ_ಹುದ್ದೆ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ಡೇಟಾ_ಹುದ್ದೆ.read_bytes()) for ಡೇಟಾ_ಹುದ್ದೆ in sorted(포함항목.rglob('*.class'))]
            else:
                ಫೈಲ್_ಪಟ್ಟಿ.append((포함항목.name, 포함항목.read_bytes()))
        ಫೈಲ್_ಪಟ್ಟಿ = [(개수, ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ) for 개수, ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ in ಫೈಲ್_ಪಟ್ಟಿ if 개수 != ಹೆಸರು] + [(ಹೆಸರು, ಡೇಟಾ)]
        for ಅಪ್_ಲೋಡ್_ಹೆಸರು, ಅಪ್_ಲೋಡ್_ಡೇಟಾ in ಫೈಲ್_ಪಟ್ಟಿ:
            if len(ಅಪ್_ಲೋಡ್_ಡೇಟಾ) > 16384 or len(ಅಪ್_ಲೋಡ್_ಹೆಸರು.encode('utf-8')) > 63 or '\n' in ಅಪ್_ಲೋಡ್_ಹೆಸರು or '\r' in ಅಪ್_ಲೋಡ್_ಹೆಸರು:
                raise ValueError('추가 파일의 ಹೆಸರು/ಗಾತ್ರ 제한 초과: ' + ಅಪ್_ಲೋಡ್_ಹೆಸರು)
            ಕಳುಹಿಸಿ('load ' + shlex.quote(ಅಪ್_ಲೋಡ್_ಹೆಸರು), b'hex> ')
            for 순번 in range(0, len(ಅಪ್_ಲೋಡ್_ಡೇಟಾ), 64): ಕಳುಹಿಸಿ(ಅಪ್_ಲೋಡ್_ಡೇಟಾ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ಕಳುಹಿಸಿ('.'): raise RuntimeError('upload failed: ' + ಅಪ್_ಲೋಡ್_ಹೆಸರು)
            갈무리자료 = ಕಳುಹಿಸಿ('hex ' + shlex.quote(ಅಪ್_ಲೋಡ್_ಹೆಸರು))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ಅಪ್_ಲೋಡ್_ಡೇಟಾ: raise RuntimeError('upload verification failed')
        if ವರ್ಗ_ಮೌಲ್ಯ == '.java' and ಪೂರೈಸು_ಆದೇಶ('javac ' + shlex.quote(ಹೆಸರು)) != 0: return 1
        실행가능파일 = ವಾದ_ಅರೇ.file.stem + '.elf'
        if ವರ್ಗ_ಮೌಲ್ಯ == '.c' and ಪೂರೈಸು_ಆದೇಶ('cc ' + shlex.quote(ಹೆಸರು) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ಅಪ್ಲಿ = 'java ' + shlex.quote(ವಾದ_ಅರೇ.class_name or ವಾದ_ಅರೇ.file.stem) if ವರ್ಗ_ಮೌಲ್ಯ in ('.java', '.class') else ('python ' if ವರ್ಗ_ಮೌಲ್ಯ == '.py' else 'run ') + shlex.quote(ಹೆಸರು)
        if ವರ್ಗ_ಮೌಲ್ಯ == '.jar': ಅಪ್ಲಿ = 'java -jar ' + shlex.quote(ಹೆಸರು)
        if ವರ್ಗ_ಮೌಲ್ಯ == '.c': ಅಪ್ಲಿ = 'run ' + shlex.quote(실행가능파일)
        if ವಾದ_ಅರೇ.linux: ಅಪ್ಲಿ = 'run --linux ' + shlex.quote(ಹೆಸರು)
        if ವಾದ_ಅರೇ.arguments: ಅಪ್ಲಿ += ' ' + ' '.join(shlex.quote(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ) for ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ in ವಾದ_ಅರೇ.arguments)
        return 0 if ಪೂರೈಸು_ಆದೇಶ(ಅಪ್ಲಿ) == 0 else 1
    finally:
        if ಪ್ರಕ್ರಿಯೆ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ.terminate()
            try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
            except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
        ಸೆಲೆಕ್ಟರ್.close(); ಪ್ರಕ್ರಿಯೆ.stdin.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ಚಲಾಯಿಸು_2())
