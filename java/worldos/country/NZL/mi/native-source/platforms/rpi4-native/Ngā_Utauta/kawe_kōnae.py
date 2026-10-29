#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. taurima 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from kawe_tono import tono


def whakahaere():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 Ingoa(예: whakamana.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class Kōnae 또는 class 디렉터리(패키지 Ingoa 유지)')
    tohenga_HUĀNGA = 인수해석기.parse_args()
    raraunga = tohenga_HUĀNGA.file.read_bytes()
    if tohenga_HUĀNGA.class_name and tohenga_HUĀNGA.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    Ingoa = tohenga_HUĀNGA.class_name + '.class' if tohenga_HUĀNGA.class_name else tohenga_HUĀNGA.file.name
    if len(raraunga) > 16384 or not 1 <= len(Ingoa.encode('utf-8')) <= 63 or '\n' in Ingoa or '\r' in Ingoa:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    kāwai_uara = '.elf' if raraunga[:4] == b'\x7fELF' else tohenga_HUĀNGA.file.suffix
    if tohenga_HUĀNGA.linux and kāwai_uara != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if kāwai_uara not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(tohenga_HUĀNGA.arguments) > 7 or any(len(aho_raraunga.encode('utf-8')) > 255 or '\n' in aho_raraunga or '\r' in aho_raraunga for aho_raraunga in tohenga_HUĀNGA.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    Kōwhiringa = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if tohenga_HUĀNGA.vnc: Kōwhiringa += ['-vnc', tohenga_HUĀNGA.vnc]
    Hātepe = subprocess.Popen(tono() + Kōwhiringa, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pūtīpako = selectors.DefaultSelector(); pūtīpako.register(Hātepe.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); mutu_OFFSET = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > mutu_OFFSET: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in pūtīpako.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if Hātepe.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def tuku(hononga, 확인표시=b'jkoros-native> '):
        Hātepe.stdin.write(hononga.encode('utf-8') + b'\n'); Hātepe.stdin.flush()
        return 수신하기(확인표시)
    def kawe_tono(hononga):
        출력결과 = tuku(hononga); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        kōnae_Rārangi = []
        for 포함항목 in tohenga_HUĀNGA.include:
            if 포함항목.is_dir():
                kōnae_Rārangi += [(str(raraunga_tūranga.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', raraunga_tūranga.read_bytes()) for raraunga_tūranga in sorted(포함항목.rglob('*.class'))]
            else:
                kōnae_Rārangi.append((포함항목.name, 포함항목.read_bytes()))
        kōnae_Rārangi = [(tuemi_COUNT, ūnga_raraunga) for tuemi_COUNT, ūnga_raraunga in kōnae_Rārangi if tuemi_COUNT != Ingoa] + [(Ingoa, raraunga)]
        for tukuatu_ingoa, tukuatu_raraunga in kōnae_Rārangi:
            if len(tukuatu_raraunga) > 16384 or len(tukuatu_ingoa.encode('utf-8')) > 63 or '\n' in tukuatu_ingoa or '\r' in tukuatu_ingoa:
                raise ValueError('추가 파일의 Ingoa/rahi 제한 초과: ' + tukuatu_ingoa)
            tuku('load ' + shlex.quote(tukuatu_ingoa), b'hex> ')
            for 순번 in range(0, len(tukuatu_raraunga), 64): tuku(tukuatu_raraunga[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in tuku('.'): raise RuntimeError('upload failed: ' + tukuatu_ingoa)
            갈무리자료 = tuku('hex ' + shlex.quote(tukuatu_ingoa))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != tukuatu_raraunga: raise RuntimeError('upload verification failed')
        if kāwai_uara == '.java' and kawe_tono('javac ' + shlex.quote(Ingoa)) != 0: return 1
        실행가능파일 = tohenga_HUĀNGA.file.stem + '.elf'
        if kāwai_uara == '.c' and kawe_tono('cc ' + shlex.quote(Ingoa) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        kaupapa = 'java ' + shlex.quote(tohenga_HUĀNGA.class_name or tohenga_HUĀNGA.file.stem) if kāwai_uara in ('.java', '.class') else ('python ' if kāwai_uara == '.py' else 'run ') + shlex.quote(Ingoa)
        if kāwai_uara == '.jar': kaupapa = 'java -jar ' + shlex.quote(Ingoa)
        if kāwai_uara == '.c': kaupapa = 'run ' + shlex.quote(실행가능파일)
        if tohenga_HUĀNGA.linux: kaupapa = 'run --linux ' + shlex.quote(Ingoa)
        if tohenga_HUĀNGA.arguments: kaupapa += ' ' + ' '.join(shlex.quote(aho_raraunga) for aho_raraunga in tohenga_HUĀNGA.arguments)
        return 0 if kawe_tono(kaupapa) == 0 else 1
    finally:
        if Hātepe.poll() is None:
            Hātepe.terminate()
            try: Hātepe.wait(timeout=5)
            except subprocess.TimeoutExpired: Hātepe.kill(); Hātepe.wait(timeout=5)
        pūtīpako.close(); Hātepe.stdin.close(); Hātepe.stdout.close()


if __name__ == '__main__':
    raise SystemExit(whakahaere())
