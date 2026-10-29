#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. òstair 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from gnìomhaich_àithne import àithne


def ruith():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ainm(예: dearbh_5fb2b747.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class faidhle 또는 class 디렉터리(패키지 Ainm 유지)')
    argamaid_ARRAY = 인수해석기.parse_args()
    dàta = argamaid_ARRAY.file.read_bytes()
    if argamaid_ARRAY.class_name and argamaid_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Ainm = argamaid_ARRAY.class_name + '.class' if argamaid_ARRAY.class_name else argamaid_ARRAY.file.name
    if len(dàta) > 16384 or not 1 <= len(Ainm.encode('utf-8')) <= 63 or '\n' in Ainm or '\r' in Ainm:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    roinn_seòrsa_VALUE = '.elf' if dàta[:4] == b'\x7fELF' else argamaid_ARRAY.file.suffix
    if argamaid_ARRAY.linux and roinn_seòrsa_VALUE != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if roinn_seòrsa_VALUE not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(argamaid_ARRAY.arguments) > 7 or any(len(sreang_dàta.encode('utf-8')) > 255 or '\n' in sreang_dàta or '\r' in sreang_dàta for sreang_dàta in argamaid_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Roghainnean = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if argamaid_ARRAY.vnc: Roghainnean += ['-vnc', argamaid_ARRAY.vnc]
    Pròiseas = subprocess.Popen(àithne() + Roghainnean, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnaichear = selectors.DefaultSelector(); roghnaichear.register(Pròiseas.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); crìochnaich_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > crìochnaich_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in roghnaichear.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Pròiseas.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def cuir(loidhne, 확인표시=b'jkoros-native> '):
        Pròiseas.stdin.write(loidhne.encode('utf-8') + b'\n'); Pròiseas.stdin.flush()
        return 수신하기(확인표시)
    def gnìomhaich_àithne(loidhne):
        출력결과 = cuir(loidhne); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        faidhle_Liosta = []
        for 포함항목 in argamaid_ARRAY.include:
            if 포함항목.is_dir():
                faidhle_Liosta += [(str(dàta_suidhich.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', dàta_suidhich.read_bytes()) for dàta_suidhich in sorted(포함항목.rglob('*.class'))]
            else:
                faidhle_Liosta.append((포함항목.name, 포함항목.read_bytes()))
        faidhle_Liosta = [(nì_COUNT, ceann_uidhe_dàta) for nì_COUNT, ceann_uidhe_dàta in faidhle_Liosta if nì_COUNT != Ainm] + [(Ainm, dàta)]
        for luchdaich_suas_ainm, luchdaich_suas_dàta in faidhle_Liosta:
            if len(luchdaich_suas_dàta) > 16384 or len(luchdaich_suas_ainm.encode('utf-8')) > 63 or '\n' in luchdaich_suas_ainm or '\r' in luchdaich_suas_ainm:
                raise ValueError('추가 파일의 Ainm/atharraich_am_meud 제한 초과: ' + luchdaich_suas_ainm)
            cuir('load ' + shlex.quote(luchdaich_suas_ainm), b'hex> ')
            for 순번 in range(0, len(luchdaich_suas_dàta), 64): cuir(luchdaich_suas_dàta[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in cuir('.'): raise RuntimeError('upload failed: ' + luchdaich_suas_ainm)
            갈무리자료 = cuir('hex ' + shlex.quote(luchdaich_suas_ainm))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != luchdaich_suas_dàta: raise RuntimeError('upload verification failed')
        if roinn_seòrsa_VALUE == '.java' and gnìomhaich_àithne('javac ' + shlex.quote(Ainm)) != 0: return 1
        실행가능파일 = argamaid_ARRAY.file.stem + '.elf'
        if roinn_seòrsa_VALUE == '.c' and gnìomhaich_àithne('cc ' + shlex.quote(Ainm) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ap = 'java ' + shlex.quote(argamaid_ARRAY.class_name or argamaid_ARRAY.file.stem) if roinn_seòrsa_VALUE in ('.java', '.class') else ('python ' if roinn_seòrsa_VALUE == '.py' else 'run ') + shlex.quote(Ainm)
        if roinn_seòrsa_VALUE == '.jar': ap = 'java -jar ' + shlex.quote(Ainm)
        if roinn_seòrsa_VALUE == '.c': ap = 'run ' + shlex.quote(실행가능파일)
        if argamaid_ARRAY.linux: ap = 'run --linux ' + shlex.quote(Ainm)
        if argamaid_ARRAY.arguments: ap += ' ' + ' '.join(shlex.quote(sreang_dàta) for sreang_dàta in argamaid_ARRAY.arguments)
        return 0 if gnìomhaich_àithne(ap) == 0 else 1
    finally:
        if Pròiseas.poll() is None:
            Pròiseas.terminate()
            try: Pròiseas.wait(timeout=5)
            except subprocess.TimeoutExpired: Pròiseas.kill(); Pròiseas.wait(timeout=5)
        roghnaichear.close(); Pròiseas.stdin.close(); Pròiseas.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ruith())
