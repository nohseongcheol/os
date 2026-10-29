#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ଆୟୋଜକ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ନିର୍ଦ୍ଦେଶ


def ଚଳାନ୍ତୁ():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ନାମ(예: ବୈଧକରଣ.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ଫାଇଲ 또는 class 디렉터리(패키지 ନାମ 유지)')
    ଯୁକ୍ତି_ଆରେ = 인수해석기.parse_args()
    ଡାଟା = ଯୁକ୍ତି_ଆରେ.file.read_bytes()
    if ଯୁକ୍ତି_ଆରେ.class_name and ଯୁକ୍ତି_ଆରେ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ନାମ = ଯୁକ୍ତି_ଆରେ.class_name + '.class' if ଯୁକ୍ତି_ଆରେ.class_name else ଯୁକ୍ତି_ଆରେ.file.name
    if len(ଡାଟା) > 16384 or not 1 <= len(ନାମ.encode('utf-8')) <= 63 or '\n' in ନାମ or '\r' in ନାମ:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ବର୍ଗ_ମୂଲ୍ୟ = '.elf' if ଡାଟା[:4] == b'\x7fELF' else ଯୁକ୍ତି_ଆରେ.file.suffix
    if ଯୁକ୍ତି_ଆରେ.linux and ବର୍ଗ_ମୂଲ୍ୟ != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ବର୍ଗ_ମୂଲ୍ୟ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ଯୁକ୍ତି_ଆରେ.arguments) > 7 or any(len(ଷ୍ଟ୍ରିଂ_ଡାଟା.encode('utf-8')) > 255 or '\n' in ଷ୍ଟ୍ରିଂ_ଡାଟା or '\r' in ଷ୍ଟ୍ରିଂ_ଡାଟା for ଷ୍ଟ୍ରିଂ_ଡାଟା in ଯୁକ୍ତି_ଆରେ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ବିକଳ୍ପ_ସମୂହ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ଯୁକ୍ତି_ଆରେ.vnc: ବିକଳ୍ପ_ସମୂହ += ['-vnc', ଯୁକ୍ତି_ଆରେ.vnc]
    ପ୍ରକ୍ରିୟା = subprocess.Popen(ନିର୍ଦ୍ଦେଶ() + ବିକଳ୍ପ_ସମୂହ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ଚୟନକାରୀ = selectors.DefaultSelector(); ଚୟନକାରୀ.register(ପ୍ରକ୍ରିୟା.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ଚୟନକାରୀ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ପ୍ରକ୍ରିୟା.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ପଠାନ୍ତୁ(ରେଖା, 확인표시=b'jkoros-native> '):
        ପ୍ରକ୍ରିୟା.stdin.write(ରେଖା.encode('utf-8') + b'\n'); ପ୍ରକ୍ରିୟା.stdin.flush()
        return 수신하기(확인표시)
    def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ରେଖା):
        출력결과 = ପଠାନ୍ତୁ(ରେଖା); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ଫାଇଲ୍_ତାଲିକା = []
        for 포함항목 in ଯୁକ୍ତି_ଆରେ.include:
            if 포함항목.is_dir():
                ଫାଇଲ୍_ତାଲିକା += [(str(ଡାଟା_ସ୍ଥିତି.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ଡାଟା_ସ୍ଥିତି.read_bytes()) for ଡାଟା_ସ୍ଥିତି in sorted(포함항목.rglob('*.class'))]
            else:
                ଫାଇଲ୍_ତାଲିକା.append((포함항목.name, 포함항목.read_bytes()))
        ଫାଇଲ୍_ତାଲିକା = [(개수, ଲକ୍ଷସ୍ଥଳ_ଡାଟା) for 개수, ଲକ୍ଷସ୍ଥଳ_ଡାଟା in ଫାଇଲ୍_ତାଲିକା if 개수 != ନାମ] + [(ନାମ, ଡାଟା)]
        for ଅପଲୋଡ୍_ନାମ, ଅପଲୋଡ୍_ଡାଟା in ଫାଇଲ୍_ତାଲିକା:
            if len(ଅପଲୋଡ୍_ଡାଟା) > 16384 or len(ଅପଲୋଡ୍_ନାମ.encode('utf-8')) > 63 or '\n' in ଅପଲୋଡ୍_ନାମ or '\r' in ଅପଲୋଡ୍_ନାମ:
                raise ValueError('추가 파일의 ନାମ/ଆକାର 제한 초과: ' + ଅପଲୋଡ୍_ନାମ)
            ପଠାନ୍ତୁ('load ' + shlex.quote(ଅପଲୋଡ୍_ନାମ), b'hex> ')
            for 순번 in range(0, len(ଅପଲୋଡ୍_ଡାଟା), 64): ପଠାନ୍ତୁ(ଅପଲୋଡ୍_ଡାଟା[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ପଠାନ୍ତୁ('.'): raise RuntimeError('upload failed: ' + ଅପଲୋଡ୍_ନାମ)
            갈무리자료 = ପଠାନ୍ତୁ('hex ' + shlex.quote(ଅପଲୋଡ୍_ନାମ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ଅପଲୋଡ୍_ଡାଟା: raise RuntimeError('upload verification failed')
        if ବର୍ଗ_ମୂଲ୍ୟ == '.java' and ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('javac ' + shlex.quote(ନାମ)) != 0: return 1
        실행가능파일 = ଯୁକ୍ତି_ଆରେ.file.stem + '.elf'
        if ବର୍ଗ_ମୂଲ୍ୟ == '.c' and ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('cc ' + shlex.quote(ନାମ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ଅନୁପ୍ରୟୋଗ = 'java ' + shlex.quote(ଯୁକ୍ତି_ଆରେ.class_name or ଯୁକ୍ତି_ଆରେ.file.stem) if ବର୍ଗ_ମୂଲ୍ୟ in ('.java', '.class') else ('python ' if ବର୍ଗ_ମୂଲ୍ୟ == '.py' else 'run ') + shlex.quote(ନାମ)
        if ବର୍ଗ_ମୂଲ୍ୟ == '.jar': ଅନୁପ୍ରୟୋଗ = 'java -jar ' + shlex.quote(ନାମ)
        if ବର୍ଗ_ମୂଲ୍ୟ == '.c': ଅନୁପ୍ରୟୋଗ = 'run ' + shlex.quote(실행가능파일)
        if ଯୁକ୍ତି_ଆରେ.linux: ଅନୁପ୍ରୟୋଗ = 'run --linux ' + shlex.quote(ନାମ)
        if ଯୁକ୍ତି_ଆରେ.arguments: ଅନୁପ୍ରୟୋଗ += ' ' + ' '.join(shlex.quote(ଷ୍ଟ୍ରିଂ_ଡାଟା) for ଷ୍ଟ୍ରିଂ_ଡାଟା in ଯୁକ୍ତି_ଆରେ.arguments)
        return 0 if ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ଅନୁପ୍ରୟୋଗ) == 0 else 1
    finally:
        if ପ୍ରକ୍ରିୟା.poll() is None:
            ପ୍ରକ୍ରିୟା.terminate()
            try: ପ୍ରକ୍ରିୟା.wait(timeout=5)
            except subprocess.TimeoutExpired: ପ୍ରକ୍ରିୟା.kill(); ପ୍ରକ୍ରିୟା.wait(timeout=5)
        ଚୟନକାରୀ.close(); ପ୍ରକ୍ରିୟା.stdin.close(); ପ୍ରକ୍ରିୟା.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ଚଳାନ୍ତୁ())
