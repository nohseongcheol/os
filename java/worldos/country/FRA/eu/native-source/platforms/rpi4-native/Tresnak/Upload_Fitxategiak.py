#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
datuak_kargu=argparse.ArgumentParser(description=__doc__);datuak_kargu.add_argument('file',type=Path);datuak_kargu.add_argument('--name',help='guest file name (e.g. package.Class.class)');arg_matrize=datuak_kargu.parse_args()
datuak=arg_matrize.file.read_bytes();Izena=arg_matrize.name or arg_matrize.file.name
if len(datuak)>16384 or not 1<=len(Izena.encode('utf-8'))<=63 or any(ord(karaktere_kode)<32 for karaktere_kode in Izena):datuak_kargu.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Izena))
for 순번 in range(0,len(datuak),64):print(datuak[순번:순번+64].hex())
print('.')
