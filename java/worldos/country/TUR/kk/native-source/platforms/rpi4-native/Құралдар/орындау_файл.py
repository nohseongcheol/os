#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. орналастыру 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from орындау_пәрмен import Команда


def Орындау_2():
    талдау_құралы = argparse.ArgumentParser(description=__doc__)
    талдау_құралы.add_argument('file', type=Path)
    талдау_құралы.add_argument('arguments', nargs='*')
    талдау_құралы.add_argument('--class-name', help='패키지가 있는 .class의 전체 Аты(예: тексеру_5fb2b747.꾸러미시험)')
    талдау_құралы.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    талдау_құралы.add_argument('--vnc', help='예: 127.0.0.1:2')
    талдау_құралы.add_argument('--include', action='append', type=Path, default=[], help='қосу_енгізу class Файл 또는 class 디렉터리(패키지 Аты 유지)')
    аргумент_массив = талдау_құралы.parse_args()
    деректер = аргумент_массив.file.read_bytes()
    if аргумент_массив.class_name and аргумент_массив.file.suffix != '.class': талдау_құралы.error('--class-name은 .class 입력에서 사용합니다.')
    Аты = аргумент_массив.class_name + '.class' if аргумент_массив.class_name else аргумент_массив.file.name
    if len(деректер) > 16384 or not 1 <= len(Аты.encode('utf-8')) <= 63 or '\n' in Аты or '\r' in Аты:
        талдау_құралы.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    Санат_мән = '.elf' if деректер[:4] == b'\x7fELF' else аргумент_массив.file.suffix
    if аргумент_массив.linux and Санат_мән != '.elf': талдау_құралы.error('--linux는 ELF 바이너리에만 사용합니다.')
    if Санат_мән not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        талдау_құралы.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_массив.arguments) > 7 or any(len(жол_деректер.encode('utf-8')) > 255 or '\n' in жол_деректер or '\r' in жол_деректер for жол_деректер in аргумент_массив.arguments):
        талдау_құралы.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметрлер = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_массив.vnc: Параметрлер += ['-vnc', аргумент_массив.vnc]
    Үрдіс = subprocess.Popen(Команда() + Параметрлер, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор = selectors.DefaultSelector(); селектор.register(Үрдіс.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); тоқтату_жылжыту = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > тоқтату_жылжыту: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in селектор.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Үрдіс.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def жіберу(Жол, 확인표시=b'jkoros-native> '):
        Үрдіс.stdin.write(Жол.encode('utf-8') + b'\n'); Үрдіс.stdin.flush()
        return 수신하기(확인표시)
    def орындау_пәрмен(Жол):
        출력결과 = жіберу(Жол); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Тізім = []
        for 포함항목 in аргумент_массив.include:
            if 포함항목.is_dir():
                файл_Тізім += [(str(деректер_лауазым.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', деректер_лауазым.read_bytes()) for деректер_лауазым in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Тізім.append((포함항목.name, 포함항목.read_bytes()))
        файл_Тізім = [(개수, тағайындау_деректер) for 개수, тағайындау_деректер in файл_Тізім if 개수 != Аты] + [(Аты, деректер)]
        for Жүктеп_салу_аты, Жүктеп_салу_деректер in файл_Тізім:
            if len(Жүктеп_салу_деректер) > 16384 or len(Жүктеп_салу_аты.encode('utf-8')) > 63 or '\n' in Жүктеп_салу_аты or '\r' in Жүктеп_салу_аты:
                raise ValueError('қосу_енгізу 파일의 Аты/Өлшемі 제한 초과: ' + Жүктеп_салу_аты)
            жіберу('load ' + shlex.quote(Жүктеп_салу_аты), b'hex> ')
            for 순번 in range(0, len(Жүктеп_салу_деректер), 64): жіберу(Жүктеп_салу_деректер[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in жіберу('.'): raise RuntimeError('upload failed: ' + Жүктеп_салу_аты)
            갈무리자료 = жіберу('hex ' + shlex.quote(Жүктеп_салу_аты))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Жүктеп_салу_деректер: raise RuntimeError('upload verification failed')
        if Санат_мән == '.java' and орындау_пәрмен('javac ' + shlex.quote(Аты)) != 0: return 1
        실행가능파일 = аргумент_массив.file.stem + '.elf'
        if Санат_мән == '.c' and орындау_пәрмен('cc ' + shlex.quote(Аты) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        бағдарлама = 'java ' + shlex.quote(аргумент_массив.class_name or аргумент_массив.file.stem) if Санат_мән in ('.java', '.class') else ('python ' if Санат_мән == '.py' else 'run ') + shlex.quote(Аты)
        if Санат_мән == '.jar': бағдарлама = 'java -jar ' + shlex.quote(Аты)
        if Санат_мән == '.c': бағдарлама = 'run ' + shlex.quote(실행가능파일)
        if аргумент_массив.linux: бағдарлама = 'run --linux ' + shlex.quote(Аты)
        if аргумент_массив.arguments: бағдарлама += ' ' + ' '.join(shlex.quote(жол_деректер) for жол_деректер in аргумент_массив.arguments)
        return 0 if орындау_пәрмен(бағдарлама) == 0 else 1
    finally:
        if Үрдіс.poll() is None:
            Үрдіс.terminate()
            try: Үрдіс.wait(timeout=5)
            except subprocess.TimeoutExpired: Үрдіс.kill(); Үрдіс.wait(timeout=5)
        селектор.close(); Үрдіс.stdin.close(); Үрдіс.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Орындау_2())
