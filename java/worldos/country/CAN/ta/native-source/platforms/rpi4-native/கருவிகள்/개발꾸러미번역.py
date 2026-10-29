#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 자체 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def செயல்படுத்துக():
    பார்சர் = argparse.ArgumentParser(description=__doc__)
    பார்சர்.add_argument('source', type=Path)
    பார்சர்.add_argument('-o', '--output', type=Path, required=True)
    மதிப்புரு_கோவை = பார்சர்.parse_args()
    개발꾸러미 = Path(__file__).resolve().parent
    출력결과 = மதிப்புரு_கோவை.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        இலக்குக்_கோப்பு, செயல்படுத்தக்கூடிய_கோப்பு = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = மதிப்புரு_கோவை.source.suffix == '.c'
        번역기 = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        மொழி = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([번역기, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(개발꾸러미 / 'include'), '-c', str(மதிப்புரு_கோவை.source.resolve()), '-o', str(இலக்குக்_கோப்பு)] + மொழி)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(개발꾸러미 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(செயல்படுத்தக்கூடிய_கோப்பு), str(개발꾸러미 / 'lib/start.o'), str(개발꾸러미 / 'lib/runtime.o'),
            str(இலக்குக்_கோப்பு), str(개발꾸러미 / 'lib/libposix-kor-user.a')])
        os.replace(str(செயல்படுத்தக்கூடிய_கோப்பு), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    செயல்படுத்துக()
