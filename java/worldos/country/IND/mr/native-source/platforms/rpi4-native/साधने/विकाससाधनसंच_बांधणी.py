#!/usr/bin/env python3
"""वितरण_मूल्य SDK에서 freestanding C/C++를 स्वकीय ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def सुरू_करा():
    व्याकरणविश्लेषक = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक.add_argument('source', type=Path)
    व्याकरणविश्लेषक.add_argument('-o', '--output', type=Path, required=True)
    वितर्क_ऍरे = व्याकरणविश्लेषक.parse_args()
    विकास_संच = Path(__file__).resolve().parent
    प्रदान = वितर्क_ऍरे.output.resolve()
    प्रदान.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(प्रदान.parent)) as कार्यरत_पथ:
        गंतव्य_फाइल, निष्पादनीय_संचिका = Path(कार्यरत_पथ) / 'program.o', Path(कार्यरत_पथ) / 'program.elf'
        आहे_सी_भाषा = वितर्क_ऍरे.source.suffix == '.c'
        संकलक_साधन = os.environ.get('ARM64_CC', 'clang') if आहे_सी_भाषा else os.environ.get('ARM64_CXX', 'clang++')
        भाषा = ['-std=c11'] if आहे_सी_भाषा else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([संकलक_साधन, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(विकास_संच / 'include'), '-c', str(वितर्क_ऍरे.source.resolve()), '-o', str(गंतव्य_फाइल)] + भाषा)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(विकास_संच / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(निष्पादनीय_संचिका), str(विकास_संच / 'lib/start.o'), str(विकास_संच / 'lib/runtime.o'),
            str(गंतव्य_फाइल), str(विकास_संच / 'lib/libposix-kor-user.a')])
        os.replace(str(निष्पादनीय_संचिका), str(प्रदान))
    print(प्रदान)


if __name__ == '__main__':
    सुरू_करा()
