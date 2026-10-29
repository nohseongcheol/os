#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 자체 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Стартиране():
    анализатор = argparse.ArgumentParser(description=__doc__)
    анализатор.add_argument('source', type=Path)
    анализатор.add_argument('-o', '--output', type=Path, required=True)
    аргумент_масив = анализатор.parse_args()
    развоен_пакет = Path(__file__).resolve().parent
    출력결과 = аргумент_масив.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        файл_местоназначение, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = аргумент_масив.source.suffix == '.c'
        компилатор_инструмент = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        език = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([компилатор_инструмент, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(развоен_пакет / 'include'), '-c', str(аргумент_масив.source.resolve()), '-o', str(файл_местоназначение)] + език)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(развоен_пакет / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(развоен_пакет / 'lib/start.o'), str(развоен_пакет / 'lib/runtime.o'),
            str(файл_местоназначение), str(развоен_пакет / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Стартиране()
