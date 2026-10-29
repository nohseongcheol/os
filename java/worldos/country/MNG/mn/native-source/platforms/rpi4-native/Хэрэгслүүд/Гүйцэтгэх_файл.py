#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. хост 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from Гүйцэтгэх_команд import Тушаал


def Ажиллуулах():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Нэр(예: баталгаажуулах.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Файл 또는 class 디렉터리(패키지 Нэр 유지)')
    аргумент_олонлог = 인수해석기.parse_args()
    өгөгдөл = аргумент_олонлог.file.read_bytes()
    if аргумент_олонлог.class_name and аргумент_олонлог.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Нэр = аргумент_олонлог.class_name + '.class' if аргумент_олонлог.class_name else аргумент_олонлог.file.name
    if len(өгөгдөл) > 16384 or not 1 <= len(Нэр.encode('utf-8')) <= 63 or '\n' in Нэр or '\r' in Нэр:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ангилал_утга = '.elf' if өгөгдөл[:4] == b'\x7fELF' else аргумент_олонлог.file.suffix
    if аргумент_олонлог.linux and ангилал_утга != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ангилал_утга not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_олонлог.arguments) > 7 or any(len(мөр_өгөгдөл.encode('utf-8')) > 255 or '\n' in мөр_өгөгдөл or '\r' in мөр_өгөгдөл for мөр_өгөгдөл in аргумент_олонлог.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Сонголтууд = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_олонлог.vnc: Сонголтууд += ['-vnc', аргумент_олонлог.vnc]
    үйл_явц = subprocess.Popen(Тушаал() + Сонголтууд, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сонгогч = selectors.DefaultSelector(); сонгогч.register(үйл_явц.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); дуусгах_Оффсет = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > дуусгах_Оффсет: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in сонгогч.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if үйл_явц.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def илгээх(Шугам, 확인표시=b'jkoros-native> '):
        үйл_явц.stdin.write(Шугам.encode('utf-8') + b'\n'); үйл_явц.stdin.flush()
        return 수신하기(확인표시)
    def Гүйцэтгэх_команд(Шугам):
        출력결과 = илгээх(Шугам); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Жагсаалт = []
        for 포함항목 in аргумент_олонлог.include:
            if 포함항목.is_dir():
                файл_Жагсаалт += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Жагсаалт.append((포함항목.name, 포함항목.read_bytes()))
        файл_Жагсаалт = [(개수, товлосон_газар_өгөгдөл) for 개수, товлосон_газар_өгөгдөл in файл_Жагсаалт if 개수 != Нэр] + [(Нэр, өгөгдөл)]
        for байршуулах_нэр, байршуулах_өгөгдөл in файл_Жагсаалт:
            if len(байршуулах_өгөгдөл) > 16384 or len(байршуулах_нэр.encode('utf-8')) > 63 or '\n' in байршуулах_нэр or '\r' in байршуулах_нэр:
                raise ValueError('추가 파일의 Нэр/Хэмжээ 제한 초과: ' + байршуулах_нэр)
            илгээх('load ' + shlex.quote(байршуулах_нэр), b'hex> ')
            for 순번 in range(0, len(байршуулах_өгөгдөл), 64): илгээх(байршуулах_өгөгдөл[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in илгээх('.'): raise RuntimeError('upload failed: ' + байршуулах_нэр)
            갈무리자료 = илгээх('hex ' + shlex.quote(байршуулах_нэр))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != байршуулах_өгөгдөл: raise RuntimeError('upload verification failed')
        if ангилал_утга == '.java' and Гүйцэтгэх_команд('javac ' + shlex.quote(Нэр)) != 0: return 1
        실행가능파일 = аргумент_олонлог.file.stem + '.elf'
        if ангилал_утга == '.c' and Гүйцэтгэх_команд('cc ' + shlex.quote(Нэр) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програм = 'java ' + shlex.quote(аргумент_олонлог.class_name or аргумент_олонлог.file.stem) if ангилал_утга in ('.java', '.class') else ('python ' if ангилал_утга == '.py' else 'run ') + shlex.quote(Нэр)
        if ангилал_утга == '.jar': програм = 'java -jar ' + shlex.quote(Нэр)
        if ангилал_утга == '.c': програм = 'run ' + shlex.quote(실행가능파일)
        if аргумент_олонлог.linux: програм = 'run --linux ' + shlex.quote(Нэр)
        if аргумент_олонлог.arguments: програм += ' ' + ' '.join(shlex.quote(мөр_өгөгдөл) for мөр_өгөгдөл in аргумент_олонлог.arguments)
        return 0 if Гүйцэтгэх_команд(програм) == 0 else 1
    finally:
        if үйл_явц.poll() is None:
            үйл_явц.terminate()
            try: үйл_явц.wait(timeout=5)
            except subprocess.TimeoutExpired: үйл_явц.kill(); үйл_явц.wait(timeout=5)
        сонгогч.close(); үйл_явц.stdin.close(); үйл_явц.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Ажиллуулах())
