#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ධාරකය 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ක්_රියාත්මක_කරන්න_විධානය import විධානය


def ක්_රියාත්මක_කරන්න_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 නම(예: වලංගු_කරන්න.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ගොනු 또는 class 디렉터리(패키지 නම 유지)')
    විස්තාරකය_ආරා_ව = 인수해석기.parse_args()
    දත්ත = විස්තාරකය_ආරා_ව.file.read_bytes()
    if විස්තාරකය_ආරා_ව.class_name and විස්තාරකය_ආරා_ව.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    නම = විස්තාරකය_ආරා_ව.class_name + '.class' if විස්තාරකය_ආරා_ව.class_name else විස්තාරකය_ආරා_ව.file.name
    if len(දත්ත) > 16384 or not 1 <= len(නම.encode('utf-8')) <= 63 or '\n' in නම or '\r' in නම:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ප්_රවර්ගය_අගය = '.elf' if දත්ත[:4] == b'\x7fELF' else විස්තාරකය_ආරා_ව.file.suffix
    if විස්තාරකය_ආරා_ව.linux and ප්_රවර්ගය_අගය != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ප්_රවර්ගය_අගය not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(විස්තාරකය_ආරා_ව.arguments) > 7 or any(len(අනුලකුණු_වැල_දත්ත.encode('utf-8')) > 255 or '\n' in අනුලකුණු_වැල_දත්ත or '\r' in අනුලකුණු_වැල_දත්ත for අනුලකුණු_වැල_දත්ත in විස්තාරකය_ආරා_ව.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    අභිරුචි = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if විස්තාරකය_ආරා_ව.vnc: අභිරුචි += ['-vnc', විස්තාරකය_ආරා_ව.vnc]
    සැකසුම = subprocess.Popen(විධානය() + අභිරුචි, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    වරකය = selectors.DefaultSelector(); වරකය.register(සැකසුම.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); නිමා_කරන්න_ඕෆ්සෙට් = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > නිමා_කරන්න_ඕෆ්සෙට්: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in වරකය.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if සැකසුම.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ඊමේල්(පේළිය, 확인표시=b'jkoros-native> '):
        සැකසුම.stdin.write(පේළිය.encode('utf-8') + b'\n'); සැකසුම.stdin.flush()
        return 수신하기(확인표시)
    def ක්_රියාත්මක_කරන්න_විධානය(පේළිය):
        출력결과 = ඊමේල්(පේළිය); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ගොනුව_ලැයිස්තුව = []
        for 포함항목 in විස්තාරකය_ආරා_ව.include:
            if 포함항목.is_dir():
                ගොනුව_ලැයිස්තුව += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                ගොනුව_ලැයිස්තුව.append((포함항목.name, 포함항목.read_bytes()))
        ගොනුව_ලැයිස්තුව = [(개수, ගමනාන්තය_දත්ත) for 개수, ගමනාන්තය_දත්ත in ගොනුව_ලැයිස්තුව if 개수 != නම] + [(නම, දත්ත)]
        for උඩුගත_කරන්න_නම, උඩුගත_කරන්න_දත්ත in ගොනුව_ලැයිස්තුව:
            if len(උඩුගත_කරන්න_දත්ත) > 16384 or len(උඩුගත_කරන්න_නම.encode('utf-8')) > 63 or '\n' in උඩුගත_කරන්න_නම or '\r' in උඩුගත_කරන්න_නම:
                raise ValueError('추가 파일의 නම/ප්_රමාණය 제한 초과: ' + උඩුගත_කරන්න_නම)
            ඊමේල්('load ' + shlex.quote(උඩුගත_කරන්න_නම), b'hex> ')
            for 순번 in range(0, len(උඩුගත_කරන්න_දත්ත), 64): ඊමේල්(උඩුගත_කරන්න_දත්ත[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ඊමේල්('.'): raise RuntimeError('upload failed: ' + උඩුගත_කරන්න_නම)
            갈무리자료 = ඊමේල්('hex ' + shlex.quote(උඩුගත_කරන්න_නම))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != උඩුගත_කරන්න_දත්ත: raise RuntimeError('upload verification failed')
        if ප්_රවර්ගය_අගය == '.java' and ක්_රියාත්මක_කරන්න_විධානය('javac ' + shlex.quote(නම)) != 0: return 1
        실행가능파일 = විස්තාරකය_ආරා_ව.file.stem + '.elf'
        if ප්_රවර්ගය_අගය == '.c' and ක්_රියාත්මක_කරන්න_විධානය('cc ' + shlex.quote(නම) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        යෙදු = 'java ' + shlex.quote(විස්තාරකය_ආරා_ව.class_name or විස්තාරකය_ආරා_ව.file.stem) if ප්_රවර්ගය_අගය in ('.java', '.class') else ('python ' if ප්_රවර්ගය_අගය == '.py' else 'run ') + shlex.quote(නම)
        if ප්_රවර්ගය_අගය == '.jar': යෙදු = 'java -jar ' + shlex.quote(නම)
        if ප්_රවර්ගය_අගය == '.c': යෙදු = 'run ' + shlex.quote(실행가능파일)
        if විස්තාරකය_ආරා_ව.linux: යෙදු = 'run --linux ' + shlex.quote(නම)
        if විස්තාරකය_ආරා_ව.arguments: යෙදු += ' ' + ' '.join(shlex.quote(අනුලකුණු_වැල_දත්ත) for අනුලකුණු_වැල_දත්ත in විස්තාරකය_ආරා_ව.arguments)
        return 0 if ක්_රියාත්මක_කරන්න_විධානය(යෙදු) == 0 else 1
    finally:
        if සැකසුම.poll() is None:
            සැකසුම.terminate()
            try: සැකසුම.wait(timeout=5)
            except subprocess.TimeoutExpired: සැකසුම.kill(); සැකසුම.wait(timeout=5)
        වරකය.close(); සැකසුම.stdin.close(); සැකසුම.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ක්_රියාත්මක_කරන්න_2())
