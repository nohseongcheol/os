#!/usr/bin/env python3
"""명시한 Java fonte_albero/Corso_VALORE 파일을 avvio_macchina 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def BIND_endpoint(항목들):
    파일들 = []
    이름들 = {'Hello.java'}
    명시 = set()
    for voce_VALORE in 항목들:
        if '=' not in voce_VALORE:
            raise ValueError('expected NAME=PATH: ' + voce_VALORE)
        Nome, percorso = voce_VALORE.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', Nome) or Nome in 명시:
            raise ValueError('invalid or duplicate file name: ' + Nome)
        명시.add(Nome)
        이름들.add(Nome)
        dati = Path(percorso).read_bytes()
        if len(dati) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + Nome)
        파일들.append((Nome.encode('ascii'), dati))
    if len(이름들) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    risultato = bytearray(struct.pack('<4sI', b'JKJF', len(파일들)))
    risultato.extend(bytes(72 * len(파일들)))
    for numero, (Nome, dati) in enumerate(파일들):
        struct.pack_into('<64sII', risultato, 8 + numero * 72, Nome, len(risultato), len(dati))
        risultato.extend(dati)
    return bytes(risultato)


if __name__ == '__main__':
    analizzare_VALORE = argparse.ArgumentParser(description=__doc__)
    analizzare_VALORE.add_argument('-o', required=True)
    analizzare_VALORE.add_argument('files', nargs='*', help='NAME=PATH')
    argomenti = analizzare_VALORE.parse_args()
    try:
        dati = BIND_endpoint(argomenti.files)
        meta_VALORE = Path(argomenti.o)
        if not meta_VALORE.exists() or meta_VALORE.read_bytes() != dati:
            임시 = meta_VALORE.with_name(meta_VALORE.name + '.tmp')
            임시.write_bytes(dati)
            임시.replace(meta_VALORE)
    except (ValueError, OSError) as errore:
        analizzare_VALORE.error(str(errore))
