#!/usr/bin/env python3
"""distribuição_VALOR SDK에서 freestanding C/C++를 nativo ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def iniciar():
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument('source', type=Path)
    analisador.add_argument('-o', '--output', type=Path, required=True)
    argumento_MATRIZ = analisador.parse_args()
    kit_de_desenvolvimento = Path(__file__).resolve().parent
    saída = argumento_MATRIZ.output.resolve()
    saída.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(saída.parent)) as 작업경로:
        arquivo_de_destino, executável = Path(작업경로) / 'program.o', Path(작업경로) / 'program.elf'
        TI_C_Idioma = argumento_MATRIZ.source.suffix == '.c'
        compilador_ferramenta = os.environ.get('ARM64_CC', 'clang') if TI_C_Idioma else os.environ.get('ARM64_CXX', 'clang++')
        Idioma = ['-std=c11'] if TI_C_Idioma else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([compilador_ferramenta, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(kit_de_desenvolvimento / 'include'), '-c', str(argumento_MATRIZ.source.resolve()), '-o', str(arquivo_de_destino)] + Idioma)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(kit_de_desenvolvimento / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(executável), str(kit_de_desenvolvimento / 'lib/start.o'), str(kit_de_desenvolvimento / 'lib/runtime.o'),
            str(arquivo_de_destino), str(kit_de_desenvolvimento / 'lib/libposix-kor-user.a')])
        os.replace(str(executável), str(saída))
    print(saída)


if __name__ == '__main__':
    iniciar()
