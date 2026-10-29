#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dados_cargo=argparse.ArgumentParser(description=__doc__);dados_cargo.add_argument('file',type=Path);dados_cargo.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumento_MATRIZ=dados_cargo.parse_args()
dados=argumento_MATRIZ.file.read_bytes();Nome=argumento_MATRIZ.name or argumento_MATRIZ.file.name
if len(dados)>16384 or not 1<=len(Nome.encode('utf-8'))<=63 or any(ord(ponto_de_código)<32 for ponto_de_código in Nome):dados_cargo.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nome))
for 순번 in range(0,len(dados),64):print(dados[순번:순번+64].hex())
print('.')
