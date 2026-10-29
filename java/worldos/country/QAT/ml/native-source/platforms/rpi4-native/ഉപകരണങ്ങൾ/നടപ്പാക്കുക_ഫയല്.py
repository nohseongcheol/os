#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ഹോസ്റ്റ് 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from നടപ്പാക്കുക_കമാന്_ഡ് import ആജ്ഞ


def നടപ്പിലാക്കുക():
    പാഴ്_സർ = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ.add_argument('file', type=Path)
    പാഴ്_സർ.add_argument('arguments', nargs='*')
    പാഴ്_സർ.add_argument('--class-name', help='패키지가 있는 .class의 전체 പേരു്(예: സാധൂകരിക്കുക.꾸러미시험)')
    പാഴ്_സർ.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    പാഴ്_സർ.add_argument('--vnc', help='예: 127.0.0.1:2')
    പാഴ്_സർ.add_argument('--include', action='append', type=Path, default=[], help='추가 class ഫയല് 또는 class 디렉터리(패키지 പേരു് 유지)')
    ആര്_ഗ്യുമെന്_റ്_അരേ = പാഴ്_സർ.parse_args()
    ഡാറ്റാ = ആര്_ഗ്യുമെന്_റ്_അരേ.file.read_bytes()
    if ആര്_ഗ്യുമെന്_റ്_അരേ.class_name and ആര്_ഗ്യുമെന്_റ്_അരേ.file.suffix != '.class': പാഴ്_സർ.error('--class-name은 .class 입력에서 사용합니다.')
    പേരു് = ആര്_ഗ്യുമെന്_റ്_അരേ.class_name + '.class' if ആര്_ഗ്യുമെന്_റ്_അരേ.class_name else ആര്_ഗ്യുമെന്_റ്_അരേ.file.name
    if len(ഡാറ്റാ) > 16384 or not 1 <= len(പേരു്.encode('utf-8')) <= 63 or '\n' in പേരു് or '\r' in പേരു്:
        പാഴ്_സർ.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    വകുപ്പ്_മൂല്യം = '.elf' if ഡാറ്റാ[:4] == b'\x7fELF' else ആര്_ഗ്യുമെന്_റ്_അരേ.file.suffix
    if ആര്_ഗ്യുമെന്_റ്_അരേ.linux and വകുപ്പ്_മൂല്യം != '.elf': പാഴ്_സർ.error('--linux는 ELF 바이너리에만 사용합니다.')
    if വകുപ്പ്_മൂല്യം not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        പാഴ്_സർ.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ആര്_ഗ്യുമെന്_റ്_അരേ.arguments) > 7 or any(len(സ്ട്രിംഗ്_ഡാറ്റാ.encode('utf-8')) > 255 or '\n' in സ്ട്രിംഗ്_ഡാറ്റാ or '\r' in സ്ട്രിംഗ്_ഡാറ്റാ for സ്ട്രിംഗ്_ഡാറ്റാ in ആര്_ഗ്യുമെന്_റ്_അരേ.arguments):
        പാഴ്_സർ.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ഐച്ഛികങ്ങള് = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ആര്_ഗ്യുമെന്_റ്_അരേ.vnc: ഐച്ഛികങ്ങള് += ['-vnc', ആര്_ഗ്യുമെന്_റ്_അരേ.vnc]
    പ്രക്രിയ = subprocess.Popen(ആജ്ഞ() + ഐച്ഛികങ്ങള്, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్ = selectors.DefaultSelector(); సెలక్టర్.register(പ്രക്രിയ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in సెలక్టర్.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if പ്രക്രിയ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def അയയ്ക്കുക(ലൈൻ, 확인표시=b'jkoros-native> '):
        പ്രക്രിയ.stdin.write(ലൈൻ.encode('utf-8') + b'\n'); പ്രക്രിയ.stdin.flush()
        return 수신하기(확인표시)
    def നടപ്പാക്കുക_കമാന്_ഡ്(ലൈൻ):
        출력결과 = അയയ്ക്കുക(ലൈൻ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ഫയല്_ലിസ്റ്റ് = []
        for 포함항목 in ആര്_ഗ്യുമെന്_റ്_അരേ.include:
            if 포함항목.is_dir():
                ഫയല്_ലിസ്റ്റ് += [(str(ഡാറ്റാ_പദവി.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ഡാറ്റാ_പദവി.read_bytes()) for ഡാറ്റാ_പദവി in sorted(포함항목.rglob('*.class'))]
            else:
                ഫയല്_ലിസ്റ്റ്.append((포함항목.name, 포함항목.read_bytes()))
        ഫയല്_ലിസ്റ്റ് = [(개수, ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ) for 개수, ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ in ഫയല്_ലിസ്റ്റ് if 개수 != പേരു്] + [(പേരു്, ഡാറ്റാ)]
        for അപ്_ലോഡ്_നാ_മം, അപ്_ലോഡ്_ഡാറ്റാ in ഫയല്_ലിസ്റ്റ്:
            if len(അപ്_ലോഡ്_ഡാറ്റാ) > 16384 or len(അപ്_ലോഡ്_നാ_മം.encode('utf-8')) > 63 or '\n' in അപ്_ലോഡ്_നാ_മം or '\r' in അപ്_ലോഡ്_നാ_മം:
                raise ValueError('추가 파일의 പേരു്/വലിപ്പം 제한 초과: ' + അപ്_ലോഡ്_നാ_മം)
            അയയ്ക്കുക('load ' + shlex.quote(അപ്_ലോഡ്_നാ_മം), b'hex> ')
            for 순번 in range(0, len(അപ്_ലോഡ്_ഡാറ്റാ), 64): അയയ്ക്കുക(അപ്_ലോഡ്_ഡാറ്റാ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in അയയ്ക്കുക('.'): raise RuntimeError('upload failed: ' + അപ്_ലോഡ്_നാ_മം)
            갈무리자료 = അയയ്ക്കുക('hex ' + shlex.quote(അപ്_ലോഡ്_നാ_മം))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != അപ്_ലോഡ്_ഡാറ്റാ: raise RuntimeError('upload verification failed')
        if വകുപ്പ്_മൂല്യം == '.java' and നടപ്പാക്കുക_കമാന്_ഡ്('javac ' + shlex.quote(പേരു്)) != 0: return 1
        നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ് = ആര്_ഗ്യുമെന്_റ്_അരേ.file.stem + '.elf'
        if വകുപ്പ്_മൂല്യം == '.c' and നടപ്പാക്കുക_കമാന്_ഡ്('cc ' + shlex.quote(പേരു്) + ' -o ' + shlex.quote(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്)) != 0: return 1
        പ്രോഗ്രാം = 'java ' + shlex.quote(ആര്_ഗ്യുമെന്_റ്_അരേ.class_name or ആര്_ഗ്യുമെന്_റ്_അരേ.file.stem) if വകുപ്പ്_മൂല്യം in ('.java', '.class') else ('python ' if വകുപ്പ്_മൂല്യം == '.py' else 'run ') + shlex.quote(പേരു്)
        if വകുപ്പ്_മൂല്യം == '.jar': പ്രോഗ്രാം = 'java -jar ' + shlex.quote(പേരു്)
        if വകുപ്പ്_മൂല്യം == '.c': പ്രോഗ്രാം = 'run ' + shlex.quote(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്)
        if ആര്_ഗ്യുമെന്_റ്_അരേ.linux: പ്രോഗ്രാം = 'run --linux ' + shlex.quote(പേരു്)
        if ആര്_ഗ്യുമെന്_റ്_അരേ.arguments: പ്രോഗ്രാം += ' ' + ' '.join(shlex.quote(സ്ട്രിംഗ്_ഡാറ്റാ) for സ്ട്രിംഗ്_ഡാറ്റാ in ആര്_ഗ്യുമെന്_റ്_അരേ.arguments)
        return 0 if നടപ്പാക്കുക_കമാന്_ഡ്(പ്രോഗ്രാം) == 0 else 1
    finally:
        if പ്രക്രിയ.poll() is None:
            പ്രക്രിയ.terminate()
            try: പ്രക്രിയ.wait(timeout=5)
            except subprocess.TimeoutExpired: പ്രക്രിയ.kill(); പ്രക്രിയ.wait(timeout=5)
        సెలక్టర్.close(); പ്രക്രിയ.stdin.close(); പ്രക്രിയ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(നടപ്പിലാക്കുക())
