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
from اجرا_فرمان import فرمان


def اجرا_2():
    مفسر = argparse.ArgumentParser(description=__doc__)
    مفسر.add_argument('file', type=Path)
    مفسر.add_argument('arguments', nargs='*')
    مفسر.add_argument('--class-name', help='패키지가 있는 .class의 전체 نام(예: ارزیابی_کردن.꾸러미시험)')
    مفسر.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    مفسر.add_argument('--vnc', help='예: 127.0.0.1:2')
    مفسر.add_argument('--include', action='append', type=Path, default=[], help='추가 class پرونده 또는 class 디렉터리(패키지 نام 유지)')
    آرگومان_آرايه = مفسر.parse_args()
    داده_ها = آرگومان_آرايه.file.read_bytes()
    if آرگومان_آرايه.class_name and آرگومان_آرايه.file.suffix != '.class': مفسر.error('--class-name은 .class 입력에서 사용합니다.')
    نام = آرگومان_آرايه.class_name + '.class' if آرگومان_آرايه.class_name else آرگومان_آرايه.file.name
    if len(داده_ها) > 16384 or not 1 <= len(نام.encode('utf-8')) <= 63 or '\n' in نام or '\r' in نام:
        مفسر.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    دسته_مقدار = '.elf' if داده_ها[:4] == b'\x7fELF' else آرگومان_آرايه.file.suffix
    if آرگومان_آرايه.linux and دسته_مقدار != '.elf': مفسر.error('--linux는 ELF 바이너리에만 사용합니다.')
    if دسته_مقدار not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        مفسر.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(آرگومان_آرايه.arguments) > 7 or any(len(رشته_داده_ها.encode('utf-8')) > 255 or '\n' in رشته_داده_ها or '\r' in رشته_داده_ها for رشته_داده_ها in آرگومان_آرايه.arguments):
        مفسر.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    گزینه_ها = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if آرگومان_آرايه.vnc: گزینه_ها += ['-vnc', آرگومان_آرايه.vnc]
    فرآیند = subprocess.Popen(فرمان() + گزینه_ها, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    انتخاب_کننده = selectors.DefaultSelector(); انتخاب_کننده.register(فرآیند.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); پایان_دادن_جابجایی_لایه_ای = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > پایان_دادن_جابجایی_لایه_ای: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in انتخاب_کننده.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if فرآیند.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ارسال(خط, 확인표시=b'jkoros-native> '):
        فرآیند.stdin.write(خط.encode('utf-8') + b'\n'); فرآیند.stdin.flush()
        return 수신하기(확인표시)
    def اجرا_فرمان(خط):
        출력결과 = ارسال(خط); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        فایل_لیست = []
        for 포함항목 in آرگومان_آرايه.include:
            if 포함항목.is_dir():
                فایل_لیست += [(str(داده_ها_مرتب_کردن.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', داده_ها_مرتب_کردن.read_bytes()) for داده_ها_مرتب_کردن in sorted(포함항목.rglob('*.class'))]
            else:
                فایل_لیست.append((포함항목.name, 포함항목.read_bytes()))
        فایل_لیست = [(개수, مقصد_داده_ها) for 개수, مقصد_داده_ها in فایل_لیست if 개수 != نام] + [(نام, داده_ها)]
        for آپلود_نام, آپلود_داده_ها in فایل_لیست:
            if len(آپلود_داده_ها) > 16384 or len(آپلود_نام.encode('utf-8')) > 63 or '\n' in آپلود_نام or '\r' in آپلود_نام:
                raise ValueError('추가 파일의 نام/اندازه 제한 초과: ' + آپلود_نام)
            ارسال('load ' + shlex.quote(آپلود_نام), b'hex> ')
            for 순번 in range(0, len(آپلود_داده_ها), 64): ارسال(آپلود_داده_ها[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ارسال('.'): raise RuntimeError('upload failed: ' + آپلود_نام)
            갈무리자료 = ارسال('hex ' + shlex.quote(آپلود_نام))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != آپلود_داده_ها: raise RuntimeError('upload verification failed')
        if دسته_مقدار == '.java' and اجرا_فرمان('javac ' + shlex.quote(نام)) != 0: return 1
        실행가능파일 = آرگومان_آرايه.file.stem + '.elf'
        if دسته_مقدار == '.c' and اجرا_فرمان('cc ' + shlex.quote(نام) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        برنامه = 'java ' + shlex.quote(آرگومان_آرايه.class_name or آرگومان_آرايه.file.stem) if دسته_مقدار in ('.java', '.class') else ('python ' if دسته_مقدار == '.py' else 'run ') + shlex.quote(نام)
        if دسته_مقدار == '.jar': برنامه = 'java -jar ' + shlex.quote(نام)
        if دسته_مقدار == '.c': برنامه = 'run ' + shlex.quote(실행가능파일)
        if آرگومان_آرايه.linux: برنامه = 'run --linux ' + shlex.quote(نام)
        if آرگومان_آرايه.arguments: برنامه += ' ' + ' '.join(shlex.quote(رشته_داده_ها) for رشته_داده_ها in آرگومان_آرايه.arguments)
        return 0 if اجرا_فرمان(برنامه) == 0 else 1
    finally:
        if فرآیند.poll() is None:
            فرآیند.terminate()
            try: فرآیند.wait(timeout=5)
            except subprocess.TimeoutExpired: فرآیند.kill(); فرآیند.wait(timeout=5)
        انتخاب_کننده.close(); فرآیند.stdin.close(); فرآیند.stdout.close()


if __name__ == '__main__':
    raise SystemExit(اجرا_2())
