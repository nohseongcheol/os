#!/usr/bin/env python3
"""dreifing_VALUE SDK에서 freestanding C/C++를 eigin ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Keyra_2():
    þáttari = argparse.ArgumentParser(description=__doc__)
    þáttari.add_argument('source', type=Path)
    þáttari.add_argument('-o', '--output', type=Path, required=True)
    frumbreyta_ARRAY = þáttari.parse_args()
    개발꾸러미 = Path(__file__).resolve().parent
    úttak_54cd5e1d = frumbreyta_ARRAY.output.resolve()
    úttak_54cd5e1d.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(úttak_54cd5e1d.parent)) as 작업경로:
        viðtökuskrá, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = frumbreyta_ARRAY.source.suffix == '.c'
        번역기 = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        Tungumál = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([번역기, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(개발꾸러미 / 'include'), '-c', str(frumbreyta_ARRAY.source.resolve()), '-o', str(viðtökuskrá)] + Tungumál)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(개발꾸러미 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(개발꾸러미 / 'lib/start.o'), str(개발꾸러미 / 'lib/runtime.o'),
            str(viðtökuskrá), str(개발꾸러미 / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(úttak_54cd5e1d))
    print(úttak_54cd5e1d)


if __name__ == '__main__':
    Keyra_2()
