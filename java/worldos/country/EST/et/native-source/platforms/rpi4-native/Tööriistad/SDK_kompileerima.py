#!/usr/bin/env python3
"""turustus_VALUE SDK에서 freestanding C/C++를 oma ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Käivita_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_ARRAY = parser.parse_args()
    arenduskomplekt = Path(__file__).resolve().parent
    toodang = argument_ARRAY.output.resolve()
    toodang.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(toodang.parent)) as 작업경로:
        sihtfail, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        infotehnoloogia_15_Keeled = argument_ARRAY.source.suffix == '.c'
        kompilaator_tööriist = os.environ.get('ARM64_CC', 'clang') if infotehnoloogia_15_Keeled else os.environ.get('ARM64_CXX', 'clang++')
        Keeled = ['-std=c11'] if infotehnoloogia_15_Keeled else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilaator_tööriist, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(arenduskomplekt / 'include'), '-c', str(argument_ARRAY.source.resolve()), '-o', str(sihtfail)] + Keeled)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(arenduskomplekt / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(arenduskomplekt / 'lib/start.o'), str(arenduskomplekt / 'lib/runtime.o'),
            str(sihtfail), str(arenduskomplekt / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(toodang))
    print(toodang)


if __name__ == '__main__':
    Käivita_2()
