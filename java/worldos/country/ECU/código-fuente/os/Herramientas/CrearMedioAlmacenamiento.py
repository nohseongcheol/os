#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 valorAlmacenar 매체를 만든다. 기존 Archivo/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def crearEntradaElemento(ruta):
    with Path(ruta).open('xb') as Salida:
        valorCabecera = bytearray(512)
        struct.pack_into('<8sII', valorCabecera, 0, b'JKSTORE1', 2048, 0x3153464a)
        Salida.write(valorCabecera)
        Salida.truncate(2048 * 512)

if __name__ == '__main__':
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('ruta')
    argumentos = Analizador.parse_args()
    crearEntradaElemento(argumentos.ruta)
