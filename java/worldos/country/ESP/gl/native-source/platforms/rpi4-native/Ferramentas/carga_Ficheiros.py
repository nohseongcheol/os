#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
datos_cargo=argparse.ArgumentParser(description=__doc__);datos_cargo.add_argument('file',type=Path);datos_cargo.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumento_MATRIZ=datos_cargo.parse_args()
datos=argumento_MATRIZ.file.read_bytes();Nome=argumento_MATRIZ.name or argumento_MATRIZ.file.name
if len(datos)>16384 or not 1<=len(Nome.encode('utf-8'))<=63 or any(ord(código_de_carácter)<32 for código_de_carácter in Nome):datos_cargo.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nome))
for 순번 in range(0,len(datos),64):print(datos[순번:순번+64].hex())
print('.')
