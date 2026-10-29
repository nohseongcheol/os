#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. кабылдоо 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from аткаруу_буйрук import Команда


def Жүргүзүү():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Аты(예: жарактуулугун_текшерүү.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Файл 또는 class 디렉터리(패키지 Аты 유지)')
    аргумент_МАССИВ = 인수해석기.parse_args()
    берилмелер = аргумент_МАССИВ.file.read_bytes()
    if аргумент_МАССИВ.class_name and аргумент_МАССИВ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Аты = аргумент_МАССИВ.class_name + '.class' if аргумент_МАССИВ.class_name else аргумент_МАССИВ.file.name
    if len(берилмелер) > 16384 or not 1 <= len(Аты.encode('utf-8')) <= 63 or '\n' in Аты or '\r' in Аты:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    категория_маани = '.elf' if берилмелер[:4] == b'\x7fELF' else аргумент_МАССИВ.file.suffix
    if аргумент_МАССИВ.linux and категория_маани != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if категория_маани not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(аргумент_МАССИВ.arguments) > 7 or any(len(сап_берилмелер.encode('utf-8')) > 255 or '\n' in сап_берилмелер or '\r' in сап_берилмелер for сап_берилмелер in аргумент_МАССИВ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Параметрлер = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if аргумент_МАССИВ.vnc: Параметрлер += ['-vnc', аргумент_МАССИВ.vnc]
    Процесси = subprocess.Popen(Команда() + Параметрлер, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор = selectors.DefaultSelector(); селектор.register(Процесси.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); аяктоо_Жылбышуу = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > аяктоо_Жылбышуу: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in селектор.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Процесси.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def жөнөтүү(сап, 확인표시=b'jkoros-native> '):
        Процесси.stdin.write(сап.encode('utf-8') + b'\n'); Процесси.stdin.flush()
        return 수신하기(확인표시)
    def аткаруу_буйрук(сап):
        출력결과 = жөнөтүү(сап); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        файл_Тизме = []
        for 포함항목 in аргумент_МАССИВ.include:
            if 포함항목.is_dir():
                файл_Тизме += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                файл_Тизме.append((포함항목.name, 포함항목.read_bytes()))
        файл_Тизме = [(개수, көздөө_жайы_берилмелер) for 개수, көздөө_жайы_берилмелер in файл_Тизме if 개수 != Аты] + [(Аты, берилмелер)]
        for жүктөп_жөнөтүү_аты, жүктөп_жөнөтүү_берилмелер in файл_Тизме:
            if len(жүктөп_жөнөтүү_берилмелер) > 16384 or len(жүктөп_жөнөтүү_аты.encode('utf-8')) > 63 or '\n' in жүктөп_жөнөтүү_аты or '\r' in жүктөп_жөнөтүү_аты:
                raise ValueError('추가 파일의 Аты/Өлчөмү 제한 초과: ' + жүктөп_жөнөтүү_аты)
            жөнөтүү('load ' + shlex.quote(жүктөп_жөнөтүү_аты), b'hex> ')
            for 순번 in range(0, len(жүктөп_жөнөтүү_берилмелер), 64): жөнөтүү(жүктөп_жөнөтүү_берилмелер[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in жөнөтүү('.'): raise RuntimeError('upload failed: ' + жүктөп_жөнөтүү_аты)
            갈무리자료 = жөнөтүү('hex ' + shlex.quote(жүктөп_жөнөтүү_аты))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != жүктөп_жөнөтүү_берилмелер: raise RuntimeError('upload verification failed')
        if категория_маани == '.java' and аткаруу_буйрук('javac ' + shlex.quote(Аты)) != 0: return 1
        실행가능파일 = аргумент_МАССИВ.file.stem + '.elf'
        if категория_маани == '.c' and аткаруу_буйрук('cc ' + shlex.quote(Аты) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        програм = 'java ' + shlex.quote(аргумент_МАССИВ.class_name or аргумент_МАССИВ.file.stem) if категория_маани in ('.java', '.class') else ('python ' if категория_маани == '.py' else 'run ') + shlex.quote(Аты)
        if категория_маани == '.jar': програм = 'java -jar ' + shlex.quote(Аты)
        if категория_маани == '.c': програм = 'run ' + shlex.quote(실행가능파일)
        if аргумент_МАССИВ.linux: програм = 'run --linux ' + shlex.quote(Аты)
        if аргумент_МАССИВ.arguments: програм += ' ' + ' '.join(shlex.quote(сап_берилмелер) for сап_берилмелер in аргумент_МАССИВ.arguments)
        return 0 if аткаруу_буйрук(програм) == 0 else 1
    finally:
        if Процесси.poll() is None:
            Процесси.terminate()
            try: Процесси.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесси.kill(); Процесси.wait(timeout=5)
        селектор.close(); Процесси.stdin.close(); Процесси.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Жүргүзүү())
