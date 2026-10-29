#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
date_poziție=argparse.ArgumentParser(description=__doc__);date_poziție.add_argument('file',type=Path);date_poziție.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=date_poziție.parse_args()
date=argument_ARRAY.file.read_bytes();Nume=argument_ARRAY.name or argument_ARRAY.file.name
if len(date)>16384 or not 1<=len(Nume.encode('utf-8'))<=63 or any(ord(cod_caracter)<32 for cod_caracter in Nume):date_poziție.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nume))
for 순번 in range(0,len(date),64):print(date[순번:순번+64].hex())
print('.')
