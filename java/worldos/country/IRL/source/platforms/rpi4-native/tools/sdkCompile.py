#!/usr/bin/env python3
"""distributionValue SDK에서 freestanding C/C++를 Native ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    argumentArray = parser.parse_args()
    developmentKit = Path(__file__).resolve().parent
    output = argumentArray.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(output.parent)) as workingPath:
        destinationFile, executableFile = Path(workingPath) / 'program.o', Path(workingPath) / 'program.elf'
        isCLanguage = argumentArray.source.suffix == '.c'
        compilerTool = os.environ.get('ARM64_CC', 'clang') if isCLanguage else os.environ.get('ARM64_CXX', 'clang++')
        language = ['-std=c11'] if isCLanguage else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compilerTool, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(developmentKit / 'include'), '-c', str(argumentArray.source.resolve()), '-o', str(destinationFile)] + language)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(developmentKit / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(executableFile), str(developmentKit / 'lib/start.o'), str(developmentKit / 'lib/runtime.o'),
            str(destinationFile), str(developmentKit / 'lib/libposix-kor-user.a')])
        os.replace(str(executableFile), str(output))
    print(output)


if __name__ == '__main__':
    run()
