#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. host 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Mag_execute_utos import utos


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('arguments', nargs='*')
    parser.add_argument('--class-name', help='패키지가 있는 .class의 전체 pangalan(예: patunayan.꾸러미시험)')
    parser.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    parser.add_argument('--vnc', help='예: 127.0.0.1:2')
    parser.add_argument('--include', action='append', type=Path, default=[], help='추가 class file 또는 class 디렉터리(패키지 pangalan 유지)')
    argumento_ARRAY = parser.parse_args()
    data = argumento_ARRAY.file.read_bytes()
    if argumento_ARRAY.class_name and argumento_ARRAY.file.suffix != '.class': parser.error('--class-name은 .class 입력에서 사용합니다.')
    pangalan = argumento_ARRAY.class_name + '.class' if argumento_ARRAY.class_name else argumento_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(pangalan.encode('utf-8')) <= 63 or '\n' in pangalan or '\r' in pangalan:
        parser.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategorya_VALUE = '.elf' if data[:4] == b'\x7fELF' else argumento_ARRAY.file.suffix
    if argumento_ARRAY.linux and kategorya_VALUE != '.elf': parser.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategorya_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        parser.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argumento_ARRAY.arguments) > 7 or any(len(string_data.encode('utf-8')) > 255 or '\n' in string_data or '\r' in string_data for string_data in argumento_ARRAY.arguments):
        parser.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Mga_Opsyon = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argumento_ARRAY.vnc: Mga_Opsyon += ['-vnc', argumento_ARRAY.vnc]
    Proseso = subprocess.Popen(utos() + Mga_Opsyon, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tagapili = selectors.DefaultSelector(); tagapili.register(Proseso.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); tapusin_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > tapusin_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in tagapili.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Proseso.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def i_email(linya, 확인표시=b'jkoros-native> '):
        Proseso.stdin.write(linya.encode('utf-8') + b'\n'); Proseso.stdin.flush()
        return 수신하기(확인표시)
    def Mag_execute_utos(linya):
        출력결과 = i_email(linya); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        file_list = []
        for 포함항목 in argumento_ARRAY.include:
            if 포함항목.is_dir():
                file_list += [(str(data_posisyon.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', data_posisyon.read_bytes()) for data_posisyon in sorted(포함항목.rglob('*.class'))]
            else:
                file_list.append((포함항목.name, 포함항목.read_bytes()))
        file_list = [(item_COUNT, patutunguhan_data) for item_COUNT, patutunguhan_data in file_list if item_COUNT != pangalan] + [(pangalan, data)]
        for upload_pangalan, upload_data in file_list:
            if len(upload_data) > 16384 or len(upload_pangalan.encode('utf-8')) > 63 or '\n' in upload_pangalan or '\r' in upload_pangalan:
                raise ValueError('추가 파일의 pangalan/sukat_82232621 제한 초과: ' + upload_pangalan)
            i_email('load ' + shlex.quote(upload_pangalan), b'hex> ')
            for 순번 in range(0, len(upload_data), 64): i_email(upload_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in i_email('.'): raise RuntimeError('upload failed: ' + upload_pangalan)
            갈무리자료 = i_email('hex ' + shlex.quote(upload_pangalan))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != upload_data: raise RuntimeError('upload verification failed')
        if kategorya_VALUE == '.java' and Mag_execute_utos('javac ' + shlex.quote(pangalan)) != 0: return 1
        실행가능파일 = argumento_ARRAY.file.stem + '.elf'
        if kategorya_VALUE == '.c' and Mag_execute_utos('cc ' + shlex.quote(pangalan) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        app = 'java ' + shlex.quote(argumento_ARRAY.class_name or argumento_ARRAY.file.stem) if kategorya_VALUE in ('.java', '.class') else ('python ' if kategorya_VALUE == '.py' else 'run ') + shlex.quote(pangalan)
        if kategorya_VALUE == '.jar': app = 'java -jar ' + shlex.quote(pangalan)
        if kategorya_VALUE == '.c': app = 'run ' + shlex.quote(실행가능파일)
        if argumento_ARRAY.linux: app = 'run --linux ' + shlex.quote(pangalan)
        if argumento_ARRAY.arguments: app += ' ' + ' '.join(shlex.quote(string_data) for string_data in argumento_ARRAY.arguments)
        return 0 if Mag_execute_utos(app) == 0 else 1
    finally:
        if Proseso.poll() is None:
            Proseso.terminate()
            try: Proseso.wait(timeout=5)
            except subprocess.TimeoutExpired: Proseso.kill(); Proseso.wait(timeout=5)
        tagapili.close(); Proseso.stdin.close(); Proseso.stdout.close()


if __name__ == '__main__':
    raise SystemExit(run())
