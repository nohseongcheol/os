#!/usr/bin/env python3
"""명시한 Usuario ELF만 leer 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def EmpaquetarEjecutables():
    analizarValor = argparse.ArgumentParser()
    analizarValor.add_argument('-o', required=True)
    analizarValor.add_argument('files', nargs='+', help='nombre=ELF경로')
    argumentoParámetro = analizarValor.parse_args()
    if len(argumentoParámetro.files) > 32:
        analizarValor.error('Programa valorMáximo 32개')
    listaEntradas = []
    listaNombres = set()
    for valorEntradaElemento in argumentoParámetro.files:
        nombre, ruta = valorEntradaElemento.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', nombre) or nombre in listaNombres:
            analizarValor.error('ejecutarComando 이름이 잘못되었거나 중복됨: ' + nombre)
        listaNombres.add(nombre)
        Datos = Path(ruta).read_bytes()
        if len(Datos) > 2 * 1024 * 1024:
            analizarValor.error('ejecutarComando 파일이 너무 큼')
        listaEntradas.append((nombre.encode(), Datos))
    resultado = bytearray(8 + 24 * len(listaEntradas))
    struct.pack_into('<II', resultado, 0, 0x50414b4a, len(listaEntradas))
    for número, (nombre, Datos) in enumerate(listaEntradas):
        resultado.extend(bytes((-len(resultado)) % 16))
        struct.pack_into('<16sII', resultado, 8 + número * 24, nombre, len(resultado), len(Datos))
        resultado.extend(Datos)
    Path(argumentoParámetro.o).write_bytes(resultado)

if __name__ == '__main__':
    EmpaquetarEjecutables()
