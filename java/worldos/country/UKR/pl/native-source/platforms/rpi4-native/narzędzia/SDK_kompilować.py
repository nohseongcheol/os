#!/usr/bin/env python3
"""dystrybucja_WARTOŚĆ SDK에서 freestanding C/C++를 własny ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Uruchom_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_TABLICA = parser.parse_args()
    zestaw_deweloperski = Path(__file__).resolve().parent
    produkt_wyjściowy = argument_TABLICA.output.resolve()
    produkt_wyjściowy.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(produkt_wyjściowy.parent)) as 작업경로:
        plik_docelowy, plik_wykonywalny = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        systemy_informacyjne_C_Język = argument_TABLICA.source.suffix == '.c'
        kompilator_narzędzie = os.environ.get('ARM64_CC', 'clang') if systemy_informacyjne_C_Język else os.environ.get('ARM64_CXX', 'clang++')
        Język = ['-std=c11'] if systemy_informacyjne_C_Język else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([kompilator_narzędzie, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(zestaw_deweloperski / 'include'), '-c', str(argument_TABLICA.source.resolve()), '-o', str(plik_docelowy)] + Język)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(zestaw_deweloperski / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(plik_wykonywalny), str(zestaw_deweloperski / 'lib/start.o'), str(zestaw_deweloperski / 'lib/runtime.o'),
            str(plik_docelowy), str(zestaw_deweloperski / 'lib/libposix-kor-user.a')])
        os.replace(str(plik_wykonywalny), str(produkt_wyjściowy))
    print(produkt_wyjściowy)


if __name__ == '__main__':
    Uruchom_2()
