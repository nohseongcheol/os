#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. gucumbikira 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from gukora_ibwiriza import Icyo_wifuza


def ihuriro():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Izina(예: kwemeza.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Idosiye 또는 class 디렉터리(패키지 Izina 유지)')
    ingingo_ARRAY = 인수해석기.parse_args()
    amakurushingiro = ingingo_ARRAY.file.read_bytes()
    if ingingo_ARRAY.class_name and ingingo_ARRAY.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Izina = ingingo_ARRAY.class_name + '.class' if ingingo_ARRAY.class_name else ingingo_ARRAY.file.name
    if len(amakurushingiro) > 16384 or not 1 <= len(Izina.encode('utf-8')) <= 63 or '\n' in Izina or '\r' in Izina:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    icyiciro_agaciro = '.elf' if amakurushingiro[:4] == b'\x7fELF' else ingingo_ARRAY.file.suffix
    if ingingo_ARRAY.linux and icyiciro_agaciro != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if icyiciro_agaciro not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ingingo_ARRAY.arguments) > 7 or any(len(igicenteruro_amakurushingiro.encode('utf-8')) > 255 or '\n' in igicenteruro_amakurushingiro or '\r' in igicenteruro_amakurushingiro for igicenteruro_amakurushingiro in ingingo_ARRAY.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Amahitamo = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ingingo_ARRAY.vnc: Amahitamo += ['-vnc', ingingo_ARRAY.vnc]
    Inzira_a7054519 = subprocess.Popen(Icyo_wifuza() + Amahitamo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    muhitamo = selectors.DefaultSelector(); muhitamo.register(Inzira_a7054519.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); kurangiza_Ofuseti = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > kurangiza_Ofuseti: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in muhitamo.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Inzira_a7054519.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def kohereza(umurongo, 확인표시=b'jkoros-native> '):
        Inzira_a7054519.stdin.write(umurongo.encode('utf-8') + b'\n'); Inzira_a7054519.stdin.flush()
        return 수신하기(확인표시)
    def gukora_ibwiriza(umurongo):
        출력결과 = kohereza(umurongo); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        dosiye_Urutonde = []
        for 포함항목 in ingingo_ARRAY.include:
            if 포함항목.is_dir():
                dosiye_Urutonde += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                dosiye_Urutonde.append((포함항목.name, 포함항목.read_bytes()))
        dosiye_Urutonde = [(개수, aho_ijya_amakurushingiro) for 개수, aho_ijya_amakurushingiro in dosiye_Urutonde if 개수 != Izina] + [(Izina, amakurushingiro)]
        for gukurura_izina, gukurura_amakurushingiro in dosiye_Urutonde:
            if len(gukurura_amakurushingiro) > 16384 or len(gukurura_izina.encode('utf-8')) > 63 or '\n' in gukurura_izina or '\r' in gukurura_izina:
                raise ValueError('추가 파일의 Izina/Ingano 제한 초과: ' + gukurura_izina)
            kohereza('load ' + shlex.quote(gukurura_izina), b'hex> ')
            for 순번 in range(0, len(gukurura_amakurushingiro), 64): kohereza(gukurura_amakurushingiro[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in kohereza('.'): raise RuntimeError('upload failed: ' + gukurura_izina)
            갈무리자료 = kohereza('hex ' + shlex.quote(gukurura_izina))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != gukurura_amakurushingiro: raise RuntimeError('upload verification failed')
        if icyiciro_agaciro == '.java' and gukora_ibwiriza('javac ' + shlex.quote(Izina)) != 0: return 1
        실행가능파일 = ingingo_ARRAY.file.stem + '.elf'
        if icyiciro_agaciro == '.c' and gukora_ibwiriza('cc ' + shlex.quote(Izina) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        porogaramu = 'java ' + shlex.quote(ingingo_ARRAY.class_name or ingingo_ARRAY.file.stem) if icyiciro_agaciro in ('.java', '.class') else ('python ' if icyiciro_agaciro == '.py' else 'run ') + shlex.quote(Izina)
        if icyiciro_agaciro == '.jar': porogaramu = 'java -jar ' + shlex.quote(Izina)
        if icyiciro_agaciro == '.c': porogaramu = 'run ' + shlex.quote(실행가능파일)
        if ingingo_ARRAY.linux: porogaramu = 'run --linux ' + shlex.quote(Izina)
        if ingingo_ARRAY.arguments: porogaramu += ' ' + ' '.join(shlex.quote(igicenteruro_amakurushingiro) for igicenteruro_amakurushingiro in ingingo_ARRAY.arguments)
        return 0 if gukora_ibwiriza(porogaramu) == 0 else 1
    finally:
        if Inzira_a7054519.poll() is None:
            Inzira_a7054519.terminate()
            try: Inzira_a7054519.wait(timeout=5)
            except subprocess.TimeoutExpired: Inzira_a7054519.kill(); Inzira_a7054519.wait(timeout=5)
        muhitamo.close(); Inzira_a7054519.stdin.close(); Inzira_a7054519.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ihuriro())
