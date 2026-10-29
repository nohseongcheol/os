#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. হ_ষ্ট 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from নিষ্পাদন_আদেশ import কমান্ড


def সঞ্চালন():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 নাম(예: বৈধকৰণ_কৰক.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class নথিপত্ৰ 또는 class 디렉터리(패키지 নাম 유지)')
    যুক্তি_শৃঙ্খলা = 인수해석기.parse_args()
    ডাটা = যুক্তি_শৃঙ্খলা.file.read_bytes()
    if যুক্তি_শৃঙ্খলা.class_name and যুক্তি_শৃঙ্খলা.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    নাম = যুক্তি_শৃঙ্খলা.class_name + '.class' if যুক্তি_শৃঙ্খলা.class_name else যুক্তি_শৃঙ্খলা.file.name
    if len(ডাটা) > 16384 or not 1 <= len(নাম.encode('utf-8')) <= 63 or '\n' in নাম or '\r' in নাম:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    বর্গ_মান = '.elf' if ডাটা[:4] == b'\x7fELF' else যুক্তি_শৃঙ্খলা.file.suffix
    if যুক্তি_শৃঙ্খলা.linux and বর্গ_মান != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if বর্গ_মান not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(যুক্তি_শৃঙ্খলা.arguments) > 7 or any(len(ষ্ট্ৰিং_ডাটা.encode('utf-8')) > 255 or '\n' in ষ্ট্ৰিং_ডাটা or '\r' in ষ্ট্ৰিং_ডাটা for ষ্ট্ৰিং_ডাটা in যুক্তি_শৃঙ্খলা.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    বিকল্প = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if যুক্তি_শৃঙ্খলা.vnc: বিকল্প += ['-vnc', যুক্তি_শৃঙ্খলা.vnc]
    প্ৰসেস = subprocess.Popen(কমান্ড() + বিকল্প, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    চয়নকাৰী = selectors.DefaultSelector(); চয়নকাৰী.register(প্ৰসেস.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); অন্ত_কৰক_অফছেট = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > অন্ত_কৰক_অফছেট: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in চয়নকাৰী.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if প্ৰসেস.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ই_মেইল_কৰক(লাইন, 확인표시=b'jkoros-native> '):
        প্ৰসেস.stdin.write(লাইন.encode('utf-8') + b'\n'); প্ৰসেস.stdin.flush()
        return 수신하기(확인표시)
    def নিষ্পাদন_আদেশ(লাইন):
        출력결과 = ই_মেইল_কৰক(লাইন); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ফাইল_সূচী = []
        for 포함항목 in যুক্তি_শৃঙ্খলা.include:
            if 포함항목.is_dir():
                ফাইল_সূচী += [(str(ডাটা_স্থান_সলনি_কৰক.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ডাটা_স্থান_সলনি_কৰক.read_bytes()) for ডাটা_স্থান_সলনি_কৰক in sorted(포함항목.rglob('*.class'))]
            else:
                ফাইল_সূচী.append((포함항목.name, 포함항목.read_bytes()))
        ফাইল_সূচী = [(개수, গন্তব্য_স্থান_ডাটা) for 개수, গন্তব্য_স্থান_ডাটা in ফাইল_সূচী if 개수 != নাম] + [(নাম, ডাটা)]
        for আপল_ড_কৰক_নাম, আপল_ড_কৰক_ডাটা in ফাইল_সূচী:
            if len(আপল_ড_কৰক_ডাটা) > 16384 or len(আপল_ড_কৰক_নাম.encode('utf-8')) > 63 or '\n' in আপল_ড_কৰক_নাম or '\r' in আপল_ড_কৰক_নাম:
                raise ValueError('추가 파일의 নাম/মাপ 제한 초과: ' + আপল_ড_কৰক_নাম)
            ই_মেইল_কৰক('load ' + shlex.quote(আপল_ড_কৰক_নাম), b'hex> ')
            for 순번 in range(0, len(আপল_ড_কৰক_ডাটা), 64): ই_মেইল_কৰক(আপল_ড_কৰক_ডাটা[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ই_মেইল_কৰক('.'): raise RuntimeError('upload failed: ' + আপল_ড_কৰক_নাম)
            갈무리자료 = ই_মেইল_কৰক('hex ' + shlex.quote(আপল_ড_কৰক_নাম))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != আপল_ড_কৰক_ডাটা: raise RuntimeError('upload verification failed')
        if বর্গ_মান == '.java' and নিষ্পাদন_আদেশ('javac ' + shlex.quote(নাম)) != 0: return 1
        실행가능파일 = যুক্তি_শৃঙ্খলা.file.stem + '.elf'
        if বর্গ_মান == '.c' and নিষ্পাদন_আদেশ('cc ' + shlex.quote(নাম) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        এপ্প্ = 'java ' + shlex.quote(যুক্তি_শৃঙ্খলা.class_name or যুক্তি_শৃঙ্খলা.file.stem) if বর্গ_মান in ('.java', '.class') else ('python ' if বর্গ_মান == '.py' else 'run ') + shlex.quote(নাম)
        if বর্গ_মান == '.jar': এপ্প্ = 'java -jar ' + shlex.quote(নাম)
        if বর্গ_মান == '.c': এপ্প্ = 'run ' + shlex.quote(실행가능파일)
        if যুক্তি_শৃঙ্খলা.linux: এপ্প্ = 'run --linux ' + shlex.quote(নাম)
        if যুক্তি_শৃঙ্খলা.arguments: এপ্প্ += ' ' + ' '.join(shlex.quote(ষ্ট্ৰিং_ডাটা) for ষ্ট্ৰিং_ডাটা in যুক্তি_শৃঙ্খলা.arguments)
        return 0 if নিষ্পাদন_আদেশ(এপ্প্) == 0 else 1
    finally:
        if প্ৰসেস.poll() is None:
            প্ৰসেস.terminate()
            try: প্ৰসেস.wait(timeout=5)
            except subprocess.TimeoutExpired: প্ৰসেস.kill(); প্ৰসেস.wait(timeout=5)
        চয়নকাৰী.close(); প্ৰসেস.stdin.close(); প্ৰসেস.stdout.close()


if __name__ == '__main__':
    raise SystemExit(সঞ্চালন())
