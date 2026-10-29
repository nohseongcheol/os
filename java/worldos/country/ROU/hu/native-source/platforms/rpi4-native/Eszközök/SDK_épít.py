#!/usr/bin/env python3
"""elosztás_ÉRTÉK SDK에서 freestanding C/C++를 saját ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Futtatás():
    elemző = argparse.ArgumentParser(description=__doc__)
    elemző.add_argument('source', type=Path)
    elemző.add_argument('-o', '--output', type=Path, required=True)
    argumentum_TÖMB = elemző.parse_args()
    fejlesztőkészlet = Path(__file__).resolve().parent
    kimenet = argumentum_TÖMB.output.resolve()
    kimenet.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(kimenet.parent)) as 작업경로:
        célfájl, végrehajtható_Fájl = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informatikai_részleg_C_Nyelv = argumentum_TÖMB.source.suffix == '.c'
        fordítóprogram_eszköz = os.environ.get('ARM64_CC', 'clang') if informatikai_részleg_C_Nyelv else os.environ.get('ARM64_CXX', 'clang++')
        Nyelv = ['-std=c11'] if informatikai_részleg_C_Nyelv else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([fordítóprogram_eszköz, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(fejlesztőkészlet / 'include'), '-c', str(argumentum_TÖMB.source.resolve()), '-o', str(célfájl)] + Nyelv)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(fejlesztőkészlet / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(végrehajtható_Fájl), str(fejlesztőkészlet / 'lib/start.o'), str(fejlesztőkészlet / 'lib/runtime.o'),
            str(célfájl), str(fejlesztőkészlet / 'lib/libposix-kor-user.a')])
        os.replace(str(végrehajtható_Fájl), str(kimenet))
    print(kimenet)


if __name__ == '__main__':
    Futtatás()
