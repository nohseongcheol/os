#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 Asli ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Jalan():
    penghurai = argparse.ArgumentParser(description=__doc__)
    penghurai.add_argument('source', type=Path)
    penghurai.add_argument('-o', '--output', type=Path, required=True)
    argumen_ARRAY = penghurai.parse_args()
    개발꾸러미 = Path(__file__).resolve().parent
    출력결과 = argumen_ARRAY.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        fail_destinasi, fail_boleh_laku = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        teknologi_maklumat_C_Bahasa = argumen_ARRAY.source.suffix == '.c'
        번역기 = os.environ.get('ARM64_CC', 'clang') if teknologi_maklumat_C_Bahasa else os.environ.get('ARM64_CXX', 'clang++')
        Bahasa = ['-std=c11'] if teknologi_maklumat_C_Bahasa else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([번역기, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(개발꾸러미 / 'include'), '-c', str(argumen_ARRAY.source.resolve()), '-o', str(fail_destinasi)] + Bahasa)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(개발꾸러미 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(fail_boleh_laku), str(개발꾸러미 / 'lib/start.o'), str(개발꾸러미 / 'lib/runtime.o'),
            str(fail_destinasi), str(개발꾸러미 / 'lib/libposix-kor-user.a')])
        os.replace(str(fail_boleh_laku), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Jalan()
