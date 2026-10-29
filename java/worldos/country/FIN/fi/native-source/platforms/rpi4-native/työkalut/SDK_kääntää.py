#!/usr/bin/env python3
"""jakelu_ARVO SDK에서 freestanding C/C++를 oma ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Suorita_2():
    jäsennin = argparse.ArgumentParser(description=__doc__)
    jäsennin.add_argument('source', type=Path)
    jäsennin.add_argument('-o', '--output', type=Path, required=True)
    argumentti_MATRIISI = jäsennin.parse_args()
    ohjelmankehityspaketti = Path(__file__).resolve().parent
    tulos = argumentti_MATRIISI.output.resolve()
    tulos.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(tulos.parent)) as 작업경로:
        kohdetiedosto, suoritettava_tiedosto = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        tietojärjestelmät_C_Kieli = argumentti_MATRIISI.source.suffix == '.c'
        kääntäjä_työkalu = os.environ.get('ARM64_CC', 'clang') if tietojärjestelmät_C_Kieli else os.environ.get('ARM64_CXX', 'clang++')
        Kieli = ['-std=c11'] if tietojärjestelmät_C_Kieli else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kääntäjä_työkalu, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(ohjelmankehityspaketti / 'include'), '-c', str(argumentti_MATRIISI.source.resolve()), '-o', str(kohdetiedosto)] + Kieli)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(ohjelmankehityspaketti / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(suoritettava_tiedosto), str(ohjelmankehityspaketti / 'lib/start.o'), str(ohjelmankehityspaketti / 'lib/runtime.o'),
            str(kohdetiedosto), str(ohjelmankehityspaketti / 'lib/libposix-kor-user.a')])
        os.replace(str(suoritettava_tiedosto), str(tulos))
    print(tulos)


if __name__ == '__main__':
    Suorita_2()
