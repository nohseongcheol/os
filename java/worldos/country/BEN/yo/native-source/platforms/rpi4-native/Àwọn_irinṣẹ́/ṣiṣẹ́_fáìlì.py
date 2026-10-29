#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. olùpèsè 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ṣiṣẹ́_àṣẹ import Àṣẹ


def Rọ́ọ̀nù():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Orúkọ(예: ìfọwọ́síìwé.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Fáìlì 또는 class 디렉터리(패키지 Orúkọ 유지)')
    ágúmẹ́ntì_ÀRÉÈ = 인수해석기.parse_args()
    détà = ágúmẹ́ntì_ÀRÉÈ.file.read_bytes()
    if ágúmẹ́ntì_ÀRÉÈ.class_name and ágúmẹ́ntì_ÀRÉÈ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Orúkọ = ágúmẹ́ntì_ÀRÉÈ.class_name + '.class' if ágúmẹ́ntì_ÀRÉÈ.class_name else ágúmẹ́ntì_ÀRÉÈ.file.name
    if len(détà) > 16384 or not 1 <= len(Orúkọ.encode('utf-8')) <= 63 or '\n' in Orúkọ or '\r' in Orúkọ:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ìsọ̀rí_iye = '.elf' if détà[:4] == b'\x7fELF' else ágúmẹ́ntì_ÀRÉÈ.file.suffix
    if ágúmẹ́ntì_ÀRÉÈ.linux and ìsọ̀rí_iye != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ìsọ̀rí_iye not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ágúmẹ́ntì_ÀRÉÈ.arguments) > 7 or any(len(fọ́nrán_détà.encode('utf-8')) > 255 or '\n' in fọ́nrán_détà or '\r' in fọ́nrán_détà for fọ́nrán_détà in ágúmẹ́ntì_ÀRÉÈ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Àwọn_Ẹ̀yàn = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ágúmẹ́ntì_ÀRÉÈ.vnc: Àwọn_Ẹ̀yàn += ['-vnc', ágúmẹ́ntì_ÀRÉÈ.vnc]
    Ìlànà = subprocess.Popen(Àṣẹ() + Àwọn_Ẹ̀yàn, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    olùyàn = selectors.DefaultSelector(); olùyàn.register(Ìlànà.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); parí_Ìtayọ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > parí_Ìtayọ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in olùyàn.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Ìlànà.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def í_meèlì(ìlà, 확인표시=b'jkoros-native> '):
        Ìlànà.stdin.write(ìlà.encode('utf-8') + b'\n'); Ìlànà.stdin.flush()
        return 수신하기(확인표시)
    def ṣiṣẹ́_àṣẹ(ìlà):
        출력결과 = í_meèlì(ìlà); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        fáìlì_Àtòkọ = []
        for 포함항목 in ágúmẹ́ntì_ÀRÉÈ.include:
            if 포함항목.is_dir():
                fáìlì_Àtòkọ += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                fáìlì_Àtòkọ.append((포함항목.name, 포함항목.read_bytes()))
        fáìlì_Àtòkọ = [(개수, èbúté_détà) for 개수, èbúté_détà in fáìlì_Àtòkọ if 개수 != Orúkọ] + [(Orúkọ, détà)]
        for fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ, fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà in fáìlì_Àtòkọ:
            if len(fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà) > 16384 or len(fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ.encode('utf-8')) > 63 or '\n' in fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ or '\r' in fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ:
                raise ValueError('추가 파일의 Orúkọ/Ìwọ̀n 제한 초과: ' + fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ)
            í_meèlì('load ' + shlex.quote(fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ), b'hex> ')
            for 순번 in range(0, len(fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà), 64): í_meèlì(fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in í_meèlì('.'): raise RuntimeError('upload failed: ' + fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ)
            갈무리자료 = í_meèlì('hex ' + shlex.quote(fífi_ẹ̀dà_fáìlì_ṣọwọ́_orúkọ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != fífi_ẹ̀dà_fáìlì_ṣọwọ́_détà: raise RuntimeError('upload verification failed')
        if ìsọ̀rí_iye == '.java' and ṣiṣẹ́_àṣẹ('javac ' + shlex.quote(Orúkọ)) != 0: return 1
        실행가능파일 = ágúmẹ́ntì_ÀRÉÈ.file.stem + '.elf'
        if ìsọ̀rí_iye == '.c' and ṣiṣẹ́_àṣẹ('cc ' + shlex.quote(Orúkọ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        àtòjọ_ètò = 'java ' + shlex.quote(ágúmẹ́ntì_ÀRÉÈ.class_name or ágúmẹ́ntì_ÀRÉÈ.file.stem) if ìsọ̀rí_iye in ('.java', '.class') else ('python ' if ìsọ̀rí_iye == '.py' else 'run ') + shlex.quote(Orúkọ)
        if ìsọ̀rí_iye == '.jar': àtòjọ_ètò = 'java -jar ' + shlex.quote(Orúkọ)
        if ìsọ̀rí_iye == '.c': àtòjọ_ètò = 'run ' + shlex.quote(실행가능파일)
        if ágúmẹ́ntì_ÀRÉÈ.linux: àtòjọ_ètò = 'run --linux ' + shlex.quote(Orúkọ)
        if ágúmẹ́ntì_ÀRÉÈ.arguments: àtòjọ_ètò += ' ' + ' '.join(shlex.quote(fọ́nrán_détà) for fọ́nrán_détà in ágúmẹ́ntì_ÀRÉÈ.arguments)
        return 0 if ṣiṣẹ́_àṣẹ(àtòjọ_ètò) == 0 else 1
    finally:
        if Ìlànà.poll() is None:
            Ìlànà.terminate()
            try: Ìlànà.wait(timeout=5)
            except subprocess.TimeoutExpired: Ìlànà.kill(); Ìlànà.wait(timeout=5)
        olùyàn.close(); Ìlànà.stdin.close(); Ìlànà.stdout.close()


if __name__ == '__main__':
    raise SystemExit(Rọ́ọ̀nù())
