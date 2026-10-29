#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. مضيف 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ينفذ_أمر import أمر


def تشغيل():
    المحلل = argparse.ArgumentParser(description=__doc__)
    المحلل.add_argument('file', type=Path)
    المحلل.add_argument('arguments', nargs='*')
    المحلل.add_argument('--class-name', help='패키지가 있는 .class의 전체 اسم(예: التحقق_من_صحة.يختبر_يُجمع)')
    المحلل.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI يستخدم_قيمة')
    المحلل.add_argument('--vnc', help='예: 127.0.0.1:2')
    المحلل.add_argument('--include', action='append', type=Path, default=[], help='إلحاق_إدخال class ملف 또는 class 디렉터리(패키지 اسم 유지)')
    وسيطة_صفيف = المحلل.parse_args()
    بيانات = وسيطة_صفيف.file.read_bytes()
    if وسيطة_صفيف.class_name and وسيطة_صفيف.file.suffix != '.class': المحلل.error('--class-name은 .class 입력에서 사용합니다.')
    اسم = وسيطة_صفيف.class_name + '.class' if وسيطة_صفيف.class_name else وسيطة_صفيف.file.name
    if len(بيانات) > 16384 or not 1 <= len(اسم.encode('utf-8')) <= 63 or '\n' in اسم or '\r' in اسم:
        المحلل.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    فئة_قيمة = '.elf' if بيانات[:4] == b'\x7fELF' else وسيطة_صفيف.file.suffix
    if وسيطة_صفيف.linux and فئة_قيمة != '.elf': المحلل.error('--linux는 ELF 바이너리에만 사용합니다.')
    if فئة_قيمة not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        المحلل.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(وسيطة_صفيف.arguments) > 7 or any(len(سلسلة_بيانات.encode('utf-8')) > 255 or '\n' in سلسلة_بيانات or '\r' in سلسلة_بيانات for سلسلة_بيانات in وسيطة_صفيف.arguments):
        المحلل.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    خيارات = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if وسيطة_صفيف.vnc: خيارات += ['-vnc', وسيطة_صفيف.vnc]
    عملية = subprocess.Popen(أمر() + خيارات, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    محدد = selectors.DefaultSelector(); محدد.register(عملية.stdout, selectors.EVENT_READ)
    def يستلم_رسالة(علامة, 시간제한=45):
        الناتج = bytearray(); إنهاء_مكالمة_إزاحة = time.monotonic() + 시간제한
        while علامة not in الناتج:
            if time.monotonic() > إنهاء_مكالمة_إزاحة: raise RuntimeError('UART timeout: ' + الناتج.decode('utf-8', 'replace'))
            for 누름값, _ in محدد.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: الناتج.extend(조각)
            if b'PANIC:' in الناتج or b'FAIL ' in الناتج: raise RuntimeError(الناتج.decode('utf-8', 'replace'))
            if عملية.poll() is not None: raise RuntimeError('QEMU exited: ' + الناتج.decode('utf-8', 'replace'))
        return bytes(الناتج)
    def يرسل(سطر, علامة=b'jkoros-native> '):
        عملية.stdin.write(سطر.encode('utf-8') + b'\n'); عملية.stdin.flush()
        return يستلم_رسالة(علامة)
    def ينفذ_أمر(سطر):
        الناتج = يرسل(سطر); sys.stdout.buffer.write(الناتج); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', الناتج)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        يستلم_رسالة(b'jkoros-native> ')
        ملف_قائمة = []
        for 포함항목 in وسيطة_صفيف.include:
            if 포함항목.is_dir():
                ملف_قائمة += [(str(بيانات_منصب.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', بيانات_منصب.read_bytes()) for بيانات_منصب in sorted(포함항목.rglob('*.class'))]
            else:
                ملف_قائمة.append((포함항목.name, 포함항목.read_bytes()))
        ملف_قائمة = [(개수, وجهة_بيانات) for 개수, وجهة_بيانات in ملف_قائمة if 개수 != اسم] + [(اسم, بيانات)]
        for تحميل_اسم, تحميل_بيانات in ملف_قائمة:
            if len(تحميل_بيانات) > 16384 or len(تحميل_اسم.encode('utf-8')) > 63 or '\n' in تحميل_اسم or '\r' in تحميل_اسم:
                raise ValueError('إلحاق_إدخال 파일의 اسم/حجم 제한 초과: ' + تحميل_اسم)
            يرسل('load ' + shlex.quote(تحميل_اسم), b'hex> ')
            for 순번 in range(0, len(تحميل_بيانات), 64): يرسل(تحميل_بيانات[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in يرسل('.'): raise RuntimeError('upload failed: ' + تحميل_اسم)
            갈무리자료 = يرسل('hex ' + shlex.quote(تحميل_اسم))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != تحميل_بيانات: raise RuntimeError('upload verification failed')
        if فئة_قيمة == '.java' and ينفذ_أمر('javac ' + shlex.quote(اسم)) != 0: return 1
        실행가능파일 = وسيطة_صفيف.file.stem + '.elf'
        if فئة_قيمة == '.c' and ينفذ_أمر('cc ' + shlex.quote(اسم) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        تطبيق = 'java ' + shlex.quote(وسيطة_صفيف.class_name or وسيطة_صفيف.file.stem) if فئة_قيمة in ('.java', '.class') else ('python ' if فئة_قيمة == '.py' else 'run ') + shlex.quote(اسم)
        if فئة_قيمة == '.jar': تطبيق = 'java -jar ' + shlex.quote(اسم)
        if فئة_قيمة == '.c': تطبيق = 'run ' + shlex.quote(실행가능파일)
        if وسيطة_صفيف.linux: تطبيق = 'run --linux ' + shlex.quote(اسم)
        if وسيطة_صفيف.arguments: تطبيق += ' ' + ' '.join(shlex.quote(سلسلة_بيانات) for سلسلة_بيانات in وسيطة_صفيف.arguments)
        return 0 if ينفذ_أمر(تطبيق) == 0 else 1
    finally:
        if عملية.poll() is None:
            عملية.terminate()
            try: عملية.wait(timeout=5)
            except subprocess.TimeoutExpired: عملية.kill(); عملية.wait(timeout=5)
        محدد.close(); عملية.stdin.close(); عملية.stdout.close()


if __name__ == '__main__':
    raise SystemExit(تشغيل())
