#!/usr/bin/env python3
"""توزيع_قيمة SDK에서 freestanding C/C++를 ذاتي ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def تشغيل():
    المحلل = argparse.ArgumentParser(description=__doc__)
    المحلل.add_argument('source', type=Path)
    المحلل.add_argument('-o', '--output', type=Path, required=True)
    وسيطة_صفيف = المحلل.parse_args()
    أداة_التطوير = Path(__file__).resolve().parent
    الناتج = وسيطة_صفيف.output.resolve()
    الناتج.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(الناتج.parent)) as 작업경로:
        الملف_الوجهة, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        أنظمة_المعلومات_الرمز_البريدي_لغة = وسيطة_صفيف.source.suffix == '.c'
        محول_برمجي_أداة = os.environ.get('ARM64_CC', 'clang') if أنظمة_المعلومات_الرمز_البريدي_لغة else os.environ.get('ARM64_CXX', 'clang++')
        لغة = ['-std=c11'] if أنظمة_المعلومات_الرمز_البريدي_لغة else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([محول_برمجي_أداة, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(أداة_التطوير / 'include'), '-c', str(وسيطة_صفيف.source.resolve()), '-o', str(الملف_الوجهة)] + لغة)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(أداة_التطوير / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(أداة_التطوير / 'lib/start.o'), str(أداة_التطوير / 'lib/runtime.o'),
            str(الملف_الوجهة), str(أداة_التطوير / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(الناتج))
    print(الناتج)


if __name__ == '__main__':
    تشغيل()
