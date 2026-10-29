#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
gegevens_functie=argparse.ArgumentParser(description=__doc__);gegevens_functie.add_argument('file',type=Path);gegevens_functie.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_MATRIX=gegevens_functie.parse_args()
gegevens=argument_MATRIX.file.read_bytes();Naam=argument_MATRIX.name or argument_MATRIX.file.name
if len(gegevens)>16384 or not 1<=len(Naam.encode('utf-8'))<=63 or any(ord(codepoint)<32 for codepoint in Naam):gegevens_functie.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Naam))
for 순번 in range(0,len(gegevens),64):print(gegevens[순번:순번+64].hex())
print('.')
