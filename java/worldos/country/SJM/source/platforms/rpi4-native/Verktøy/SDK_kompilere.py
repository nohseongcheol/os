#!/usr/bin/env python3
"""distribusjon_VERDI SDK에서 freestanding C/C++를 eget ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Kjør_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_MATRISE = parser.parse_args()
    utviklingspakke = Path(__file__).resolve().parent
    produksjon = argument_MATRISE.output.resolve()
    produksjon.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(produksjon.parent)) as 작업경로:
        målfil, kjørbar_fil = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informasjonssystemer_C_Språk = argument_MATRISE.source.suffix == '.c'
        kompilator_verktøy = os.environ.get('ARM64_CC', 'clang') if informasjonssystemer_C_Språk else os.environ.get('ARM64_CXX', 'clang++')
        Språk = ['-std=c11'] if informasjonssystemer_C_Språk else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilator_verktøy, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(utviklingspakke / 'include'), '-c', str(argument_MATRISE.source.resolve()), '-o', str(målfil)] + Språk)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(utviklingspakke / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(kjørbar_fil), str(utviklingspakke / 'lib/start.o'), str(utviklingspakke / 'lib/runtime.o'),
            str(målfil), str(utviklingspakke / 'lib/libposix-kor-user.a')])
        os.replace(str(kjørbar_fil), str(produksjon))
    print(produksjon)


if __name__ == '__main__':
    Kjør_2()
