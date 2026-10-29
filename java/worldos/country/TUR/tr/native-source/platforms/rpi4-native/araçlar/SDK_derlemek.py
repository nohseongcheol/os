#!/usr/bin/env python3
"""dağıtım_değer SDK에서 freestanding C/C++를 Öz ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def çalıştır():
    ayrıştırıcı = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı.add_argument('source', type=Path)
    ayrıştırıcı.add_argument('-o', '--output', type=Path, required=True)
    bağımsız_değişken_DİZİ = ayrıştırıcı.parse_args()
    geliştirme_seti = Path(__file__).resolve().parent
    çıktı = bağımsız_değişken_DİZİ.output.resolve()
    çıktı.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(çıktı.parent)) as 작업경로:
        hedef_dosya, çalıştırılabilir = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        bilgi_teknolojisi_C_Dil = bağımsız_değişken_DİZİ.source.suffix == '.c'
        derleyici_araç = os.environ.get('ARM64_CC', 'clang') if bilgi_teknolojisi_C_Dil else os.environ.get('ARM64_CXX', 'clang++')
        Dil = ['-std=c11'] if bilgi_teknolojisi_C_Dil else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([derleyici_araç, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(geliştirme_seti / 'include'), '-c', str(bağımsız_değişken_DİZİ.source.resolve()), '-o', str(hedef_dosya)] + Dil)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(geliştirme_seti / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(çalıştırılabilir), str(geliştirme_seti / 'lib/start.o'), str(geliştirme_seti / 'lib/runtime.o'),
            str(hedef_dosya), str(geliştirme_seti / 'lib/libposix-kor-user.a')])
        os.replace(str(çalıştırılabilir), str(çıktı))
    print(çıktı)


if __name__ == '__main__':
    çalıştır()
