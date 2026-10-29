#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. узел 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 실행 import команда


def запустить():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('file', type=Path)
    анализатор.add_argument('arguments', nargs='*')
    анализатор.add_argument('--class-name', help='패키지가 있는 .class의 전체 Название(예: проверить.тест_пакет)')
    анализатор.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI использовать_ЗНАЧЕН')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2')
    анализатор.add_argument('--include', action='append', type=Path, default=[], help='добавить_ввод class файл 또는 class 디렉터리(패키지 Название сохранять_ЗНАЧЕН)')
    аргумент_МАССИВ = анализатор.parse_args()
    данные = аргумент_МАССИВ.file.read_bytes()
    if аргумент_МАССИВ.class_name and аргумент_МАССИВ.file.suffix != '.class': анализатор.error('--class-name은 .class 입력에서 사용합니다.')
    Название = аргумент_МАССИВ.class_name + '.class' if аргумент_МАССИВ.class_name else аргумент_МАССИВ.file.name
    if len(данные) > 16384 or not 1 <= len(Название.encode('utf-8')) <= 63 or '\n' in Название or '\r' in Название:
        анализатор.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    область_ЗНАЧЕН = '.elf' if данные[:4] == b'\x7fELF' else аргумент_МАССИВ.file.suffix
    if аргумент_МАССИВ.linux and область_ЗНАЧЕН != '.elf': анализатор.error('--linux는 ELF 바이너리에만 사용합니다.')
    if область_ЗНАЧЕН not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        анализатор.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_МАССИВ.arguments) > 7 or any(len(строка_данные.encode('utf-8')) > 255 or '\n' in строка_данные or '\r' in строка_данные for строка_данные in аргумент_МАССИВ.arguments):
        анализатор.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметры = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_МАССИВ.vnc: Параметры += ['-vnc', аргумент_МАССИВ.vnc]
    Процесс = subprocess.Popen(команда() + Параметры, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор = selectors.DefaultSelector(); селектор.register(Процесс.stdout, selectors.EVENT_READ)
    def получить_письмо(метка, выполнение_ТАЙМАУТ=45):
        выход = bytearray(); элемент_СМЕЩ = time.monotonic() + выполнение_ТАЙМАУТ
        while метка not in выход:
            if time.monotonic() > элемент_СМЕЩ: raise RuntimeError('UART timeout: ' + выход.decode('utf-8', 'replace'))
            for 누름값, _ in селектор.select(0.1):
                блок_ЗНАЧЕН_652d4b53 = 누름값.fileobj.read(4096)
                if блок_ЗНАЧЕН_652d4b53: выход.extend(блок_ЗНАЧЕН_652d4b53)
            if b'PANIC:' in выход or b'FAIL ' in выход: raise RuntimeError(выход.decode('utf-8', 'replace'))
            if Процесс.poll() is not None: raise RuntimeError('QEMU exited: ' + выход.decode('utf-8', 'replace'))
        return bytes(выход)
    def написать(строка_ввода, метка=b'jkoros-native> '):
        Процесс.stdin.write(строка_ввода.encode('utf-8') + b'\n'); Процесс.stdin.flush()
        return получить_письмо(метка)
    def 실행(строка_ввода):
        выход = написать(строка_ввода); sys.stdout.buffer.write(выход); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', выход)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        получить_письмо(b'jkoros-native> ')
        список_файлов = []
        for включать in аргумент_МАССИВ.include:
            if включать.is_dir():
                список_файлов += [(str(данные_позиция.relative_to(включать).with_suffix('')).replace('/', '.') + '.class', данные_позиция.read_bytes()) for данные_позиция in sorted(включать.rglob('*.class'))]
            else:
                список_файлов.append((включать.name, включать.read_bytes()))
        список_файлов = [(товар_СЧЁТ, цель_данные) for товар_СЧЁТ, цель_данные in список_файлов if товар_СЧЁТ != Название] + [(Название, данные)]
        for Upload_имя, Upload_данные in список_файлов:
            if len(Upload_данные) > 16384 or len(Upload_имя.encode('utf-8')) > 63 or '\n' in Upload_имя or '\r' in Upload_имя:
                raise ValueError('добавить_ввод 파일의 Название/Размер 제한 초과: ' + Upload_имя)
            написать('load ' + shlex.quote(Upload_имя), b'hex> ')
            for 순번 in range(0, len(Upload_данные), 64): написать(Upload_данные[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in написать('.'): raise RuntimeError('upload failed: ' + Upload_имя)
            갈무리자료 = написать('hex ' + shlex.quote(Upload_имя))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != Upload_данные: raise RuntimeError('upload verification failed')
        if область_ЗНАЧЕН == '.java' and 실행('javac ' + shlex.quote(Название)) != 0: return 1
        исполняемый_фото = аргумент_МАССИВ.file.stem + '.elf'
        if область_ЗНАЧЕН == '.c' and 실행('cc ' + shlex.quote(Название) + ' -o ' + shlex.quote(исполняемый_фото)) != 0: return 1
        программа = 'java ' + shlex.quote(аргумент_МАССИВ.class_name or аргумент_МАССИВ.file.stem) if область_ЗНАЧЕН in ('.java', '.class') else ('python ' if область_ЗНАЧЕН == '.py' else 'run ') + shlex.quote(Название)
        if область_ЗНАЧЕН == '.jar': программа = 'java -jar ' + shlex.quote(Название)
        if область_ЗНАЧЕН == '.c': программа = 'run ' + shlex.quote(исполняемый_фото)
        if аргумент_МАССИВ.linux: программа = 'run --linux ' + shlex.quote(Название)
        if аргумент_МАССИВ.arguments: программа += ' ' + ' '.join(shlex.quote(строка_данные) for строка_данные in аргумент_МАССИВ.arguments)
        return 0 if 실행(программа) == 0 else 1
    finally:
        if Процесс.poll() is None:
            Процесс.terminate()
            try: Процесс.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait(timeout=5)
        селектор.close(); Процесс.stdin.close(); Процесс.stdout.close()


if __name__ == '__main__':
    raise SystemExit(запустить())
