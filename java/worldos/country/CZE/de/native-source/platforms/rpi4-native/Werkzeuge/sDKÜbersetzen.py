#!/usr/bin/env python3
"""verteilungWert SDK에서 freestanding C/C++를 eigen ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def ausführenVorgang():
    strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    strukturanalysierer.add_argument('source', type=Path)
    strukturanalysierer.add_argument('-o', '--output', type=Path, required=True)
    argumentDatenfeld = strukturanalysierer.parse_args()
    entwicklungWerkzeugsatz = Path(__file__).resolve().parent
    ausgabe = argumentDatenfeld.output.resolve()
    ausgabe.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(ausgabe.parent)) as arbeitendPfad:
        zielDatei, ausführdateiDatei = Path(arbeitendPfad) / 'program.o', Path(arbeitendPfad) / 'program.elf'
        istCSprache = argumentDatenfeld.source.suffix == '.c'
        übersetzerWerkzeug = os.environ.get('ARM64_CC', 'clang') if istCSprache else os.environ.get('ARM64_CXX', 'clang++')
        Sprache = ['-std=c11'] if istCSprache else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([übersetzerWerkzeug, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(entwicklungWerkzeugsatz / 'include'), '-c', str(argumentDatenfeld.source.resolve()), '-o', str(zielDatei)] + Sprache)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(entwicklungWerkzeugsatz / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(ausführdateiDatei), str(entwicklungWerkzeugsatz / 'lib/start.o'), str(entwicklungWerkzeugsatz / 'lib/runtime.o'),
            str(zielDatei), str(entwicklungWerkzeugsatz / 'lib/libposix-kor-user.a')])
        os.replace(str(ausführdateiDatei), str(ausgabe))
    print(ausgabe)


if __name__ == '__main__':
    ausführenVorgang()
