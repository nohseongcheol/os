#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. მასპინძელი 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from შესრულება_ბრძანება import ბრძანება


def გაშვება():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 სახელი(예: შემოწმება.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ფაილი 또는 class 디렉터리(패키지 სახელი 유지)')
    არგუმენტი_მასივი = 인수해석기.parse_args()
    მონაცემები = არგუმენტი_მასივი.file.read_bytes()
    if არგუმენტი_მასივი.class_name and არგუმენტი_მასივი.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    სახელი = არგუმენტი_მასივი.class_name + '.class' if არგუმენტი_მასივი.class_name else არგუმენტი_მასივი.file.name
    if len(მონაცემები) > 16384 or not 1 <= len(სახელი.encode('utf-8')) <= 63 or '\n' in სახელი or '\r' in სახელი:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    კატეგორია_მნიშვნელობა = '.elf' if მონაცემები[:4] == b'\x7fELF' else არგუმენტი_მასივი.file.suffix
    if არგუმენტი_მასივი.linux and კატეგორია_მნიშვნელობა != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if კატეგორია_მნიშვნელობა not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(არგუმენტი_მასივი.arguments) > 7 or any(len(სტრიქონი_მონაცემები.encode('utf-8')) > 255 or '\n' in სტრიქონი_მონაცემები or '\r' in სტრიქონი_მონაცემები for სტრიქონი_მონაცემები in არგუმენტი_მასივი.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ვარიანტები = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if არგუმენტი_მასივი.vnc: ვარიანტები += ['-vnc', არგუმენტი_მასივი.vnc]
    პროცესი = subprocess.Popen(ბრძანება() + ვარიანტები, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    სელექტორი = selectors.DefaultSelector(); სელექტორი.register(პროცესი.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); დასასრული_ოფსეტი = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > დასასრული_ოფსეტი: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in სელექტორი.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if პროცესი.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def გაგზავნა(ხაზი, 확인표시=b'jkoros-native> '):
        პროცესი.stdin.write(ხაზი.encode('utf-8') + b'\n'); პროცესი.stdin.flush()
        return 수신하기(확인표시)
    def შესრულება_ბრძანება(ხაზი):
        출력결과 = გაგზავნა(ხაზი); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ფაილი_სია = []
        for 포함항목 in არგუმენტი_მასივი.include:
            if 포함항목.is_dir():
                ფაილი_სია += [(str(მონაცემები_პოზიცია.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', მონაცემები_პოზიცია.read_bytes()) for მონაცემები_პოზიცია in sorted(포함항목.rglob('*.class'))]
            else:
                ფაილი_სია.append((포함항목.name, 포함항목.read_bytes()))
        ფაილი_სია = [(개수, მიმართულება_მონაცემები) for 개수, მიმართულება_მონაცემები in ფაილი_სია if 개수 != სახელი] + [(სახელი, მონაცემები)]
        for ატვირთვა_სახელი, ატვირთვა_მონაცემები in ფაილი_სია:
            if len(ატვირთვა_მონაცემები) > 16384 or len(ატვირთვა_სახელი.encode('utf-8')) > 63 or '\n' in ატვირთვა_სახელი or '\r' in ატვირთვა_სახელი:
                raise ValueError('추가 파일의 სახელი/ზომა 제한 초과: ' + ატვირთვა_სახელი)
            გაგზავნა('load ' + shlex.quote(ატვირთვა_სახელი), b'hex> ')
            for 순번 in range(0, len(ატვირთვა_მონაცემები), 64): გაგზავნა(ატვირთვა_მონაცემები[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in გაგზავნა('.'): raise RuntimeError('upload failed: ' + ატვირთვა_სახელი)
            갈무리자료 = გაგზავნა('hex ' + shlex.quote(ატვირთვა_სახელი))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ატვირთვა_მონაცემები: raise RuntimeError('upload verification failed')
        if კატეგორია_მნიშვნელობა == '.java' and შესრულება_ბრძანება('javac ' + shlex.quote(სახელი)) != 0: return 1
        실행가능파일 = არგუმენტი_მასივი.file.stem + '.elf'
        if კატეგორია_მნიშვნელობა == '.c' and შესრულება_ბრძანება('cc ' + shlex.quote(სახელი) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        აპი = 'java ' + shlex.quote(არგუმენტი_მასივი.class_name or არგუმენტი_მასივი.file.stem) if კატეგორია_მნიშვნელობა in ('.java', '.class') else ('python ' if კატეგორია_მნიშვნელობა == '.py' else 'run ') + shlex.quote(სახელი)
        if კატეგორია_მნიშვნელობა == '.jar': აპი = 'java -jar ' + shlex.quote(სახელი)
        if კატეგორია_მნიშვნელობა == '.c': აპი = 'run ' + shlex.quote(실행가능파일)
        if არგუმენტი_მასივი.linux: აპი = 'run --linux ' + shlex.quote(სახელი)
        if არგუმენტი_მასივი.arguments: აპი += ' ' + ' '.join(shlex.quote(სტრიქონი_მონაცემები) for სტრიქონი_მონაცემები in არგუმენტი_მასივი.arguments)
        return 0 if შესრულება_ბრძანება(აპი) == 0 else 1
    finally:
        if პროცესი.poll() is None:
            პროცესი.terminate()
            try: პროცესი.wait(timeout=5)
            except subprocess.TimeoutExpired: პროცესი.kill(); პროცესი.wait(timeout=5)
        სელექტორი.close(); პროცესი.stdin.close(); პროცესი.stdout.close()


if __name__ == '__main__':
    raise SystemExit(გაშვება())
