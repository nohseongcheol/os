#!/usr/bin/env python3
"""fördelning_värde SDK에서 freestanding C/C++를 eget ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Kör():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_MATRIS = parser.parse_args()
    development_kit = Path(__file__).resolve().parent
    utleverans = argument_MATRIS.output.resolve()
    utleverans.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(utleverans.parent)) as 작업경로:
        målfil, körbar_fil_fil = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informationsteknik_C_Språk = argument_MATRIS.source.suffix == '.c'
        kompilerare_verktyg = os.environ.get('ARM64_CC', 'clang') if informationsteknik_C_Språk else os.environ.get('ARM64_CXX', 'clang++')
        Språk = ['-std=c11'] if informationsteknik_C_Språk else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilerare_verktyg, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(development_kit / 'include'), '-c', str(argument_MATRIS.source.resolve()), '-o', str(målfil)] + Språk)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(development_kit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(körbar_fil_fil), str(development_kit / 'lib/start.o'), str(development_kit / 'lib/runtime.o'),
            str(målfil), str(development_kit / 'lib/libposix-kor-user.a')])
        os.replace(str(körbar_fil_fil), str(utleverans))
    print(utleverans)


if __name__ == '__main__':
    Kör()
