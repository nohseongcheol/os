#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 vlastné ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Spustiť_2():
    analyzátor = argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('source', type=Path)
    analyzátor.add_argument('-o', '--output', type=Path, required=True)
    argument_pole = analyzátor.parse_args()
    Development_Kit = Path(__file__).resolve().parent
    출력결과 = argument_pole.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        cieľový_súbor, spustiteľný_súbor = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        Informačné_systémy_C_Jazyky = argument_pole.source.suffix == '.c'
        kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang') if Informačné_systémy_C_Jazyky else os.environ.get('ARM64_CXX', 'clang++')
        Jazyky = ['-std=c11'] if Informačné_systémy_C_Jazyky else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilátor_nástroj, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(Development_Kit / 'include'), '-c', str(argument_pole.source.resolve()), '-o', str(cieľový_súbor)] + Jazyky)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(Development_Kit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(spustiteľný_súbor), str(Development_Kit / 'lib/start.o'), str(Development_Kit / 'lib/runtime.o'),
            str(cieľový_súbor), str(Development_Kit / 'lib/libposix-kor-user.a')])
        os.replace(str(spustiteľný_súbor), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Spustiť_2()
