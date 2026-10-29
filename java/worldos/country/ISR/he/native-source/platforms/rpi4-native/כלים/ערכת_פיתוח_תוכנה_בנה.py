#!/usr/bin/env python3
"""הפצה_ערך SDK에서 freestanding C/C++를 עצמי ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def הפעלה():
    מנתח = argparse.ArgumentParser(description=__doc__)
    מנתח.add_argument('source', type=Path)
    מנתח.add_argument('-o', '--output', type=Path, required=True)
    ארגומנט_מערך = מנתח.parse_args()
    ערכת_פיתוח = Path(__file__).resolve().parent
    פלט = ארגומנט_מערך.output.resolve()
    פלט.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(פלט.parent)) as 작업경로:
        קובץ_יעד_ffac9b48, 실행파일 = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        מערכות_מידע_מ_שפה = ארגומנט_מערך.source.suffix == '.c'
        מהדר_כלי = os.environ.get('ARM64_CC', 'clang') if מערכות_מידע_מ_שפה else os.environ.get('ARM64_CXX', 'clang++')
        שפה = ['-std=c11'] if מערכות_מידע_מ_שפה else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([מהדר_כלי, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(ערכת_פיתוח / 'include'), '-c', str(ארגומנט_מערך.source.resolve()), '-o', str(קובץ_יעד_ffac9b48)] + שפה)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(ערכת_פיתוח / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(실행파일), str(ערכת_פיתוח / 'lib/start.o'), str(ערכת_פיתוח / 'lib/runtime.o'),
            str(קובץ_יעד_ffac9b48), str(ערכת_פיתוח / 'lib/libposix-kor-user.a')])
        os.replace(str(실행파일), str(פלט))
    print(פלט)


if __name__ == '__main__':
    הפעלה()
