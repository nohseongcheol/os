#!/usr/bin/env python3
"""distributie_WAARDE SDK에서 freestanding C/C++를 Eigen ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def starten():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_MATRIX = parser.parse_args()
    Development_Kit = Path(__file__).resolve().parent
    uitvoer = argument_MATRIX.output.resolve()
    uitvoer.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(uitvoer.parent)) as 작업경로:
        doelbestand, uitvoerbaar_bestand = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informatie_C_Taal = argument_MATRIX.source.suffix == '.c'
        compiler_hulpmiddel = os.environ.get('ARM64_CC', 'clang') if informatie_C_Taal else os.environ.get('ARM64_CXX', 'clang++')
        Taal = ['-std=c11'] if informatie_C_Taal else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compiler_hulpmiddel, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(Development_Kit / 'include'), '-c', str(argument_MATRIX.source.resolve()), '-o', str(doelbestand)] + Taal)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(Development_Kit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(uitvoerbaar_bestand), str(Development_Kit / 'lib/start.o'), str(Development_Kit / 'lib/runtime.o'),
            str(doelbestand), str(Development_Kit / 'lib/libposix-kor-user.a')])
        os.replace(str(uitvoerbaar_bestand), str(uitvoer))
    print(uitvoer)


if __name__ == '__main__':
    starten()
