#!/usr/bin/env python3
"""valorDistribución SDK에서 freestanding C/C++를 propio ABI ELF64로 컴파일한다."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def ponerEnMarcha():
    analizador = argparse.ArgumentParser(description=__doc__)
    analizador.add_argument('source', type=Path)
    analizador.add_argument('-o', '--output', type=Path, required=True)
    arregloArgumento = analizador.parse_args()
    juegoHerramientasDesarrollo = Path(__file__).resolve().parent
    salida = arregloArgumento.output.resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jkoros-sdk-', dir=str(salida.parent)) as rutaTrabajoEnCurso:
        archivoDestino, archivoCódigoEjecutable = Path(rutaTrabajoEnCurso) / 'program.o', Path(rutaTrabajoEnCurso) / 'program.elf'
        esLenguaC = arregloArgumento.source.suffix == '.c'
        herramientaCompilador = os.environ.get('ARM64_CC', 'clang') if esLenguaC else os.environ.get('ARM64_CXX', 'clang++')
        Lengua = ['-std=c11'] if esLenguaC else ['-std=c++11', '-fno-exceptions', '-fno-rtti']
        subprocess.check_call([herramientaCompilador, '--target=aarch64-none-elf',
            '-mcpu=cortex-a72', '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables',
            '-O2', '-I', str(juegoHerramientasDesarrollo / 'include'), '-c', str(arregloArgumento.source.resolve()), '-o', str(archivoDestino)] + Lengua)
        subprocess.check_call([os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld'), '-T', str(juegoHerramientasDesarrollo / 'user.ld'),
            '-z', 'max-page-size=4096', '-o', str(archivoCódigoEjecutable), str(juegoHerramientasDesarrollo / 'lib/start.o'), str(juegoHerramientasDesarrollo / 'lib/runtime.o'),
            str(archivoDestino), str(juegoHerramientasDesarrollo / 'lib/libposix-kor-user.a')])
        os.replace(str(archivoCódigoEjecutable), str(salida))
    print(salida)


if __name__ == '__main__':
    ponerEnMarcha()
