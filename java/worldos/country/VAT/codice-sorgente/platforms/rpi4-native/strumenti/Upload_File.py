#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dati_funzione=argparse.ArgumentParser(description=__doc__);dati_funzione.add_argument('file',type=Path);dati_funzione.add_argument('--name',help='guest file name (e.g. package.Class.class)');argomento_array=dati_funzione.parse_args()
dati=argomento_array.file.read_bytes();Nome=argomento_array.name or argomento_array.file.name
if len(dati)>16384 or not 1<=len(Nome.encode('utf-8'))<=63 or any(ord(punto_di_codice)<32 for punto_di_codice in Nome):dati_funzione.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nome))
for 순번 in range(0,len(dati),64):print(dati[순번:순번+64].hex())
print('.')
