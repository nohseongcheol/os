#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
podatki_položaj=argparse.ArgumentParser(description=__doc__);podatki_položaj.add_argument('file',type=Path);podatki_položaj.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=podatki_položaj.parse_args()
podatki=argument_ARRAY.file.read_bytes();Ime=argument_ARRAY.name or argument_ARRAY.file.name
if len(podatki)>16384 or not 1<=len(Ime.encode('utf-8'))<=63 or any(ord(koda_znaka)<32 for koda_znaka in Ime):podatki_položaj.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ime))
for 순번 in range(0,len(podatki),64):print(podatki[순번:순번+64].hex())
print('.')
