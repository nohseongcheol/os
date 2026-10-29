#!/usr/bin/env python3
"""distribuzione_VALORE SDK에서 freestanding C/C++를 nativo ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def avvia():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argomento_array = parser.parse_args()
    kit_di_sviluppo = Path(__file__).resolve().parent
    output = argomento_array.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(output.parent)) as 작업경로:
        file_di_destinazione, eseguibile = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        reparto_IT_C_Lingua = argomento_array.source.suffix == '.c'
        compilatore_strumento = os.environ.get('ARM64_CC', 'clang') if reparto_IT_C_Lingua else os.environ.get('ARM64_CXX', 'clang++')
        Lingua = ['-std=c11'] if reparto_IT_C_Lingua else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compilatore_strumento, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(kit_di_sviluppo / 'include'), '-c', str(argomento_array.source.resolve()), '-o', str(file_di_destinazione)] + Lingua)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(kit_di_sviluppo / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(eseguibile), str(kit_di_sviluppo / 'lib/start.o'), str(kit_di_sviluppo / 'lib/runtime.o'),
            str(file_di_destinazione), str(kit_di_sviluppo / 'lib/libposix-kor-user.a')])
        os.replace(str(eseguibile), str(output))
    print(output)


if __name__ == '__main__':
    avvia()
