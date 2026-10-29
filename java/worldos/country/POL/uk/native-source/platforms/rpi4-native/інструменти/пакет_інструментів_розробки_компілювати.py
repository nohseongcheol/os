#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 своє ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def запустити():
    аналізатор = argparse.ArgumentParser(description=__doc__)
    аналізатор.add_argument('source', type=Path)
    аналізатор.add_argument('-o', '--output', type=Path, required=True)
    аргумент_масив = аналізатор.parse_args()
    пакет_розробки = Path(__file__).resolve().parent
    출력결과 = аргумент_масив.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        кінцевий_файл, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = аргумент_масив.source.suffix == '.c'
        компілятор_інструмент = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        Мови = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([компілятор_інструмент, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(пакет_розробки / 'include'), '-c', str(аргумент_масив.source.resolve()), '-o', str(кінцевий_файл)] + Мови)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(пакет_розробки / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(пакет_розробки / 'lib/start.o'), str(пакет_розробки / 'lib/runtime.o'),
            str(кінцевий_файл), str(пакет_розробки / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    запустити()
