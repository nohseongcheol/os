#!/usr/bin/env python3
"""配布値 SDK에서 freestanding C/C++를 内蔵 ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def 起動処理():
    引数解析器 = argparse.ArgumentParser(description=__doc__)
    引数解析器.add_argument('source', type=Path)
    引数解析器.add_argument('-o', '--output', type=Path, required=True)
    引数配列 = 引数解析器.parse_args()
    開発道具一式 = Path(__file__).resolve().parent
    出力結果 = 引数配列.output.resolve()
    出力結果.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(出力結果.parent)) as 作業中経路:
        宛先ファイル, 実行形式ファイル = Path(作業中経路) / 'program.o', Path(作業中経路) / 'program.elf'
        判定C言語 = 引数配列.source.suffix == '.c'
        コンパイラ道具要素 = os.environ.get('ARM64_CC', 'clang') if 判定C言語 else os.environ.get('ARM64_CXX', 'clang++')
        言語 = ['-std=c11'] if 判定C言語 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([コンパイラ道具要素, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(開発道具一式 / 'include'), '-c', str(引数配列.source.resolve()), '-o', str(宛先ファイル)] + 言語)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(開発道具一式 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(実行形式ファイル), str(開発道具一式 / 'lib/start.o'), str(開発道具一式 / 'lib/runtime.o'),
            str(宛先ファイル), str(開発道具一式 / 'lib/libposix-kor-user.a')])
        os.replace(str(実行形式ファイル), str(出力結果))
    print(出力結果)


if __name__ == '__main__':
    起動処理()
