#!/usr/bin/env python3
"""分发值 SDK에서 freestanding C/C++를 内置 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def 运行():
    参数解析器 = argparse.ArgumentParser(description=__doc__)
    参数解析器.add_argument('source', type=Path)
    参数解析器.add_argument('-o', '--output', type=Path, required=True)
    参数数组 = 参数解析器.parse_args()
    开发工具套件 = Path(__file__).resolve().parent
    输出结果 = 参数数组.output.resolve()
    输出结果.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(输出结果.parent)) as 工作中路径:
        目的地址文件, 可执行文件文件 = Path(工作中路径) / 'program.o', Path(工作中路径) / 'program.elf'
        是否C语言 = 参数数组.source.suffix == '.c'
        编译器工具 = os.environ.get('ARM64_CC', 'clang') if 是否C语言 else os.environ.get('ARM64_CXX', 'clang++')
        语言 = ['-std=c11'] if 是否C语言 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([编译器工具, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(开发工具套件 / 'include'), '-c', str(参数数组.source.resolve()), '-o', str(目的地址文件)] + 语言)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(开发工具套件 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(可执行文件文件), str(开发工具套件 / 'lib/start.o'), str(开发工具套件 / 'lib/runtime.o'),
            str(目的地址文件), str(开发工具套件 / 'lib/libposix-kor-user.a')])
        os.replace(str(可执行文件文件), str(输出结果))
    print(输出结果)


if __name__ == '__main__':
    运行()
