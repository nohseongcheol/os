#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. dalal 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from def_ndigel import ndigel


def daw():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 tur_253d1510(예: wéral.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class bara_denc 또는 class 디렉터리(패키지 tur_253d1510 유지)')
    Tegtal_TABLO = 인수해석기.parse_args()
    mbir = Tegtal_TABLO.file.read_bytes()
    if Tegtal_TABLO.class_name and Tegtal_TABLO.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    tur_253d1510 = Tegtal_TABLO.class_name + '.class' if Tegtal_TABLO.class_name else Tegtal_TABLO.file.name
    if len(mbir) > 16384 or not 1 <= len(tur_253d1510.encode('utf-8')) <= 63 or '\n' in tur_253d1510 or '\r' in tur_253d1510:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ngiir_xëyma = '.elf' if mbir[:4] == b'\x7fELF' else Tegtal_TABLO.file.suffix
    if Tegtal_TABLO.linux and ngiir_xëyma != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ngiir_xëyma not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(Tegtal_TABLO.arguments) > 7 or any(len(araf_yu_bennoo_mbir.encode('utf-8')) > 255 or '\n' in araf_yu_bennoo_mbir or '\r' in araf_yu_bennoo_mbir for araf_yu_bennoo_mbir in Tegtal_TABLO.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    tànneef = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if Tegtal_TABLO.vnc: tànneef += ['-vnc', Tegtal_TABLO.vnc]
    yokkute = subprocess.Popen(ndigel() + tànneef, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    tànnkat = selectors.DefaultSelector(); tànnkat.register(yokkute.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); jeexal_Randal = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > jeexal_Randal: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in tànnkat.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if yokkute.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def Yónnee(buum, 확인표시=b'jkoros-native> '):
        yokkute.stdin.write(buum.encode('utf-8') + b'\n'); yokkute.stdin.flush()
        return 수신하기(확인표시)
    def def_ndigel(buum):
        출력결과 = Yónnee(buum); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        bara_denc_lim = []
        for 포함항목 in Tegtal_TABLO.include:
            if 포함항목.is_dir():
                bara_denc_lim += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                bara_denc_lim.append((포함항목.name, 포함항목.read_bytes()))
        bara_denc_lim = [(개수, jëmmukaay_mbir) for 개수, jëmmukaay_mbir in bara_denc_lim if 개수 != tur_253d1510] + [(tur_253d1510, mbir)]
        for toxalsi_tur, toxalsi_mbir in bara_denc_lim:
            if len(toxalsi_mbir) > 16384 or len(toxalsi_tur.encode('utf-8')) > 63 or '\n' in toxalsi_tur or '\r' in toxalsi_tur:
                raise ValueError('추가 파일의 tur_253d1510/tolluwaay 제한 초과: ' + toxalsi_tur)
            Yónnee('load ' + shlex.quote(toxalsi_tur), b'hex> ')
            for 순번 in range(0, len(toxalsi_mbir), 64): Yónnee(toxalsi_mbir[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in Yónnee('.'): raise RuntimeError('upload failed: ' + toxalsi_tur)
            갈무리자료 = Yónnee('hex ' + shlex.quote(toxalsi_tur))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != toxalsi_mbir: raise RuntimeError('upload verification failed')
        if ngiir_xëyma == '.java' and def_ndigel('javac ' + shlex.quote(tur_253d1510)) != 0: return 1
        실행가능파일 = Tegtal_TABLO.file.stem + '.elf'
        if ngiir_xëyma == '.c' and def_ndigel('cc ' + shlex.quote(tur_253d1510) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        jëfekaay = 'java ' + shlex.quote(Tegtal_TABLO.class_name or Tegtal_TABLO.file.stem) if ngiir_xëyma in ('.java', '.class') else ('python ' if ngiir_xëyma == '.py' else 'run ') + shlex.quote(tur_253d1510)
        if ngiir_xëyma == '.jar': jëfekaay = 'java -jar ' + shlex.quote(tur_253d1510)
        if ngiir_xëyma == '.c': jëfekaay = 'run ' + shlex.quote(실행가능파일)
        if Tegtal_TABLO.linux: jëfekaay = 'run --linux ' + shlex.quote(tur_253d1510)
        if Tegtal_TABLO.arguments: jëfekaay += ' ' + ' '.join(shlex.quote(araf_yu_bennoo_mbir) for araf_yu_bennoo_mbir in Tegtal_TABLO.arguments)
        return 0 if def_ndigel(jëfekaay) == 0 else 1
    finally:
        if yokkute.poll() is None:
            yokkute.terminate()
            try: yokkute.wait(timeout=5)
            except subprocess.TimeoutExpired: yokkute.kill(); yokkute.wait(timeout=5)
        tànnkat.close(); yokkute.stdin.close(); yokkute.stdout.close()


if __name__ == '__main__':
    raise SystemExit(daw())
