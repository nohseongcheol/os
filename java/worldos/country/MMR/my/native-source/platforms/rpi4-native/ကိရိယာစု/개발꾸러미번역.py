#!/usr/bin/env python3
"""ဖြန့်ချိမှုတန်ဖိုး SDK에서 freestanding C/C++를 ကိုယ်ပိုင် ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def လုပ်ဆောင်():
    인수해석기 = argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('source', type=Path)
    인수해석기.add_argument('-o', '--output', type=Path, required=True)
    ပေးအချက်အခင်းအကျင်း = 인수해석기.parse_args()
    개발꾸러미 = Path(__file__).resolve().parent
    출력결과 = ပေးအချက်အခင်းအကျင်း.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as လုပ်ဆောင်လမ်း:
        ဦးတည်ရာဖိုင်, စက်ဖိုင်ဖိုင် = Path(လုပ်ဆောင်လမ်း) / 'program.o', Path(လုပ်ဆောင်လမ်း) / 'program.elf'
        ဖြစ်သောCဘာသာစကား = ပေးအချက်အခင်းအကျင်း.source.suffix == '.c'
        ဘာသာပြန်စက်ကိရိယာတစ်ခု = os.environ.get('ARM64_CC', 'clang') if ဖြစ်သောCဘာသာစကား else os.environ.get('ARM64_CXX', 'clang++')
        ဘာသာစကား = ['-std=c11'] if ဖြစ်သောCဘာသာစကား else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([ဘာသာပြန်စက်ကိရိယာတစ်ခု, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(개발꾸러미 / 'include'), '-c', str(ပေးအချက်အခင်းအကျင်း.source.resolve()), '-o', str(ဦးတည်ရာဖိုင်)] + ဘာသာစကား)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(개발꾸러미 / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(စက်ဖိုင်ဖိုင်), str(개발꾸러미 / 'lib/start.o'), str(개발꾸러미 / 'lib/runtime.o'),
            str(ဦးတည်ရာဖိုင်), str(개발꾸러미 / 'lib/libposix-kor-user.a')])
        os.replace(str(စက်ဖိုင်ဖိုင်), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    လုပ်ဆောင်()
