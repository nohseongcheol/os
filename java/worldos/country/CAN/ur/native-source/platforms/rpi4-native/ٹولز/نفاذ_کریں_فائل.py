#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. میزبان 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from نفاذ_کریں_حکم import حکم


def چلائیں():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 نام(예: جواز_دہی_کریں.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class فائل_کا_نام 또는 class 디렉터리(패키지 نام 유지)')
    دلائل_لڑی = 인수해석기.parse_args()
    کوائف = دلائل_لڑی.file.read_bytes()
    if دلائل_لڑی.class_name and دلائل_لڑی.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    نام = دلائل_لڑی.class_name + '.class' if دلائل_لڑی.class_name else دلائل_لڑی.file.name
    if len(کوائف) > 16384 or not 1 <= len(نام.encode('utf-8')) <= 63 or '\n' in نام or '\r' in نام:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    زمرہ_قدر = '.elf' if کوائف[:4] == b'\x7fELF' else دلائل_لڑی.file.suffix
    if دلائل_لڑی.linux and زمرہ_قدر != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if زمرہ_قدر not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(دلائل_لڑی.arguments) > 7 or any(len(سلک_کوائف.encode('utf-8')) > 255 or '\n' in سلک_کوائف or '\r' in سلک_کوائف for سلک_کوائف in دلائل_لڑی.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    اختیارات = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if دلائل_لڑی.vnc: اختیارات += ['-vnc', دلائل_لڑی.vnc]
    عمل_کاری = subprocess.Popen(حکم() + اختیارات, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    منتخب_کنندہ = selectors.DefaultSelector(); منتخب_کنندہ.register(عمل_کاری.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); اختتام_آفسٹ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > اختتام_آفسٹ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in منتخب_کنندہ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if عمل_کاری.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def بھیجیں(اندراج_کی_سطر, 확인표시=b'jkoros-native> '):
        عمل_کاری.stdin.write(اندراج_کی_سطر.encode('utf-8') + b'\n'); عمل_کاری.stdin.flush()
        return 수신하기(확인표시)
    def نفاذ_کریں_حکم(اندراج_کی_سطر):
        출력결과 = بھیجیں(اندراج_کی_سطر); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        فائل_فہرست = []
        for 포함항목 in دلائل_لڑی.include:
            if 포함항목.is_dir():
                فائل_فہرست += [(str(کوائف_پوزیشن_ٹھیک_کریں.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', کوائف_پوزیشن_ٹھیک_کریں.read_bytes()) for کوائف_پوزیشن_ٹھیک_کریں in sorted(포함항목.rglob('*.class'))]
            else:
                فائل_فہرست.append((포함항목.name, 포함항목.read_bytes()))
        فائل_فہرست = [(개수, منزل_مقصود_کوائف) for 개수, منزل_مقصود_کوائف in فائل_فہرست if 개수 != نام] + [(نام, کوائف)]
        for اپ_لوڈ_کريں_نام, اپ_لوڈ_کريں_کوائف in فائل_فہرست:
            if len(اپ_لوڈ_کريں_کوائف) > 16384 or len(اپ_لوڈ_کريں_نام.encode('utf-8')) > 63 or '\n' in اپ_لوڈ_کريں_نام or '\r' in اپ_لوڈ_کريں_نام:
                raise ValueError('추가 파일의 نام/حجم 제한 초과: ' + اپ_لوڈ_کريں_نام)
            بھیجیں('load ' + shlex.quote(اپ_لوڈ_کريں_نام), b'hex> ')
            for 순번 in range(0, len(اپ_لوڈ_کريں_کوائف), 64): بھیجیں(اپ_لوڈ_کريں_کوائف[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in بھیجیں('.'): raise RuntimeError('upload failed: ' + اپ_لوڈ_کريں_نام)
            갈무리자료 = بھیجیں('hex ' + shlex.quote(اپ_لوڈ_کريں_نام))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != اپ_لوڈ_کريں_کوائف: raise RuntimeError('upload verification failed')
        if زمرہ_قدر == '.java' and نفاذ_کریں_حکم('javac ' + shlex.quote(نام)) != 0: return 1
        실행가능파일 = دلائل_لڑی.file.stem + '.elf'
        if زمرہ_قدر == '.c' and نفاذ_کریں_حکم('cc ' + shlex.quote(نام) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ایپ = 'java ' + shlex.quote(دلائل_لڑی.class_name or دلائل_لڑی.file.stem) if زمرہ_قدر in ('.java', '.class') else ('python ' if زمرہ_قدر == '.py' else 'run ') + shlex.quote(نام)
        if زمرہ_قدر == '.jar': ایپ = 'java -jar ' + shlex.quote(نام)
        if زمرہ_قدر == '.c': ایپ = 'run ' + shlex.quote(실행가능파일)
        if دلائل_لڑی.linux: ایپ = 'run --linux ' + shlex.quote(نام)
        if دلائل_لڑی.arguments: ایپ += ' ' + ' '.join(shlex.quote(سلک_کوائف) for سلک_کوائف in دلائل_لڑی.arguments)
        return 0 if نفاذ_کریں_حکم(ایپ) == 0 else 1
    finally:
        if عمل_کاری.poll() is None:
            عمل_کاری.terminate()
            try: عمل_کاری.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل_کاری.kill(); عمل_کاری.wait(timeout=5)
        منتخب_کنندہ.close(); عمل_کاری.stdin.close(); عمل_کاری.stdout.close()


if __name__ == '__main__':
    raise SystemExit(چلائیں())
