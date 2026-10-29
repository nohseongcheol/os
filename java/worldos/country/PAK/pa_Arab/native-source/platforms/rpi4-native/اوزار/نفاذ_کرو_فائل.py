#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. مہمان_b78e430d 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from نفاذ_کرو_حکم import حکم


def چلاؤ():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ناں(예: تریخ_دے_مطابق_کرو.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class فائل 또는 class 디렉터리(패키지 ناں 유지)')
    دلیل_ایرے = 인수해석기.parse_args()
    کوائف = دلیل_ایرے.file.read_bytes()
    if دلیل_ایرے.class_name and دلیل_ایرے.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ناں = دلیل_ایرے.class_name + '.class' if دلیل_ایرے.class_name else دلیل_ایرے.file.name
    if len(کوائف) > 16384 or not 1 <= len(ناں.encode('utf-8')) <= 63 or '\n' in ناں or '\r' in ناں:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    زمرہ_قدر = '.elf' if کوائف[:4] == b'\x7fELF' else دلیل_ایرے.file.suffix
    if دلیل_ایرے.linux and زمرہ_قدر != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if زمرہ_قدر not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(دلیل_ایرے.arguments) > 7 or any(len(سٹرنگ_کوائف.encode('utf-8')) > 255 or '\n' in سٹرنگ_کوائف or '\r' in سٹرنگ_کوائف for سٹرنگ_کوائف in دلیل_ایرے.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    اختیار = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if دلیل_ایرے.vnc: اختیار += ['-vnc', دلیل_ایرے.vnc]
    عمل = subprocess.Popen(حکم() + اختیار, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کرنڑ_آلا = selectors.DefaultSelector(); منتخب_کرنڑ_آلا.register(عمل.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ختم_کرو_آف_سیٹ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ختم_کرو_آف_سیٹ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in منتخب_کرنڑ_آلا.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if عمل.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def بھیجو(لائن, 확인표시=b'jkoros-native> '):
        عمل.stdin.write(لائن.encode('utf-8') + b'\n'); عمل.stdin.flush()
        return 수신하기(확인표시)
    def نفاذ_کرو_حکم(لائن):
        출력결과 = بھیجو(لائن); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        فائل_فرست = []
        for 포함항목 in دلیل_ایرے.include:
            if 포함항목.is_dir():
                فائل_فرست += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                فائل_فرست.append((포함항목.name, 포함항목.read_bytes()))
        فائل_فرست = [(개수, منزل_مقصود_کوائف) for 개수, منزل_مقصود_کوائف in فائل_فرست if 개수 != ناں] + [(ناں, کوائف)]
        for اپ_لوڈ_کرو_ناں, اپ_لوڈ_کرو_کوائف in فائل_فرست:
            if len(اپ_لوڈ_کرو_کوائف) > 16384 or len(اپ_لوڈ_کرو_ناں.encode('utf-8')) > 63 or '\n' in اپ_لوڈ_کرو_ناں or '\r' in اپ_لوڈ_کرو_ناں:
                raise ValueError('추가 파일의 ناں/سائز 제한 초과: ' + اپ_لوڈ_کرو_ناں)
            بھیجو('load ' + shlex.quote(اپ_لوڈ_کرو_ناں), b'hex> ')
            for 순번 in range(0, len(اپ_لوڈ_کرو_کوائف), 64): بھیجو(اپ_لوڈ_کرو_کوائف[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in بھیجو('.'): raise RuntimeError('upload failed: ' + اپ_لوڈ_کرو_ناں)
            갈무리자료 = بھیجو('hex ' + shlex.quote(اپ_لوڈ_کرو_ناں))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != اپ_لوڈ_کرو_کوائف: raise RuntimeError('upload verification failed')
        if زمرہ_قدر == '.java' and نفاذ_کرو_حکم('javac ' + shlex.quote(ناں)) != 0: return 1
        실행가능파일 = دلیل_ایرے.file.stem + '.elf'
        if زمرہ_قدر == '.c' and نفاذ_کرو_حکم('cc ' + shlex.quote(ناں) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ایپ = 'java ' + shlex.quote(دلیل_ایرے.class_name or دلیل_ایرے.file.stem) if زمرہ_قدر in ('.java', '.class') else ('python ' if زمرہ_قدر == '.py' else 'run ') + shlex.quote(ناں)
        if زمرہ_قدر == '.jar': ایپ = 'java -jar ' + shlex.quote(ناں)
        if زمرہ_قدر == '.c': ایپ = 'run ' + shlex.quote(실행가능파일)
        if دلیل_ایرے.linux: ایپ = 'run --linux ' + shlex.quote(ناں)
        if دلیل_ایرے.arguments: ایپ += ' ' + ' '.join(shlex.quote(سٹرنگ_کوائف) for سٹرنگ_کوائف in دلیل_ایرے.arguments)
        return 0 if نفاذ_کرو_حکم(ایپ) == 0 else 1
    finally:
        if عمل.poll() is None:
            عمل.terminate()
            try: عمل.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل.kill(); عمل.wait(timeout=5)
        منتخب_کرنڑ_آلا.close(); عمل.stdin.close(); عمل.stdout.close()


if __name__ == '__main__':
    raise SystemExit(چلاؤ())
