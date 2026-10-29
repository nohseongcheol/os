#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 lastno ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Zaženi():
    razčlenjevalnik = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik.add_argument('source', type=Path)
    razčlenjevalnik.add_argument('-o', '--output', type=Path, required=True)
    argument_ARRAY = razčlenjevalnik.parse_args()
    razvijalski_komplet = Path(__file__).resolve().parent
    출력결과 = argument_ARRAY.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        ciljna_datoteka, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informacijska_tehnologija_C_jezik = argument_ARRAY.source.suffix == '.c'
        prevajalnik_orodje = os.environ.get('ARM64_CC', 'clang') if informacijska_tehnologija_C_jezik else os.environ.get('ARM64_CXX', 'clang++')
        jezik = ['-std=c11'] if informacijska_tehnologija_C_jezik else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([prevajalnik_orodje, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(razvijalski_komplet / 'include'), '-c', str(argument_ARRAY.source.resolve()), '-o', str(ciljna_datoteka)] + jezik)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(razvijalski_komplet / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(razvijalski_komplet / 'lib/start.o'), str(razvijalski_komplet / 'lib/runtime.o'),
            str(ciljna_datoteka), str(razvijalski_komplet / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Zaženi()
