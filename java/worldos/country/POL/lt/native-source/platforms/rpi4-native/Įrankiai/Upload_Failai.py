#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
duomenys_padėtis=argparse.ArgumentParser(description=__doc__);duomenys_padėtis.add_argument('file',type=Path);duomenys_padėtis.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumentas_ARRAY=duomenys_padėtis.parse_args()
duomenys=argumentas_ARRAY.file.read_bytes();Pavadinimas_2=argumentas_ARRAY.name or argumentas_ARRAY.file.name
if len(duomenys)>16384 or not 1<=len(Pavadinimas_2.encode('utf-8'))<=63 or any(ord(simbolio_kodas)<32 for simbolio_kodas in Pavadinimas_2):duomenys_padėtis.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Pavadinimas_2))
for 순번 in range(0,len(duomenys),64):print(duomenys[순번:순번+64].hex())
print('.')
