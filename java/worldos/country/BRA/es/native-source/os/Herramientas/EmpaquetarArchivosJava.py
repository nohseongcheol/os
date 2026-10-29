#!/usr/bin/env python3
"""명시한 Java árbolFuente/valorClase 파일을 Arranque 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def EmpaquetarEjecutables(listaEntradas):
    entradasArchivo = []
    listaNombres = {'Hello.java'}
    nombresExplícito = set()
    for valorEntradaElemento in listaEntradas:
        if '=' not in valorEntradaElemento:
            raise ValueError('expected NAME=PATH: ' + valorEntradaElemento)
        nombre, ruta = valorEntradaElemento.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', nombre) or nombre in nombresExplícito:
            raise ValueError('invalid or duplicate file name: ' + nombre)
        nombresExplícito.add(nombre)
        listaNombres.add(nombre)
        Datos = Path(ruta).read_bytes()
        if len(Datos) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + nombre)
        entradasArchivo.append((nombre.encode('ascii'), Datos))
    if len(listaNombres) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    resultado = bytearray(struct.pack('<4sI', b'JKJF', len(entradasArchivo)))
    resultado.extend(bytes(72 * len(entradasArchivo)))
    for númeroValor, (nombre, Datos) in enumerate(entradasArchivo):
        struct.pack_into('<64sII', resultado, 8 + númeroValor * 72, nombre, len(resultado), len(Datos))
        resultado.extend(Datos)
    return bytes(resultado)


if __name__ == '__main__':
    analizarValor = argparse.ArgumentParser(description=__doc__)
    analizarValor.add_argument('-o', required=True)
    analizarValor.add_argument('files', nargs='*', help='NAME=PATH')
    argumentos = analizarValor.parse_args()
    try:
        Datos = EmpaquetarEjecutables(argumentos.files)
        valorDestino = Path(argumentos.o)
        if not valorDestino.exists() or valorDestino.read_bytes() != Datos:
            valorTemporal = valorDestino.with_name(valorDestino.name + '.tmp')
            valorTemporal.write_bytes(Datos)
            valorTemporal.replace(valorDestino)
    except (ValueError, OSError) as error:
        analizarValor.error(str(error))
