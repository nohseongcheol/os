#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 propriu ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Pornește():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_ARRAY = parser.parse_args()
    kit_de_dezvoltare = Path(__file__).resolve().parent
    출력결과 = argument_ARRAY.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        fișier_destinație, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        sisteme_de_informații_C_Limbi_străine = argument_ARRAY.source.suffix == '.c'
        compilator_instrument = os.environ.get('ARM64_CC', 'clang') if sisteme_de_informații_C_Limbi_străine else os.environ.get('ARM64_CXX', 'clang++')
        Limbi_străine = ['-std=c11'] if sisteme_de_informații_C_Limbi_străine else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compilator_instrument, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(kit_de_dezvoltare / 'include'), '-c', str(argument_ARRAY.source.resolve()), '-o', str(fișier_destinație)] + Limbi_străine)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(kit_de_dezvoltare / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(kit_de_dezvoltare / 'lib/start.o'), str(kit_de_dezvoltare / 'lib/runtime.o'),
            str(fișier_destinație), str(kit_de_dezvoltare / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Pornește()
