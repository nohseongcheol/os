#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ஓம்பு 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from இயக்கு_கட்டளை import கட்டளை


def செயல்படுத்துக():
    பார்சர் = argparse.ArgumentParser(description=__doc__)
    பார்சர்.add_argument('file', type=Path)
    பார்சர்.add_argument('arguments', nargs='*')
    பார்சர்.add_argument('--class-name', help='패키지가 있는 .class의 전체 பெயர்(예: சரிபார்_5fb2b747.꾸러미시험)')
    பார்சர்.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    பார்சர்.add_argument('--vnc', help='예: 127.0.0.1:2')
    பார்சர்.add_argument('--include', action='append', type=Path, default=[], help='추가 class கோப்பின்_பெயர் 또는 class 디렉터리(패키지 பெயர் 유지)')
    மதிப்புரு_கோவை = பார்சர்.parse_args()
    தரவு = மதிப்புரு_கோவை.file.read_bytes()
    if மதிப்புரு_கோவை.class_name and மதிப்புரு_கோவை.file.suffix != '.class': பார்சர்.error('--class-name은 .class 입력에서 사용합니다.')
    பெயர் = மதிப்புரு_கோவை.class_name + '.class' if மதிப்புரு_கோவை.class_name else மதிப்புரு_கோவை.file.name
    if len(தரவு) > 16384 or not 1 <= len(பெயர்.encode('utf-8')) <= 63 or '\n' in பெயர் or '\r' in பெயர்:
        பார்சர்.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    வகை_மதிப்பு_4b6d6445 = '.elf' if தரவு[:4] == b'\x7fELF' else மதிப்புரு_கோவை.file.suffix
    if மதிப்புரு_கோவை.linux and வகை_மதிப்பு_4b6d6445 != '.elf': பார்சர்.error('--linux는 ELF 바이너리에만 사용합니다.')
    if வகை_மதிப்பு_4b6d6445 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        பார்சர்.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(மதிப்புரு_கோவை.arguments) > 7 or any(len(சரம்_தரவு.encode('utf-8')) > 255 or '\n' in சரம்_தரவு or '\r' in சரம்_தரவு for சரம்_தரவு in மதிப்புரு_கோவை.arguments):
        பார்சர்.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    விருப்பங்கள் = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if மதிப்புரு_கோவை.vnc: விருப்பங்கள் += ['-vnc', மதிப்புரு_கோவை.vnc]
    செயல்பாடு = subprocess.Popen(கட்டளை() + விருப்பங்கள், stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    தேர்வி = selectors.DefaultSelector(); தேர்வி.register(செயல்பாடு.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); முடி_ஆஃப்செட் = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > முடி_ஆஃப்செட்: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in தேர்வி.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if செயல்பாடு.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def அனுப்பு(உள்ளீட்டு_வரி, 확인표시=b'jkoros-native> '):
        செயல்பாடு.stdin.write(உள்ளீட்டு_வரி.encode('utf-8') + b'\n'); செயல்பாடு.stdin.flush()
        return 수신하기(확인표시)
    def இயக்கு_கட்டளை(உள்ளீட்டு_வரி):
        출력결과 = அனுப்பு(உள்ளீட்டு_வரி); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        கோப்பு_பட்டியல் = []
        for 포함항목 in மதிப்புரு_கோவை.include:
            if 포함항목.is_dir():
                கோப்பு_பட்டியல் += [(str(தரவு_நிலை.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', தரவு_நிலை.read_bytes()) for தரவு_நிலை in sorted(포함항목.rglob('*.class'))]
            else:
                கோப்பு_பட்டியல்.append((포함항목.name, 포함항목.read_bytes()))
        கோப்பு_பட்டியல் = [(개수, இலக்கு_தரவு) for 개수, இலக்கு_தரவு in கோப்பு_பட்டியல் if 개수 != பெயர்] + [(பெயர், தரவு)]
        for பதிவேற்று_பெயர், பதிவேற்று_தரவு in கோப்பு_பட்டியல்:
            if len(பதிவேற்று_தரவு) > 16384 or len(பதிவேற்று_பெயர்.encode('utf-8')) > 63 or '\n' in பதிவேற்று_பெயர் or '\r' in பதிவேற்று_பெயர்:
                raise ValueError('추가 파일의 பெயர்/அளவு 제한 초과: ' + பதிவேற்று_பெயர்)
            அனுப்பு('load ' + shlex.quote(பதிவேற்று_பெயர்), b'hex> ')
            for 순번 in range(0, len(பதிவேற்று_தரவு), 64): அனுப்பு(பதிவேற்று_தரவு[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in அனுப்பு('.'): raise RuntimeError('upload failed: ' + பதிவேற்று_பெயர்)
            갈무리자료 = அனுப்பு('hex ' + shlex.quote(பதிவேற்று_பெயர்))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != பதிவேற்று_தரவு: raise RuntimeError('upload verification failed')
        if வகை_மதிப்பு_4b6d6445 == '.java' and இயக்கு_கட்டளை('javac ' + shlex.quote(பெயர்)) != 0: return 1
        செயல்படுத்தக்கூடிய_கோப்பு_படம் = மதிப்புரு_கோவை.file.stem + '.elf'
        if வகை_மதிப்பு_4b6d6445 == '.c' and இயக்கு_கட்டளை('cc ' + shlex.quote(பெயர்) + ' -o ' + shlex.quote(செயல்படுத்தக்கூடிய_கோப்பு_படம்)) != 0: return 1
        நிரல் = 'java ' + shlex.quote(மதிப்புரு_கோவை.class_name or மதிப்புரு_கோவை.file.stem) if வகை_மதிப்பு_4b6d6445 in ('.java', '.class') else ('python ' if வகை_மதிப்பு_4b6d6445 == '.py' else 'run ') + shlex.quote(பெயர்)
        if வகை_மதிப்பு_4b6d6445 == '.jar': நிரல் = 'java -jar ' + shlex.quote(பெயர்)
        if வகை_மதிப்பு_4b6d6445 == '.c': நிரல் = 'run ' + shlex.quote(செயல்படுத்தக்கூடிய_கோப்பு_படம்)
        if மதிப்புரு_கோவை.linux: நிரல் = 'run --linux ' + shlex.quote(பெயர்)
        if மதிப்புரு_கோவை.arguments: நிரல் += ' ' + ' '.join(shlex.quote(சரம்_தரவு) for சரம்_தரவு in மதிப்புரு_கோவை.arguments)
        return 0 if இயக்கு_கட்டளை(நிரல்) == 0 else 1
    finally:
        if செயல்பாடு.poll() is None:
            செயல்பாடு.terminate()
            try: செயல்பாடு.wait(timeout=5)
            except subprocess.TimeoutExpired: செயல்பாடு.kill(); செயல்பாடு.wait(timeout=5)
        தேர்வி.close(); செயல்பாடு.stdin.close(); செயல்பாடு.stdout.close()


if __name__ == '__main__':
    raise SystemExit(செயல்படுத்துக())
