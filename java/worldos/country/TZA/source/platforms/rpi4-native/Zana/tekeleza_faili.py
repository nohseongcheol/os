#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. mwenyeji 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from tekeleza_amri import amri


def endesha():
    kichanganuzi = argparse.ArgumentParser(description=__doc__)
    kichanganuzi.add_argument('file', type=Path)
    kichanganuzi.add_argument('arguments', nargs='*')
    kichanganuzi.add_argument('--class-name', help='패키지가 있는 .class의 전체 Jina(예: hakikisha.꾸러미시험)')
    kichanganuzi.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    kichanganuzi.add_argument('--vnc', help='예: 127.0.0.1:2')
    kichanganuzi.add_argument('--include', action='append', type=Path, default=[], help='추가 class faili 또는 class 디렉터리(패키지 Jina 유지)')
    hoja_ARRAY = kichanganuzi.parse_args()
    data = hoja_ARRAY.file.read_bytes()
    if hoja_ARRAY.class_name and hoja_ARRAY.file.suffix != '.class': kichanganuzi.error('--class-name은 .class 입력에서 사용합니다.')
    Jina = hoja_ARRAY.class_name + '.class' if hoja_ARRAY.class_name else hoja_ARRAY.file.name
    if len(data) > 16384 or not 1 <= len(Jina.encode('utf-8')) <= 63 or '\n' in Jina or '\r' in Jina:
        kichanganuzi.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kategoria_thamani = '.elf' if data[:4] == b'\x7fELF' else hoja_ARRAY.file.suffix
    if hoja_ARRAY.linux and kategoria_thamani != '.elf': kichanganuzi.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kategoria_thamani not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        kichanganuzi.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(hoja_ARRAY.arguments) > 7 or any(len(tungo_data.encode('utf-8')) > 255 or '\n' in tungo_data or '\r' in tungo_data for tungo_data in hoja_ARRAY.arguments):
        kichanganuzi.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    chaguo = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if hoja_ARRAY.vnc: chaguo += ['-vnc', hoja_ARRAY.vnc]
    Mchakato = subprocess.Popen(amri() + chaguo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    kiteuzi = selectors.DefaultSelector(); kiteuzi.register(Mchakato.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); tamatia_Chipua = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > tamatia_Chipua: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in kiteuzi.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Mchakato.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def tuma(laini, 확인표시=b'jkoros-native> '):
        Mchakato.stdin.write(laini.encode('utf-8') + b'\n'); Mchakato.stdin.flush()
        return 수신하기(확인표시)
    def tekeleza_amri(laini):
        출력결과 = tuma(laini); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        faili_Orodha = []
        for 포함항목 in hoja_ARRAY.include:
            if 포함항목.is_dir():
                faili_Orodha += [(str(자료위치.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', 자료위치.read_bytes()) for 자료위치 in sorted(포함항목.rglob('*.class'))]
            else:
                faili_Orodha.append((포함항목.name, 포함항목.read_bytes()))
        faili_Orodha = [(개수, fikio_data) for 개수, fikio_data in faili_Orodha if 개수 != Jina] + [(Jina, data)]
        for pakia_jina, pakia_data in faili_Orodha:
            if len(pakia_data) > 16384 or len(pakia_jina.encode('utf-8')) > 63 or '\n' in pakia_jina or '\r' in pakia_jina:
                raise ValueError('추가 파일의 Jina/panga_ukubwa 제한 초과: ' + pakia_jina)
            tuma('load ' + shlex.quote(pakia_jina), b'hex> ')
            for 순번 in range(0, len(pakia_data), 64): tuma(pakia_data[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in tuma('.'): raise RuntimeError('upload failed: ' + pakia_jina)
            갈무리자료 = tuma('hex ' + shlex.quote(pakia_jina))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != pakia_data: raise RuntimeError('upload verification failed')
        if kategoria_thamani == '.java' and tekeleza_amri('javac ' + shlex.quote(Jina)) != 0: return 1
        실행가능파일 = hoja_ARRAY.file.stem + '.elf'
        if kategoria_thamani == '.c' and tekeleza_amri('cc ' + shlex.quote(Jina) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        programu = 'java ' + shlex.quote(hoja_ARRAY.class_name or hoja_ARRAY.file.stem) if kategoria_thamani in ('.java', '.class') else ('python ' if kategoria_thamani == '.py' else 'run ') + shlex.quote(Jina)
        if kategoria_thamani == '.jar': programu = 'java -jar ' + shlex.quote(Jina)
        if kategoria_thamani == '.c': programu = 'run ' + shlex.quote(실행가능파일)
        if hoja_ARRAY.linux: programu = 'run --linux ' + shlex.quote(Jina)
        if hoja_ARRAY.arguments: programu += ' ' + ' '.join(shlex.quote(tungo_data) for tungo_data in hoja_ARRAY.arguments)
        return 0 if tekeleza_amri(programu) == 0 else 1
    finally:
        if Mchakato.poll() is None:
            Mchakato.terminate()
            try: Mchakato.wait(timeout=5)
            except subprocess.TimeoutExpired: Mchakato.kill(); Mchakato.wait(timeout=5)
        kiteuzi.close(); Mchakato.stdin.close(); Mchakato.stdout.close()


if __name__ == '__main__':
    raise SystemExit(endesha())
