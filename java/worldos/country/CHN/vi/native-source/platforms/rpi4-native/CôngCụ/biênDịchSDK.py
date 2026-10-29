#!/usr/bin/env python3
"""giáTrịBảnPhânPhối SDK에서 freestanding C/C++를 tựThân ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def chạy():
    bộPhânTích = argparse.ArgumentParser(description=__doc__)
    bộPhânTích.add_argument('source', type=Path)
    bộPhânTích.add_argument('-o', '--output', type=Path, required=True)
    mảngĐốiSố = bộPhânTích.parse_args()
    bộCôngCụPhátTriển = Path(__file__).resolve().parent
    đầuRa = mảngĐốiSố.output.resolve()
    đầuRa.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(đầuRa.parent)) as đườngDẫnĐangLàmViệc:
        tệpĐích, tệpTệpThựcThi = Path(đườngDẫnĐangLàmViệc) / 'program.o', Path(đườngDẫnĐangLàmViệc) / 'program.elf'
        làNgônNgữC = mảngĐốiSố.source.suffix == '.c'
        côngCụTrìnhBiênDịch = os.environ.get('ARM64_CC', 'clang') if làNgônNgữC else os.environ.get('ARM64_CXX', 'clang++')
        NgônNgữ = ['-std=c11'] if làNgônNgữC else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([côngCụTrìnhBiênDịch, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(bộCôngCụPhátTriển / 'include'), '-c', str(mảngĐốiSố.source.resolve()), '-o', str(tệpĐích)] + NgônNgữ)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(bộCôngCụPhátTriển / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(tệpTệpThựcThi), str(bộCôngCụPhátTriển / 'lib/start.o'), str(bộCôngCụPhátTriển / 'lib/runtime.o'),
            str(tệpĐích), str(bộCôngCụPhátTriển / 'lib/libposix-kor-user.a')])
        os.replace(str(tệpTệpThựcThi), str(đầuRa))
    print(đầuRa)


if __name__ == '__main__':
    chạy()
