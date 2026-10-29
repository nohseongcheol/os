#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 নিজ ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def চালনা():
    পার্সার = argparse.ArgumentParser(description=__doc__)
    পার্সার.add_argument('source', type=Path)
    পার্সার.add_argument('-o', '--output', type=Path, required=True)
    যুক্তি_অ্যারে = পার্সার.parse_args()
    개발꾸러미 = Path(__file__).resolve().parent
    출력결과 = যুক্তি_অ্যারে.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        গন্তব্য_ফাইল, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = যুক্তি_অ্যারে.source.suffix == '.c'
        번역기 = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        ভাষা = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([번역기, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(개발꾸러미 / 'include'), '-c', str(যুক্তি_অ্যারে.source.resolve()), '-o', str(গন্তব্য_ফাইল)] + ভাষা)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(개발꾸러미 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(개발꾸러미 / 'lib/start.o'), str(개발꾸러미 / 'lib/runtime.o'),
            str(গন্তব্য_ফাইল), str(개발꾸러미 / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    চালনা()
