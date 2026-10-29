#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ਹੋਸਟ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਕਮਾਂਡ


def ਚਲਾਓ_2():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 ਨਾਂ(예: ਪ੍ਰਮਾਣਿਤ.꾸러미시험)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='추가 class ਫਾਇਲ 또는 class 디렉터리(패키지 ਨਾਂ 유지)')
    ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ = 인수해석기.parse_args()
    ਸਮੱਗਰੀ = ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.read_bytes()
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.class_name and ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    ਨਾਂ = ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.class_name + '.class' if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.class_name else ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.name
    if len(ਸਮੱਗਰੀ) > 16384 or not 1 <= len(ਨਾਂ.encode('utf-8')) <= 63 or '\n' in ਨਾਂ or '\r' in ਨਾਂ:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ਸ਼੍ਰੇਣੀ_ਕੀਮਤ = '.elf' if ਸਮੱਗਰੀ[:4] == b'\x7fELF' else ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.suffix
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.linux and ਸ਼੍ਰੇਣੀ_ਕੀਮਤ != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.arguments) > 7 or any(len(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ.encode('utf-8')) > 255 or '\n' in ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ or '\r' in ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.arguments):
        인수해석기.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ਚੋਣਾਂ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.vnc: ਚੋਣਾਂ += ['-vnc', ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.vnc]
    ਪਰੋਸੈੱਸ = subprocess.Popen(ਕਮਾਂਡ() + ਚੋਣਾਂ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ਚੋਣਕਰਤਾ = selectors.DefaultSelector(); ਚੋਣਕਰਤਾ.register(ਪਰੋਸੈੱਸ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ਅੰਤ_ਔਫਸੈਟ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ਅੰਤ_ਔਫਸੈਟ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ਚੋਣਕਰਤਾ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ਪਰੋਸੈੱਸ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ਈਮੇਲ(ਲਾਈਨ, 확인표시=b'jkoros-native> '):
        ਪਰੋਸੈੱਸ.stdin.write(ਲਾਈਨ.encode('utf-8') + b'\n'); ਪਰੋਸੈੱਸ.stdin.flush()
        return 수신하기(확인표시)
    def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਲਾਈਨ):
        출력결과 = ਈਮੇਲ(ਲਾਈਨ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ = []
        for 포함항목 in ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.include:
            if 포함항목.is_dir():
                ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ += [(str(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.read_bytes()) for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in sorted(포함항목.rglob('*.class'))]
            else:
                ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ.append((포함항목.name, 포함항목.read_bytes()))
        ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ = [(개수, ਮੰਜਿਲ_ਸਮੱਗਰੀ) for 개수, ਮੰਜਿਲ_ਸਮੱਗਰੀ in ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ if 개수 != ਨਾਂ] + [(ਨਾਂ, ਸਮੱਗਰੀ)]
        for ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ, ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ in ਲਿਖਤ_ਪੱਤਰ_ਸੂਚੀ:
            if len(ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ) > 16384 or len(ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ.encode('utf-8')) > 63 or '\n' in ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ or '\r' in ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ:
                raise ValueError('추가 파일의 ਨਾਂ/ਆਕਾਰ 제한 초과: ' + ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ)
            ਈਮੇਲ('load ' + shlex.quote(ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ), b'hex> ')
            for 순번 in range(0, len(ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ), 64): ਈਮੇਲ(ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ਈਮੇਲ('.'): raise RuntimeError('upload failed: ' + ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ)
            갈무리자료 = ਈਮੇਲ('hex ' + shlex.quote(ਅਪਲੋਡ_ਕਰੋ_ਨਾਮ))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ਅਪਲੋਡ_ਕਰੋ_ਸਮੱਗਰੀ: raise RuntimeError('upload verification failed')
        if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ == '.java' and ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('javac ' + shlex.quote(ਨਾਂ)) != 0: return 1
        실행가능파일 = ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.stem + '.elf'
        if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ == '.c' and ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('cc ' + shlex.quote(ਨਾਂ) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ਐਪਲੀਕੇਸ਼ = 'java ' + shlex.quote(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.class_name or ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.stem) if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ in ('.java', '.class') else ('python ' if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ == '.py' else 'run ') + shlex.quote(ਨਾਂ)
        if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ == '.jar': ਐਪਲੀਕੇਸ਼ = 'java -jar ' + shlex.quote(ਨਾਂ)
        if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ == '.c': ਐਪਲੀਕੇਸ਼ = 'run ' + shlex.quote(실행가능파일)
        if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.linux: ਐਪਲੀਕੇਸ਼ = 'run --linux ' + shlex.quote(ਨਾਂ)
        if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.arguments: ਐਪਲੀਕੇਸ਼ += ' ' + ' '.join(shlex.quote(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ) for ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ in ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.arguments)
        return 0 if ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਐਪਲੀਕੇਸ਼) == 0 else 1
    finally:
        if ਪਰੋਸੈੱਸ.poll() is None:
            ਪਰੋਸੈੱਸ.terminate()
            try: ਪਰੋਸੈੱਸ.wait(timeout=5)
            except subprocess.TimeoutExpired: ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait(timeout=5)
        ਚੋਣਕਰਤਾ.close(); ਪਰੋਸੈੱਸ.stdin.close(); ਪਰੋਸੈੱਸ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ਚਲਾਓ_2())
