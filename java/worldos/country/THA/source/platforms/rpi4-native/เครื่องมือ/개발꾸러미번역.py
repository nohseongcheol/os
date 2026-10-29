#!/usr/bin/env python3
"""การกระจาย_ค่า SDK에서 freestanding C/C++를 เอง ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์ = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์.add_argument('source', type=Path)
    ตัวแยกวิเคราะห์.add_argument('-o', '--output', type=Path, required=True)
    อาร์กิวเมนต์_อาร์เรย์ = ตัวแยกวิเคราะห์.parse_args()
    ชุดเครื่องมือการพัฒนา = Path(__file__).resolve().parent
    ผลผลิต = อาร์กิวเมนต์_อาร์เรย์.output.resolve()
    ผลผลิต.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(ผลผลิต.parent)) as 작업경로:
        แฟ้มปลายทาง, แฟ้มปฏิบัติการ = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        시언어여부 = อาร์กิวเมนต์_อาร์เรย์.source.suffix == '.c'
        คอมไพเลอร์_เครื่องมือ = os.environ.get('ARM64_CC', 'clang') if 시언어여부 else os.environ.get('ARM64_CXX', 'clang++')
        ภาษา = ['-std=c11'] if 시언어여부 else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([คอมไพเลอร์_เครื่องมือ, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(ชุดเครื่องมือการพัฒนา / 'include'), '-c', str(อาร์กิวเมนต์_อาร์เรย์.source.resolve()), '-o', str(แฟ้มปลายทาง)] + ภาษา)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(ชุดเครื่องมือการพัฒนา / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(แฟ้มปฏิบัติการ), str(ชุดเครื่องมือการพัฒนา / 'lib/start.o'), str(ชุดเครื่องมือการพัฒนา / 'lib/runtime.o'),
            str(แฟ้มปลายทาง), str(ชุดเครื่องมือการพัฒนา / 'lib/libposix-kor-user.a')])
        os.replace(str(แฟ้มปฏิบัติการ), str(ผลผลิต))
    print(ผลผลิต)


if __name__ == '__main__':
    เรียกใช้งาน()
