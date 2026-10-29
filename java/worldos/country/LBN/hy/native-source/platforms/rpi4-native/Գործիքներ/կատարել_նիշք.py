#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. հոստ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from կատարել_հրաման import Հրահանգ


def Գործարկել():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Անուն(예: վավերացնել.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Ֆայլ 또는 class 디렉터리(패키지 Անուն 유지)')
    արգումենտ_ԶԱՆԳՎԱԾ = 인수해석기.parse_args()
    տվյալ = արգումենտ_ԶԱՆԳՎԱԾ.file.read_bytes()
    if արգումենտ_ԶԱՆԳՎԱԾ.class_name and արգումենտ_ԶԱՆԳՎԱԾ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Անուն = արգումենտ_ԶԱՆԳՎԱԾ.class_name + '.class' if արգումենտ_ԶԱՆԳՎԱԾ.class_name else արգումենտ_ԶԱՆԳՎԱԾ.file.name
    if len(տվյալ) > 16384 or not 1 <= len(Անուն.encode('utf-8')) <= 63 or '\n' in Անուն or '\r' in Անուն:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    անվանակարգ_արժեք = '.elf' if տվյալ[:4] == b'\x7fELF' else արգումենտ_ԶԱՆԳՎԱԾ.file.suffix
    if արգումենտ_ԶԱՆԳՎԱԾ.linux and անվանակարգ_արժեք != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if անվանակարգ_արժեք not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(արգումենտ_ԶԱՆԳՎԱԾ.arguments) > 7 or any(len(տող_տվյալ.encode('utf-8')) > 255 or '\n' in տող_տվյալ or '\r' in տող_տվյալ for տող_տվյալ in արգումենտ_ԶԱՆԳՎԱԾ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Ընտրանքներ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if արգումենտ_ԶԱՆԳՎԱԾ.vnc: Ընտրանքներ += ['-vnc', արգումենտ_ԶԱՆԳՎԱԾ.vnc]
    Գործընթաց = subprocess.Popen(Հրահանգ() + Ընտրանքներ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ընտրիչ = selectors.DefaultSelector(); ընտրիչ.register(Գործընթաց.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); վերջացնել_Տեղաշարժում = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > վերջացնել_Տեղաշարժում: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ընտրիչ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Գործընթաց.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ուղարկել(կապ, 확인표시=b'jkoros-native> '):
        Գործընթաց.stdin.write(կապ.encode('utf-8') + b'\n'); Գործընթաց.stdin.flush()
        return 수신하기(확인표시)
    def կատարել_հրաման(կապ):
        출력결과 = ուղարկել(կապ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        նիշք_Ցուցակ = []
        for 포함항목 in արգումենտ_ԶԱՆԳՎԱԾ.include:
            if 포함항목.is_dir():
                նիշք_Ցուցակ += [(str(տվյալ_դիրք.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', տվյալ_դիրք.read_bytes()) for տվյալ_դիրք in sorted(포함항목.rglob('*.class'))]
            else:
                նիշք_Ցուցակ.append((포함항목.name, 포함항목.read_bytes()))
        նիշք_Ցուցակ = [(개수, նպատակակետ_տվյալ) for 개수, նպատակակետ_տվյալ in նիշք_Ցուցակ if 개수 != Անուն] + [(Անուն, տվյալ)]
        for վերբեռնել_անուն, վերբեռնել_տվյալ in նիշք_Ցուցակ:
            if len(վերբեռնել_տվյալ) > 16384 or len(վերբեռնել_անուն.encode('utf-8')) > 63 or '\n' in վերբեռնել_անուն or '\r' in վերբեռնել_անուն:
                raise ValueError('추가 파일의 Անուն/Չափս 제한 초과: ' + վերբեռնել_անուն)
            ուղարկել('load ' + shlex.quote(վերբեռնել_անուն), b'hex> ')
            for 순번 in range(0, len(վերբեռնել_տվյալ), 64): ուղարկել(վերբեռնել_տվյալ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ուղարկել('.'): raise RuntimeError('upload failed: ' + վերբեռնել_անուն)
            갈무리자료 = ուղարկել('hex ' + shlex.quote(վերբեռնել_անուն))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != վերբեռնել_տվյալ: raise RuntimeError('upload verification failed')
        if անվանակարգ_արժեք == '.java' and կատարել_հրաման('javac ' + shlex.quote(Անուն)) != 0: return 1
        실행가능파일 = արգումենտ_ԶԱՆԳՎԱԾ.file.stem + '.elf'
        if անվանակարգ_արժեք == '.c' and կատարել_հրաման('cc ' + shlex.quote(Անուն) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ծրագիր = 'java ' + shlex.quote(արգումենտ_ԶԱՆԳՎԱԾ.class_name or արգումենտ_ԶԱՆԳՎԱԾ.file.stem) if անվանակարգ_արժեք in ('.java', '.class') else ('python ' if անվանակարգ_արժեք == '.py' else 'run ') + shlex.quote(Անուն)
        if անվանակարգ_արժեք == '.jar': ծրագիր = 'java -jar ' + shlex.quote(Անուն)
        if անվանակարգ_արժեք == '.c': ծրագիր = 'run ' + shlex.quote(실행가능파일)
        if արգումենտ_ԶԱՆԳՎԱԾ.linux: ծրագիր = 'run --linux ' + shlex.quote(Անուն)
        if արգումենտ_ԶԱՆԳՎԱԾ.arguments: ծրագիր += ' ' + ' '.join(shlex.quote(տող_տվյալ) for տող_տվյալ in արգումենտ_ԶԱՆԳՎԱԾ.arguments)
        return 0 if կատարել_հրաման(ծրագիր) == 0 else 1
    finally:
        if Գործընթաց.poll() is None:
            Գործընթաց.terminate()
            try: Գործընթաց.wait(timeout=5)
            except subprocess.TimeoutExpired: Գործընթաց.kill(); Գործընթաց.wait(timeout=5)
        ընտրիչ.close(); Գործընթաց.stdin.close(); Գործընթաց.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Գործարկել())
