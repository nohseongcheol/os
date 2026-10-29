#!/usr/bin/env python3
"""分發值 SDK에서 freestanding C/C++를 內建 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def 運行():
    參數解析器 = argparse.ArgumentParser(description=__doc__)
    參數解析器.add_argument('source', type=Path)
    參數解析器.add_argument('-o', '--output', type=Path, required=True)
    實際參數陣列 = 參數解析器.parse_args()
    開發工具套件 = Path(__file__).resolve().parent
    輸出結果 = 實際參數陣列.output.resolve()
    輸出結果.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(輸出結果.parent)) as 工作中路徑:
        目的地址檔案, 可執行文件檔案 = Path(工作中路徑) / 'program.o', Path(工作中路徑) / 'program.elf'
        是否C語言 = 實際參數陣列.source.suffix == '.c'
        編譯器工具 = os.environ.get('ARM64_CC', 'clang') if 是否C語言 else os.environ.get('ARM64_CXX', 'clang++')
        語言 = ['-std=c11'] if 是否C語言 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([編譯器工具, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(開發工具套件 / 'include'), '-c', str(實際參數陣列.source.resolve()), '-o', str(目的地址檔案)] + 語言)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(開發工具套件 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(可執行文件檔案), str(開發工具套件 / 'lib/start.o'), str(開發工具套件 / 'lib/runtime.o'),
            str(目的地址檔案), str(開發工具套件 / 'lib/libposix-kor-user.a')])
        os.replace(str(可執行文件檔案), str(輸出結果))
    print(輸出結果)


if __name__ == '__main__':
    運行()
