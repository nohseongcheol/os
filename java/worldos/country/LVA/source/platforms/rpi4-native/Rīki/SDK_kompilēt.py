#!/usr/bin/env python3
"""sadale_VALUE SDK에서 freestanding C/C++를 savs ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Palaist():
    parsētājs = argparse.ArgumentParser(description=__doc__)
    parsētājs.add_argument('source', type=Path)
    parsētājs.add_argument('-o', '--output', type=Path, required=True)
    arg_ARRAY = parsētājs.parse_args()
    programmizstrādes_komplekts = Path(__file__).resolve().parent
    ražojums = arg_ARRAY.output.resolve()
    ražojums.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(ražojums.parent)) as 작업경로:
        mērķa_fails, izpildāms_fails = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informācijas_tehnoloģija_C_Valodas = arg_ARRAY.source.suffix == '.c'
        kompilators_rīks = os.environ.get('ARM64_CC', 'clang') if informācijas_tehnoloģija_C_Valodas else os.environ.get('ARM64_CXX', 'clang++')
        Valodas = ['-std=c11'] if informācijas_tehnoloģija_C_Valodas else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilators_rīks, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(programmizstrādes_komplekts / 'include'), '-c', str(arg_ARRAY.source.resolve()), '-o', str(mērķa_fails)] + Valodas)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(programmizstrādes_komplekts / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(izpildāms_fails), str(programmizstrādes_komplekts / 'lib/start.o'), str(programmizstrādes_komplekts / 'lib/runtime.o'),
            str(mērķa_fails), str(programmizstrādes_komplekts / 'lib/libposix-kor-user.a')])
        os.replace(str(izpildāms_fails), str(ražojums))
    print(ražojums)


if __name__ == '__main__':
    Palaist()
