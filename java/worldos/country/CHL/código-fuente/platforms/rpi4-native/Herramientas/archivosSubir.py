#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
posiciónDatos=argparse.ArgumentParser(description=__doc__);posiciónDatos.add_argument('file',type=Path);posiciónDatos.add_argument('--name',help='guest file name (e.g. package.Class.class)');arregloArgumento=posiciónDatos.parse_args()
Datos=arregloArgumento.file.read_bytes();nombre=arregloArgumento.name or arregloArgumento.file.name
if len(Datos)>16384 or not 1<=len(nombre.encode('utf-8'))<=63 or any(ord(códigoCarácter)<32 for códigoCarácter in nombre):posiciónDatos.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(nombre))
for índiceOrdinal in range(0,len(Datos),64):print(Datos[índiceOrdinal:índiceOrdinal+64].hex())
print('.')
