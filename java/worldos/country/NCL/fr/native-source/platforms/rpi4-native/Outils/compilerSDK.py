#!/usr/bin/env python3
"""valeurDistribution SDK에서 freestanding C/C++를 interne ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def lancer():
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument('source', type=Path)
    analyseur.add_argument('-o', '--output', type=Path, required=True)
    tableauArgument = analyseur.parse_args()
    trousseDéveloppement = Path(__file__).resolve().parent
    sortie = tableauArgument.output.resolve()
    sortie.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(sortie.parent)) as cheminTravailEnCours:
        fichierDestination, fichierCodeExécutable = Path(cheminTravailEnCours) / 'program.o', Path(cheminTravailEnCours) / 'program.elf'
        estLangueC = tableauArgument.source.suffix == '.c'
        outilCompilateur = os.environ.get('ARM64_CC', 'clang') if estLangueC else os.environ.get('ARM64_CXX', 'clang++')
        Langue = ['-std=c11'] if estLangueC else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([outilCompilateur, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(trousseDéveloppement / 'include'), '-c', str(tableauArgument.source.resolve()), '-o', str(fichierDestination)] + Langue)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(trousseDéveloppement / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(fichierCodeExécutable), str(trousseDéveloppement / 'lib/start.o'), str(trousseDéveloppement / 'lib/runtime.o'),
            str(fichierDestination), str(trousseDéveloppement / 'lib/libposix-kor-user.a')])
        os.replace(str(fichierCodeExécutable), str(sortie))
    print(sortie)


if __name__ == '__main__':
    lancer()
