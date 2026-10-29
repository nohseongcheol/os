#!/usr/bin/env python3
"""распределение_ЗНАЧЕН SDK에서 freestanding C/C++를 свой ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def запустить():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('source', type=Path)
    анализатор.add_argument('-o', '--output', type=Path, required=True)
    аргумент_МАССИВ = анализатор.parse_args()
    комплект_SDK = Path(__file__).resolve().parent
    выход = аргумент_МАССИВ.output.resolve()
    выход.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(выход.parent)) as 작업경로:
        конечный_файл, исполняемый_файл = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        ИТ_службы_C_Язык = аргумент_МАССИВ.source.suffix == '.c'
        компилятор_средство = os.environ.get('ARM64_CC', 'clang') if ИТ_службы_C_Язык else os.environ.get('ARM64_CXX', 'clang++')
        Язык = ['-std=c11'] if ИТ_службы_C_Язык else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([компилятор_средство, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(комплект_SDK / 'include'), '-c', str(аргумент_МАССИВ.source.resolve()), '-o', str(конечный_файл)] + Язык)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(комплект_SDK / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(исполняемый_файл), str(комплект_SDK / 'lib/start.o'), str(комплект_SDK / 'lib/runtime.o'),
            str(конечный_файл), str(комплект_SDK / 'lib/libposix-kor-user.a')])
        os.replace(str(исполняемый_файл), str(выход))
    print(выход)


if __name__ == '__main__':
    запустить()
