#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 vlastiti ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Pokreni():
    analizator = argparse.ArgumentParser(description=__doc__)
    analizator.add_argument('source', type=Path)
    analizator.add_argument('-o', '--output', type=Path, required=True)
    argument_ARRAY = analizator.parse_args()
    set_razvojnih_alata = Path(__file__).resolve().parent
    출력결과 = argument_ARRAY.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        odredišna_datoteka, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        odjel_informacijske_tehnologije_C_Jezik = argument_ARRAY.source.suffix == '.c'
        kompilator_alat = os.environ.get('ARM64_CC', 'clang') if odjel_informacijske_tehnologije_C_Jezik else os.environ.get('ARM64_CXX', 'clang++')
        Jezik = ['-std=c11'] if odjel_informacijske_tehnologije_C_Jezik else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilator_alat, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(set_razvojnih_alata / 'include'), '-c', str(argument_ARRAY.source.resolve()), '-o', str(odredišna_datoteka)] + Jezik)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(set_razvojnih_alata / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(set_razvojnih_alata / 'lib/start.o'), str(set_razvojnih_alata / 'lib/runtime.o'),
            str(odredišna_datoteka), str(set_razvojnih_alata / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Pokreni()
