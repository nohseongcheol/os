#!/usr/bin/env python3
"""distribution_VÆRDI SDK에서 freestanding C/C++를 eget ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Kør_2():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argument_MATRIX = parser.parse_args()
    Development_Kit = Path(__file__).resolve().parent
    produktoutput = argument_MATRIX.output.resolve()
    produktoutput.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(produktoutput.parent)) as 작업경로:
        destinationsfil, eksekverbar_fil = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        it_C_Sprog = argument_MATRIX.source.suffix == '.c'
        compiler_værktøj = os.environ.get('ARM64_CC', 'clang') if it_C_Sprog else os.environ.get('ARM64_CXX', 'clang++')
        Sprog = ['-std=c11'] if it_C_Sprog else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compiler_værktøj, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(Development_Kit / 'include'), '-c', str(argument_MATRIX.source.resolve()), '-o', str(destinationsfil)] + Sprog)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(Development_Kit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(eksekverbar_fil), str(Development_Kit / 'lib/start.o'), str(Development_Kit / 'lib/runtime.o'),
            str(destinationsfil), str(Development_Kit / 'lib/libposix-kor-user.a')])
        os.replace(str(eksekverbar_fil), str(produktoutput))
    print(produktoutput)


if __name__ == '__main__':
    Kør_2()
