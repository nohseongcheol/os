#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dati_amats=argparse.ArgumentParser(description=__doc__);dati_amats.add_argument('file',type=Path);dati_amats.add_argument('--name',help='guest file name (e.g. package.Class.class)');arg_ARRAY=dati_amats.parse_args()
dati=arg_ARRAY.file.read_bytes();Nosaukums=arg_ARRAY.name or arg_ARRAY.file.name
if len(dati)>16384 or not 1<=len(Nosaukums.encode('utf-8'))<=63 or any(ord(koda_punkts)<32 for koda_punkts in Nosaukums):dati_amats.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nosaukums))
for 순번 in range(0,len(dati),64):print(dati[순번:순번+64].hex())
print('.')
