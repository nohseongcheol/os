#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ᎠᏁᏢᏍᎩ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import ᎤᏁᏤᎸᎩ


def ᎠᎢᏎᏍᏗ():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ᏚᏙᎥᎢ(예: ᎪᎯᏳᏙᏗ.ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ᎠᏍᏆᏂᎪᏙᏗ 또는 class 디렉터리(패키지 ᏚᏙᎥᎢ 유지)')
    ᏗᏓᎦᏘᎸᏍᏗ_array = 인수해석기.parse_args()
    ᎦᏟᏌᏅᎯ = ᏗᏓᎦᏘᎸᏍᏗ_array.file.read_bytes()
    if ᏗᏓᎦᏘᎸᏍᏗ_array.class_name and ᏗᏓᎦᏘᎸᏍᏗ_array.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ᏚᏙᎥᎢ = ᏗᏓᎦᏘᎸᏍᏗ_array.class_name + '.class' if ᏗᏓᎦᏘᎸᏍᏗ_array.class_name else ᏗᏓᎦᏘᎸᏍᏗ_array.file.name
    if len(ᎦᏟᏌᏅᎯ) > 16384 or not 1 <= len(ᏚᏙᎥᎢ.encode('utf-8')) <= 63 or '\n' in ᏚᏙᎥᎢ or '\r' in ᏚᏙᎥᎢ:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ = '.elf' if ᎦᏟᏌᏅᎯ[:4] == b'\x7fELF' else ᏗᏓᎦᏘᎸᏍᏗ_array.file.suffix
    if ᏗᏓᎦᏘᎸᏍᏗ_array.linux and ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ᏗᏓᎦᏘᎸᏍᏗ_array.arguments) > 7 or any(len(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ.encode('utf-8')) > 255 or '\n' in ᎠᏍᏘ_ᎦᏟᏌᏅᎯ or '\r' in ᎠᏍᏘ_ᎦᏟᏌᏅᎯ for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in ᏗᏓᎦᏘᎸᏍᏗ_array.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ᎠᏑᏰᏍᏗᎢ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ᏗᏓᎦᏘᎸᏍᏗ_array.vnc: ᎠᏑᏰᏍᏗᎢ += ['-vnc', ᏗᏓᎦᏘᎸᏍᏗ_array.vnc]
    ᎢᏯᏛᏁᎵᏓᏍᏗ = subprocess.Popen(ᎤᏁᏤᎸᎩ() + ᎠᏑᏰᏍᏗᎢ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ᎠᏑᏰᏍᎩ = selectors.DefaultSelector(); ᎠᏑᏰᏍᎩ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); 끝위치 = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > 끝위치: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ᎠᏑᏰᏍᎩ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ᏫᎦᏅᏗ(ᏚᏓᏅᏅᎢ, 확인표시=b'jkoros-native> '):
        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᏚᏓᏅᏅᎢ.encode('utf-8') + b'\n'); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
        return 수신하기(확인표시)
    def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᏚᏓᏅᏅᎢ):
        출력결과 = ᏫᎦᏅᏗ(ᏚᏓᏅᏅᎢ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ = []
        for 포함항목 in ᏗᏓᎦᏘᎸᏍᏗ_array.include:
            if 포함항목.is_dir():
                ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ.append((포함항목.name, 포함항목.read_bytes()))
        ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ = [(개수, ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ) for 개수, ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ in ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ if 개수 != ᏚᏙᎥᎢ] + [(ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ)]
        for ᏫᏢᎦ_ᏚᏙᎥᎢ, ᏫᏢᎦ_ᎦᏟᏌᏅᎯ in ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ:
            if len(ᏫᏢᎦ_ᎦᏟᏌᏅᎯ) > 16384 or len(ᏫᏢᎦ_ᏚᏙᎥᎢ.encode('utf-8')) > 63 or '\n' in ᏫᏢᎦ_ᏚᏙᎥᎢ or '\r' in ᏫᏢᎦ_ᏚᏙᎥᎢ:
                raise ValueError('추가 파일의 ᏚᏙᎥᎢ/ᎢᎩᏓ 제한 초과: ' + ᏫᏢᎦ_ᏚᏙᎥᎢ)
            ᏫᎦᏅᏗ('load ' + shlex.quote(ᏫᏢᎦ_ᏚᏙᎥᎢ), b'hex> ')
            for 순번 in range(0, len(ᏫᏢᎦ_ᎦᏟᏌᏅᎯ), 64): ᏫᎦᏅᏗ(ᏫᏢᎦ_ᎦᏟᏌᏅᎯ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ᏫᎦᏅᏗ('.'): raise RuntimeError('upload failed: ' + ᏫᏢᎦ_ᏚᏙᎥᎢ)
            갈무리자료 = ᏫᎦᏅᏗ('hex ' + shlex.quote(ᏫᏢᎦ_ᏚᏙᎥᎢ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ᏫᏢᎦ_ᎦᏟᏌᏅᎯ: raise RuntimeError('upload verification failed')
        if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ == '.java' and ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('javac ' + shlex.quote(ᏚᏙᎥᎢ)) != 0: return 1
        실행가능파일 = ᏗᏓᎦᏘᎸᏍᏗ_array.file.stem + '.elf'
        if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ == '.c' and ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('cc ' + shlex.quote(ᏚᏙᎥᎢ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ᎬᏙᏗ = 'java ' + shlex.quote(ᏗᏓᎦᏘᎸᏍᏗ_array.class_name or ᏗᏓᎦᏘᎸᏍᏗ_array.file.stem) if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ in ('.java', '.class') else ('python ' if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ == '.py' else 'run ') + shlex.quote(ᏚᏙᎥᎢ)
        if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ == '.jar': ᎬᏙᏗ = 'java -jar ' + shlex.quote(ᏚᏙᎥᎢ)
        if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ == '.c': ᎬᏙᏗ = 'run ' + shlex.quote(실행가능파일)
        if ᏗᏓᎦᏘᎸᏍᏗ_array.linux: ᎬᏙᏗ = 'run --linux ' + shlex.quote(ᏚᏙᎥᎢ)
        if ᏗᏓᎦᏘᎸᏍᏗ_array.arguments: ᎬᏙᏗ += ' ' + ' '.join(shlex.quote(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ) for ᎠᏍᏘ_ᎦᏟᏌᏅᎯ in ᏗᏓᎦᏘᎸᏍᏗ_array.arguments)
        return 0 if ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎬᏙᏗ) == 0 else 1
    finally:
        if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
            try: ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
            except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
        ᎠᏑᏰᏍᎩ.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ᎠᎢᏎᏍᏗ())
