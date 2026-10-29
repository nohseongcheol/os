#!/usr/bin/env python3
"""paskirstymas_VALUE SDK에서 freestanding C/C++를 savas ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Paleisti():
    analizatorius = argparse.ArgumentParser(description=__doc__)
    analizatorius.add_argument('source', type=Path)
    analizatorius.add_argument('-o', '--output', type=Path, required=True)
    argumentas_ARRAY = analizatorius.parse_args()
    programuotojo_rinkinys = Path(__file__).resolve().parent
    išeiga = argumentas_ARRAY.output.resolve()
    išeiga.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(išeiga.parent)) as 작업경로:
        paskirties_failas, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        informacinės_technologijos_C_Kalba = argumentas_ARRAY.source.suffix == '.c'
        kompiliatorius_įrankis = os.environ.get('ARM64_CC', 'clang') if informacinės_technologijos_C_Kalba else os.environ.get('ARM64_CXX', 'clang++')
        Kalba = ['-std=c11'] if informacinės_technologijos_C_Kalba else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompiliatorius_įrankis, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(programuotojo_rinkinys / 'include'), '-c', str(argumentas_ARRAY.source.resolve()), '-o', str(paskirties_failas)] + Kalba)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(programuotojo_rinkinys / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(programuotojo_rinkinys / 'lib/start.o'), str(programuotojo_rinkinys / 'lib/runtime.o'),
            str(paskirties_failas), str(programuotojo_rinkinys / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(išeiga))
    print(išeiga)


if __name__ == '__main__':
    Paleisti()
