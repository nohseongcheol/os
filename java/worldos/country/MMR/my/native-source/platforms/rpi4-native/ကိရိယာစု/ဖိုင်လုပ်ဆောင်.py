#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. အိမ်ရှင် 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from စက်မောင်း import အမိန့်


def လုပ်ဆောင်():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('file', type=Path)
    인수해석기.add_argument('arguments', nargs='*')
    인수해석기.add_argument('--class-name', help='패키지가 있는 .class의 전체 အမည်(예: မှန်ကန်ကြောင်းစစ်.အထုပ်စမ်းသပ်)')
    인수해석기.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 ခေါ်လုပ် ABI သုံးစွဲမှု')
    인수해석기.add_argument('--vnc', help='예: 127.0.0.1:2')
    인수해석기.add_argument('--include', action='append', type=Path, default=[], help='အချက်နောက်တွဲ class ဖိုင် 또는 class 디렉터리(패키지 အမည် 유지)')
    ပေးအချက်အခင်းအကျင်း = 인수해석기.parse_args()
    ဒေတာ = ပေးအချက်အခင်းအကျင်း.file.read_bytes()
    if ပေးအချက်အခင်းအကျင်း.class_name and ပေးအချက်အခင်းအကျင်း.file.suffix != '.class': 인수해석기.error('--class-name은 .class 입력에서 사용합니다.')
    အမည် = ပေးအချက်အခင်းအကျင်း.class_name + '.class' if ပေးအချက်အခင်းအကျင်း.class_name else ပေးအချက်အခင်းအကျင်း.file.name
    if len(ဒေတာ) > 16384 or not 1 <= len(အမည်.encode('utf-8')) <= 63 or '\n' in အမည် or '\r' in အမည်:
        인수해석기.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    분류 = '.elf' if ဒေတာ[:4] == b'\x7fELF' else ပေးအချက်အခင်းအကျင်း.file.suffix
    if ပေးအချက်အခင်းအကျင်း.linux and 분류 != '.elf': 인수해석기.error('--linux는 ELF 바이너리에만 사용합니다.')
    if 분류 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        인수해석기.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ပေးအချက်အခင်းအကျင်း.arguments) > 7 or any(len(အက္ခရာစဉ်ဒေတာ.encode('utf-8')) > 255 or '\n' in အက္ခရာစဉ်ဒေတာ or '\r' in အက္ခရာစဉ်ဒေတာ for အက္ခရာစဉ်ဒေတာ in ပေးအချက်အခင်းအကျင်း.arguments):
        인수해석기.error('인수는 အများဆုံးတန်ဖိုး 7개, 각각 UTF-8 255바이트 이하입니다.')
    선택사항 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ပေးအချက်အခင်းအကျင်း.vnc: 선택사항 += ['-vnc', ပေးအချက်အခင်းအကျင်း.vnc]
    실행과정 = subprocess.Popen(အမိန့်() + 선택사항, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    준비선택기 = selectors.DefaultSelector(); 준비선택기.register(실행과정.stdout, selectors.EVENT_READ)
    def စာပို့ချက်လက်ခံရယူ(확인표시, လုပ်ဆောင်မှုအချိန်လွန်=45):
        출력결과 = bytearray(); အဆုံးအရွေ့ = time.monotonic() + လုပ်ဆောင်မှုအချိန်လွန်
        while 확인표시 not in 출력결과:
            if time.monotonic() > အဆုံးအရွေ့: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in 준비선택기.select(0.1):
                အစိတ်အပိုင်း = 누름값.fileobj.read(4096)
                if အစိတ်အပိုင်း: 출력결과.extend(အစိတ်အပိုင်း)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if 실행과정.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ပို့(စာကြောင်း, 확인표시=b'jkoros-native> '):
        실행과정.stdin.write(စာကြောင်း.encode('utf-8') + b'\n'); 실행과정.stdin.flush()
        return စာပို့ချက်လက်ခံရယူ(확인표시)
    def စက်မောင်း(စာကြောင်း):
        출력결과 = ပို့(စာကြောင်း); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        ဖြစ်သောညီ = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not ဖြစ်သောညီ: raise RuntimeError('guest did not report exit status')
        return int(ဖြစ်သောညီ.group(1))
    try:
        စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ')
        ဖိုင်စာရင်း = []
        for ပါဝင်စေ in ပေးအချက်အခင်းအကျင်း.include:
            if ပါဝင်စေ.is_dir():
                ဖိုင်စာရင်း += [(str(ဒေတာနေရာ.relative_to(ပါဝင်စေ).with_suffix('')).replace('/', '.') + '.class', ဒေတာနေရာ.read_bytes()) for ဒေတာနေရာ in sorted(ပါဝင်စေ.rglob('*.class'))]
            else:
                ဖိုင်စာရင်း.append((ပါဝင်စေ.name, ပါဝင်စေ.read_bytes()))
        ဖိုင်စာရင်း = [(အရေအတွက်, ဦးတည်ရာဒေတာ) for အရေအတွက်, ဦးတည်ရာဒေတာ in ဖိုင်စာရင်း if အရေအတွက် != အမည်] + [(အမည်, ဒေတာ)]
        for တင်ပို့အမည်, တင်ပို့ဒေတာ in ဖိုင်စာရင်း:
            if len(တင်ပို့ဒေတာ) > 16384 or len(တင်ပို့အမည်.encode('utf-8')) > 63 or '\n' in တင်ပို့အမည် or '\r' in တင်ပို့အမည်:
                raise ValueError('အချက်နောက်တွဲ 파일의 အမည်/အရွယ် ကန့်သတ်ချက်တန်ဖိုး 초과: ' + တင်ပို့အမည်)
            ပို့('load ' + shlex.quote(တင်ပို့အမည်), b'hex> ')
            for အစဉ်အမှတ် in range(0, len(တင်ပို့ဒေတာ), 64): ပို့(တင်ပို့ဒေတာ[အစဉ်အမှတ်:အစဉ်အမှတ်+64].hex(), b'hex> ')
            if b'LOADED' not in ပို့('.'): raise RuntimeError('upload failed: ' + တင်ပို့အမည်)
            갈무리자료 = ပို့('hex ' + shlex.quote(တင်ပို့အမည်))
            ဖြစ်သောညီ = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not ဖြစ်သောညီ or bytes.fromhex(''.join(ဖြစ်သောညီ.group(2).decode().split())) != တင်ပို့ဒေတာ: raise RuntimeError('upload verification failed')
        if 분류 == '.java' and စက်မောင်း('javac ' + shlex.quote(အမည်)) != 0: return 1
        စက်ဖိုင်စက်ပုံရိပ် = ပေးအချက်အခင်းအကျင်း.file.stem + '.elf'
        if 분류 == '.c' and စက်မောင်း('cc ' + shlex.quote(အမည်) + ' -o ' + shlex.quote(စက်ဖိုင်စက်ပုံရိပ်)) != 0: return 1
        လုပ်ဆောင်မည့်အချက် = 'java ' + shlex.quote(ပေးအချက်အခင်းအကျင်း.class_name or ပေးအချက်အခင်းအကျင်း.file.stem) if 분류 in ('.java', '.class') else ('python ' if 분류 == '.py' else 'run ') + shlex.quote(အမည်)
        if 분류 == '.jar': လုပ်ဆောင်မည့်အချက် = 'java -jar ' + shlex.quote(အမည်)
        if 분류 == '.c': လုပ်ဆောင်မည့်အချက် = 'run ' + shlex.quote(စက်ဖိုင်စက်ပုံရိပ်)
        if ပေးအချက်အခင်းအကျင်း.linux: လုပ်ဆောင်မည့်အချက် = 'run --linux ' + shlex.quote(အမည်)
        if ပေးအချက်အခင်းအကျင်း.arguments: လုပ်ဆောင်မည့်အချက် += ' ' + ' '.join(shlex.quote(အက္ခရာစဉ်ဒေတာ) for အက္ခရာစဉ်ဒေတာ in ပေးအချက်အခင်းအကျင်း.arguments)
        return 0 if စက်မောင်း(လုပ်ဆောင်မည့်အချက်) == 0 else 1
    finally:
        if 실행과정.poll() is None:
            실행과정.terminate()
            try: 실행과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait(timeout=5)
        준비선택기.close(); 실행과정.stdin.close(); 실행과정.stdout.close()


if __name__ == '__main__':
    raise SystemExit(လုပ်ဆောင်())
