#!/usr/bin/env python3
"""distribuce_HODNOTA SDK에서 freestanding C/C++를 vlastní ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Spustit_2():
    analyzátor = argparse.ArgumentParser(description=__doc__)
    analyzátor.add_argument('source', type=Path)
    analyzátor.add_argument('-o', '--output', type=Path, required=True)
    argument_pole = analyzátor.parse_args()
    Development_Kit = Path(__file__).resolve().parent
    výstup = argument_pole.output.resolve()
    výstup.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(výstup.parent)) as 작업경로:
        cílový_soubor, spustitelný_soubor = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informační_systémy_C_Jazyk = argument_pole.source.suffix == '.c'
        kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang') if informační_systémy_C_Jazyk else os.environ.get('ARM64_CXX', 'clang++')
        Jazyk = ['-std=c11'] if informační_systémy_C_Jazyk else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilátor_nástroj, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(Development_Kit / 'include'), '-c', str(argument_pole.source.resolve()), '-o', str(cílový_soubor)] + Jazyk)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(Development_Kit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(spustitelný_soubor), str(Development_Kit / 'lib/start.o'), str(Development_Kit / 'lib/runtime.o'),
            str(cílový_soubor), str(Development_Kit / 'lib/libposix-kor-user.a')])
        os.replace(str(spustitelný_soubor), str(výstup))
    print(výstup)


if __name__ == '__main__':
    Spustit_2()
