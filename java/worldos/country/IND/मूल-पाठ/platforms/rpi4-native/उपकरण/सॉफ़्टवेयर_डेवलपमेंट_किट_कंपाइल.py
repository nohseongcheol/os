#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 निज ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def चलाएँ():
    पार्सर = argparse.ArgumentParser(description=__doc__)
    पार्सर.add_argument('source', type=Path)
    पार्सर.add_argument('-o', '--output', type=Path, required=True)
    तर्क_सरणी = पार्सर.parse_args()
    डेवलपमेंट_किट = Path(__file__).resolve().parent
    출력결과 = तर्क_सरणी.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        गंतव्य_फ़ाइल, निष्पादन_योग्य_फ़ाइल = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        सूचना_प्रौद्योगिकी_सी_भाषा = तर्क_सरणी.source.suffix == '.c'
        कंपाइलर_उपकरण = os.environ.get('ARM64_CC', 'clang') if सूचना_प्रौद्योगिकी_सी_भाषा else os.environ.get('ARM64_CXX', 'clang++')
        भाषा = ['-std=c11'] if सूचना_प्रौद्योगिकी_सी_भाषा else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([कंपाइलर_उपकरण, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(डेवलपमेंट_किट / 'include'), '-c', str(तर्क_सरणी.source.resolve()), '-o', str(गंतव्य_फ़ाइल)] + भाषा)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(डेवलपमेंट_किट / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(निष्पादन_योग्य_फ़ाइल), str(डेवलपमेंट_किट / 'lib/start.o'), str(डेवलपमेंट_किट / 'lib/runtime.o'),
            str(गंतव्य_फ़ाइल), str(डेवलपमेंट_किट / 'lib/libposix-kor-user.a')])
        os.replace(str(निष्पादन_योग्य_फ़ाइल), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    चलाएँ()
