#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 자체 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def koristiti():
    analizator = argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('source', type=Path)
    analizator.add_argument('-o', '--output', type=Path, required=True)
    argument_niz = analizator.parse_args()
    komplet_za_razvoj_programa = Path(__file__).resolve().parent
    출력결과 = argument_niz.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        odredišna_datoteka, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informatičko_odeljenje_C_jezik = argument_niz.source.suffix == '.c'
        kompajler_alatka = os.environ.get('ARM64_CC', 'clang') if informatičko_odeljenje_C_jezik else os.environ.get('ARM64_CXX', 'clang++')
        jezik = ['-std=c11'] if informatičko_odeljenje_C_jezik else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompajler_alatka, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(komplet_za_razvoj_programa / 'include'), '-c', str(argument_niz.source.resolve()), '-o', str(odredišna_datoteka)] + jezik)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(komplet_za_razvoj_programa / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(komplet_za_razvoj_programa / 'lib/start.o'), str(komplet_za_razvoj_programa / 'lib/runtime.o'),
            str(odredišna_datoteka), str(komplet_za_razvoj_programa / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    koristiti()
