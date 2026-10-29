#!/usr/bin/env python3
"""배포 SDK에서 freestanding C/C++를 ίδιο ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def Εκτέλεση_2():
    ανάλυση = argparse.ArgumentParser(description=__doc__)
    ανάλυση.add_argument('source', type=Path)
    ανάλυση.add_argument('-o', '--output', type=Path, required=True)
    όρισμα_πίνακας = ανάλυση.parse_args()
    κιτ_ανάπτυξης_λογισμικού = Path(__file__).resolve().parent
    출력결과 = όρισμα_πίνακας.output.resolve()
    출력결과.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(출력결과.parent)) as 작업경로:
        αρχείο_προορισμού, εκτελέσιμο = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        πληροφοριακά_συστήματα_Ταχυδρομικός_κώδικας_Γλώσσα = όρισμα_πίνακας.source.suffix == '.c'
        πρόγραμμα_μεταγλώττισης_εργαλείο = os.environ.get('ARM64_CC', 'clang') if πληροφοριακά_συστήματα_Ταχυδρομικός_κώδικας_Γλώσσα else os.environ.get('ARM64_CXX', 'clang++')
        Γλώσσα = ['-std=c11'] if πληροφοριακά_συστήματα_Ταχυδρομικός_κώδικας_Γλώσσα else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([πρόγραμμα_μεταγλώττισης_εργαλείο, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(κιτ_ανάπτυξης_λογισμικού / 'include'), '-c', str(όρισμα_πίνακας.source.resolve()), '-o', str(αρχείο_προορισμού)] + Γλώσσα)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(κιτ_ανάπτυξης_λογισμικού / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(εκτελέσιμο), str(κιτ_ανάπτυξης_λογισμικού / 'lib/start.o'), str(κιτ_ανάπτυξης_λογισμικού / 'lib/runtime.o'),
            str(αρχείο_προορισμού), str(κιτ_ανάπτυξης_λογισμικού / 'lib/libposix-kor-user.a')])
        os.replace(str(εκτελέσιμο), str(출력결과))
    print(출력결과)


if __name__ == '__main__':
    Εκτέλεση_2()
