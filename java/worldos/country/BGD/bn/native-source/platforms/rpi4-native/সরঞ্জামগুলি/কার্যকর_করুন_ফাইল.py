#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. হোস্ট 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from কার্যকর_করুন_আদেশ import আদেশ


def চালনা():
    পার্সার = argparse.ArgumentParser(description=__doc__)
    পার্সার.add_argument('file', type=Path)
    পার্সার.add_argument('arguments', nargs='*')
    পার্সার.add_argument('--class-name', help='패키지가 있는 .class의 전체 নাম(예: বৈধ_করুন.꾸러미시험)')
    পার্সার.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    পার্সার.add_argument('--vnc', help='예: 127.0.0.1:2')
    পার্সার.add_argument('--include', action='append', type=Path, default=[], help='추가 class নথির_নাম 또는 class 디렉터리(패키지 নাম 유지)')
    যুক্তি_অ্যারে = পার্সার.parse_args()
    ডাটা = যুক্তি_অ্যারে.file.read_bytes()
    if যুক্তি_অ্যারে.class_name and যুক্তি_অ্যারে.file.suffix != '.class': পার্সার.error('--class-name은 .class 입력에서 사용합니다.')
    নাম = যুক্তি_অ্যারে.class_name + '.class' if যুক্তি_অ্যারে.class_name else যুক্তি_অ্যারে.file.name
    if len(ডাটা) > 16384 or not 1 <= len(নাম.encode('utf-8')) <= 63 or '\n' in নাম or '\r' in নাম:
        পার্সার.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    বিভাগ_মান = '.elf' if ডাটা[:4] == b'\x7fELF' else যুক্তি_অ্যারে.file.suffix
    if যুক্তি_অ্যারে.linux and বিভাগ_মান != '.elf': পার্সার.error('--linux는 ELF 바이너리에만 사용합니다.')
    if বিভাগ_মান not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        পার্সার.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(যুক্তি_অ্যারে.arguments) > 7 or any(len(স্ট্রিং_ডাটা.encode('utf-8')) > 255 or '\n' in স্ট্রিং_ডাটা or '\r' in স্ট্রিং_ডাটা for স্ট্রিং_ডাটা in যুক্তি_অ্যারে.arguments):
        পার্সার.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    পছন্দ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if যুক্তি_অ্যারে.vnc: পছন্দ += ['-vnc', যুক্তি_অ্যারে.vnc]
    প্রসেস = subprocess.Popen(আদেশ() + পছন্দ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    নির্বাচক = selectors.DefaultSelector(); নির্বাচক.register(প্রসেস.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); শেষ_করা_অফসেট = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > শেষ_করা_অফসেট: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in নির্বাচক.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if প্রসেস.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def পাঠান(নিবেশের_পঙ্_ক্তি, 확인표시=b'jkoros-native> '):
        প্রসেস.stdin.write(নিবেশের_পঙ্_ক্তি.encode('utf-8') + b'\n'); প্রসেস.stdin.flush()
        return 수신하기(확인표시)
    def কার্যকর_করুন_আদেশ(নিবেশের_পঙ্_ক্তি):
        출력결과 = পাঠান(নিবেশের_পঙ্_ক্তি); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ফাইল_তালিকা = []
        for 포함항목 in যুক্তি_অ্যারে.include:
            if 포함항목.is_dir():
                ফাইল_তালিকা += [(str(ডাটা_পদ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ডাটা_পদ.read_bytes()) for ডাটা_পদ in sorted(포함항목.rglob('*.class'))]
            else:
                ফাইল_তালিকা.append((포함항목.name, 포함항목.read_bytes()))
        ফাইল_তালিকা = [(개수, গন্তব্য_ডাটা) for 개수, গন্তব্য_ডাটা in ফাইল_তালিকা if 개수 != নাম] + [(নাম, ডাটা)]
        for আপলোড_নাম, আপলোড_ডাটা in ফাইল_তালিকা:
            if len(আপলোড_ডাটা) > 16384 or len(আপলোড_নাম.encode('utf-8')) > 63 or '\n' in আপলোড_নাম or '\r' in আপলোড_নাম:
                raise ValueError('추가 파일의 নাম/আকার 제한 초과: ' + আপলোড_নাম)
            পাঠান('load ' + shlex.quote(আপলোড_নাম), b'hex> ')
            for 순번 in range(0, len(আপলোড_ডাটা), 64): পাঠান(আপলোড_ডাটা[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in পাঠান('.'): raise RuntimeError('upload failed: ' + আপলোড_নাম)
            갈무리자료 = পাঠান('hex ' + shlex.quote(আপলোড_নাম))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != আপলোড_ডাটা: raise RuntimeError('upload verification failed')
        if বিভাগ_মান == '.java' and কার্যকর_করুন_আদেশ('javac ' + shlex.quote(নাম)) != 0: return 1
        실행가능파일 = যুক্তি_অ্যারে.file.stem + '.elf'
        if বিভাগ_মান == '.c' and কার্যকর_করুন_আদেশ('cc ' + shlex.quote(নাম) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        অ্যাপ = 'java ' + shlex.quote(যুক্তি_অ্যারে.class_name or যুক্তি_অ্যারে.file.stem) if বিভাগ_মান in ('.java', '.class') else ('python ' if বিভাগ_মান == '.py' else 'run ') + shlex.quote(নাম)
        if বিভাগ_মান == '.jar': অ্যাপ = 'java -jar ' + shlex.quote(নাম)
        if বিভাগ_মান == '.c': অ্যাপ = 'run ' + shlex.quote(실행가능파일)
        if যুক্তি_অ্যারে.linux: অ্যাপ = 'run --linux ' + shlex.quote(নাম)
        if যুক্তি_অ্যারে.arguments: অ্যাপ += ' ' + ' '.join(shlex.quote(স্ট্রিং_ডাটা) for স্ট্রিং_ডাটা in যুক্তি_অ্যারে.arguments)
        return 0 if কার্যকর_করুন_আদেশ(অ্যাপ) == 0 else 1
    finally:
        if প্রসেস.poll() is None:
            প্রসেস.terminate()
            try: প্রসেস.wait(timeout=5)
            except subprocess.TimeoutExpired: প্রসেস.kill(); প্রসেস.wait(timeout=5)
        নির্বাচক.close(); প্রসেস.stdin.close(); প্রসেস.stdout.close()


if __name__ == '__main__':
    raise SystemExit(চালনা())
