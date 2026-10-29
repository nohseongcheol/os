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
from изпълнявам_команда import Команда


def Стартиране():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('file', type=Path)
    анализатор.add_argument('arguments', nargs='*')
    анализатор.add_argument('--class-name', help='패키지가 있는 .class의 전체 Име(예: проверка.꾸러미시험)')
    анализатор.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI използвам_стойност')
    анализатор.add_argument('--vnc', help='예: 127.0.0.1:2')
    анализатор.add_argument('--include', action='append', type=Path, default=[], help='добавям_запис class Файл 또는 class 디렉터리(패키지 Име 유지)')
    аргумент_масив = анализатор.parse_args()
    данни = аргумент_масив.file.read_bytes()
    if аргумент_масив.class_name and аргумент_масив.file.suffix != '.class': анализатор.error('--class-name은 .class 입력에서 사용합니다.')
    Име = аргумент_масив.class_name + '.class' if аргумент_масив.class_name else аргумент_масив.file.name
    if len(данни) > 16384 or not 1 <= len(Име.encode('utf-8')) <= 63 or '\n' in Име or '\r' in Име:
        анализатор.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    област_стойност = '.elf' if данни[:4] == b'\x7fELF' else аргумент_масив.file.suffix
    if аргумент_масив.linux and област_стойност != '.elf': анализатор.error('--linux는 ELF 바이너리에만 사용합니다.')
    if област_стойност not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        анализатор.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_масив.arguments) > 7 or any(len(низ_данни.encode('utf-8')) > 255 or '\n' in низ_данни or '\r' in низ_данни for низ_данни in аргумент_масив.arguments):
        анализатор.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Опции = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_масив.vnc: Опции += ['-vnc', аргумент_масив.vnc]
    Процес = subprocess.Popen(Команда() + Опции, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    свързан_елемент_за_избор = selectors.DefaultSelector(); свързан_елемент_за_избор.register(Процес.stdout, selectors.EVENT_READ)
    def получавам_имейл(маркер, 시간제한=45):
        출력결과 = bytearray(); прекратяване_на_повикването_Изместване = time.monotonic() + 시간제한
        while маркер not in 출력결과:
            if time.monotonic() > прекратяване_на_повикването_Изместване: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in свързан_елемент_за_избор.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процес.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def изпращам(ред, маркер=b'jkoros-native> '):
        Процес.stdin.write(ред.encode('utf-8') + b'\n'); Процес.stdin.flush()
        return получавам_имейл(маркер)
    def изпълнявам_команда(ред):
        출력결과 = изпращам(ред); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        получавам_имейл(b'jkoros-native> ')
        Файл_Списък = []
        for включвам_e6c90571 in аргумент_масив.include:
            if включвам_e6c90571.is_dir():
                Файл_Списък += [(str(данни_позиция.relative_to(включвам_e6c90571).with_suffix('')).replace('/', '.') + '.class', данни_позиция.read_bytes()) for данни_позиция in sorted(включвам_e6c90571.rglob('*.class'))]
            else:
                Файл_Списък.append((включвам_e6c90571.name, включвам_e6c90571.read_bytes()))
        Файл_Списък = [(개수, местоназначение_данни) for 개수, местоназначение_данни in Файл_Списък if 개수 != Име] + [(Име, данни)]
        for качвам_препратка_към_клетка, качвам_данни in Файл_Списък:
            if len(качвам_данни) > 16384 or len(качвам_препратка_към_клетка.encode('utf-8')) > 63 or '\n' in качвам_препратка_към_клетка or '\r' in качвам_препратка_към_клетка:
                raise ValueError('добавям_запис 파일의 Име/Размер 제한 초과: ' + качвам_препратка_към_клетка)
            изпращам('load ' + shlex.quote(качвам_препратка_към_клетка), b'hex> ')
            for 순번 in range(0, len(качвам_данни), 64): изпращам(качвам_данни[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in изпращам('.'): raise RuntimeError('upload failed: ' + качвам_препратка_към_клетка)
            갈무리자료 = изпращам('hex ' + shlex.quote(качвам_препратка_към_клетка))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != качвам_данни: raise RuntimeError('upload verification failed')
        if област_стойност == '.java' and изпълнявам_команда('javac ' + shlex.quote(Име)) != 0: return 1
        실행가능파일 = аргумент_масив.file.stem + '.elf'
        if област_стойност == '.c' and изпълнявам_команда('cc ' + shlex.quote(Име) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програма = 'java ' + shlex.quote(аргумент_масив.class_name or аргумент_масив.file.stem) if област_стойност in ('.java', '.class') else ('python ' if област_стойност == '.py' else 'run ') + shlex.quote(Име)
        if област_стойност == '.jar': програма = 'java -jar ' + shlex.quote(Име)
        if област_стойност == '.c': програма = 'run ' + shlex.quote(실행가능파일)
        if аргумент_масив.linux: програма = 'run --linux ' + shlex.quote(Име)
        if аргумент_масив.arguments: програма += ' ' + ' '.join(shlex.quote(низ_данни) for низ_данни in аргумент_масив.arguments)
        return 0 if изпълнявам_команда(програма) == 0 else 1
    finally:
        if Процес.poll() is None:
            Процес.terminate()
            try: Процес.wait(timeout=5)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait(timeout=5)
        свързан_елемент_за_избор.close(); Процес.stdin.close(); Процес.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Стартиране())
