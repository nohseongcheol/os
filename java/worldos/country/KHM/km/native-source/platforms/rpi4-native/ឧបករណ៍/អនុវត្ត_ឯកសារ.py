#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ហូស 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from អនុវត្ត_ពាក្យបញ្ជា import ពាក្យ_បញ្ជា


def រត់():
    មុខងារ_ញែក = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក.add_argument('file', type=Path)
    មុខងារ_ញែក.add_argument('arguments', nargs='*')
    មុខងារ_ញែក.add_argument('--class-name', help='패키지가 있는 .class의 전체 ឈ្មោះ(예: ធ្វើអោយមានសុពលភាព.꾸러미시험)')
    មុខងារ_ញែក.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    មុខងារ_ញែក.add_argument('--vnc', help='예: 127.0.0.1:2')
    មុខងារ_ញែក.add_argument('--include', action='append', type=Path, default=[], help='추가 class ឯកសារ 또는 class 디렉터리(패키지 ឈ្មោះ 유지)')
    អាគុយម៉ង់_អារេ = មុខងារ_ញែក.parse_args()
    ទិន្នន័យ = អាគុយម៉ង់_អារេ.file.read_bytes()
    if អាគុយម៉ង់_អារេ.class_name and អាគុយម៉ង់_អារេ.file.suffix != '.class': មុខងារ_ញែក.error('--class-name은 .class 입력에서 사용합니다.')
    ឈ្មោះ = អាគុយម៉ង់_អារេ.class_name + '.class' if អាគុយម៉ង់_អារេ.class_name else អាគុយម៉ង់_អារេ.file.name
    if len(ទិន្នន័យ) > 16384 or not 1 <= len(ឈ្មោះ.encode('utf-8')) <= 63 or '\n' in ឈ្មោះ or '\r' in ឈ្មោះ:
        មុខងារ_ញែក.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ប្រភេទ_តំលៃ = '.elf' if ទិន្នន័យ[:4] == b'\x7fELF' else អាគុយម៉ង់_អារេ.file.suffix
    if អាគុយម៉ង់_អារេ.linux and ប្រភេទ_តំលៃ != '.elf': មុខងារ_ញែក.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ប្រភេទ_តំលៃ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        មុខងារ_ញែក.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(អាគុយម៉ង់_អារេ.arguments) > 7 or any(len(សំនុំអក្សរ_ទិន្នន័យ.encode('utf-8')) > 255 or '\n' in សំនុំអក្សរ_ទិន្នន័យ or '\r' in សំនុំអក្សរ_ទិន្នន័យ for សំនុំអក្សរ_ទិន្នន័យ in អាគុយម៉ង់_អារេ.arguments):
        មុខងារ_ញែក.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ជំរើស = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if អាគុយម៉ង់_អារេ.vnc: ជំរើស += ['-vnc', អាគុយម៉ង់_អារេ.vnc]
    ដំណើរការ = subprocess.Popen(ពាក្យ_បញ្ជា() + ជំរើស, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    អ្នកជ្រើសរើស = selectors.DefaultSelector(); អ្នកជ្រើសរើស.register(ដំណើរការ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); បញ្ចប់_ការបែង_ភាគ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > បញ្ចប់_ការបែង_ភាគ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in អ្នកជ្រើសរើស.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ដំណើរការ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ផ្ញើ(បន្ទាត់, 확인표시=b'jkoros-native> '):
        ដំណើរការ.stdin.write(បន្ទាត់.encode('utf-8') + b'\n'); ដំណើរការ.stdin.flush()
        return 수신하기(확인표시)
    def អនុវត្ត_ពាក្យបញ្ជា(បន្ទាត់):
        출력결과 = ផ្ញើ(បន្ទាត់); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ឯកសារ_បញ្ជី = []
        for 포함항목 in អាគុយម៉ង់_អារេ.include:
            if 포함항목.is_dir():
                ឯកសារ_បញ្ជី += [(str(ទិន្នន័យ_កំណត់ទីតាំង.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ទិន្នន័យ_កំណត់ទីតាំង.read_bytes()) for ទិន្នន័យ_កំណត់ទីតាំង in sorted(포함항목.rglob('*.class'))]
            else:
                ឯកសារ_បញ្ជី.append((포함항목.name, 포함항목.read_bytes()))
        ឯកសារ_បញ្ជី = [(개수, ទិសដៅ_ទិន្នន័យ) for 개수, ទិសដៅ_ទិន្នន័យ in ឯកសារ_បញ្ជី if 개수 != ឈ្មោះ] + [(ឈ្មោះ, ទិន្នន័យ)]
        for បង្ហោះ_ឈ្មោះ, បង្ហោះ_ទិន្នន័យ in ឯកសារ_បញ្ជី:
            if len(បង្ហោះ_ទិន្នន័យ) > 16384 or len(បង្ហោះ_ឈ្មោះ.encode('utf-8')) > 63 or '\n' in បង្ហោះ_ឈ្មោះ or '\r' in បង្ហោះ_ឈ្មោះ:
                raise ValueError('추가 파일의 ឈ្មោះ/ដាក់ទំហំ 제한 초과: ' + បង្ហោះ_ឈ្មោះ)
            ផ្ញើ('load ' + shlex.quote(បង្ហោះ_ឈ្មោះ), b'hex> ')
            for 순번 in range(0, len(បង្ហោះ_ទិន្នន័យ), 64): ផ្ញើ(បង្ហោះ_ទិន្នន័យ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ផ្ញើ('.'): raise RuntimeError('upload failed: ' + បង្ហោះ_ឈ្មោះ)
            갈무리자료 = ផ្ញើ('hex ' + shlex.quote(បង្ហោះ_ឈ្មោះ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != បង្ហោះ_ទិន្នន័យ: raise RuntimeError('upload verification failed')
        if ប្រភេទ_តំលៃ == '.java' and អនុវត្ត_ពាក្យបញ្ជា('javac ' + shlex.quote(ឈ្មោះ)) != 0: return 1
        실행가능파일 = អាគុយម៉ង់_អារេ.file.stem + '.elf'
        if ប្រភេទ_តំលៃ == '.c' and អនុវត្ត_ពាក្យបញ្ជា('cc ' + shlex.quote(ឈ្មោះ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        កម្មវិធី = 'java ' + shlex.quote(អាគុយម៉ង់_អារេ.class_name or អាគុយម៉ង់_អារេ.file.stem) if ប្រភេទ_តំលៃ in ('.java', '.class') else ('python ' if ប្រភេទ_តំលៃ == '.py' else 'run ') + shlex.quote(ឈ្មោះ)
        if ប្រភេទ_តំលៃ == '.jar': កម្មវិធី = 'java -jar ' + shlex.quote(ឈ្មោះ)
        if ប្រភេទ_តំលៃ == '.c': កម្មវិធី = 'run ' + shlex.quote(실행가능파일)
        if អាគុយម៉ង់_អារេ.linux: កម្មវិធី = 'run --linux ' + shlex.quote(ឈ្មោះ)
        if អាគុយម៉ង់_អារេ.arguments: កម្មវិធី += ' ' + ' '.join(shlex.quote(សំនុំអក្សរ_ទិន្នន័យ) for សំនុំអក្សរ_ទិន្នន័យ in អាគុយម៉ង់_អារេ.arguments)
        return 0 if អនុវត្ត_ពាក្យបញ្ជា(កម្មវិធី) == 0 else 1
    finally:
        if ដំណើរការ.poll() is None:
            ដំណើរការ.terminate()
            try: ដំណើរការ.wait(timeout=5)
            except subprocess.TimeoutExpired: ដំណើរការ.kill(); ដំណើរការ.wait(timeout=5)
        អ្នកជ្រើសរើស.close(); ដំណើរការ.stdin.close(); ដំណើរការ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(រត់())
