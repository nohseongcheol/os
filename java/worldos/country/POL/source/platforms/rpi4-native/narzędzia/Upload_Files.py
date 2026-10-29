#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dane_stanowisko=argparse.ArgumentParser(description=__doc__);dane_stanowisko.add_argument('file',type=Path);dane_stanowisko.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_TABLICA=dane_stanowisko.parse_args()
dane=argument_TABLICA.file.read_bytes();Nazwa=argument_TABLICA.name or argument_TABLICA.file.name
if len(dane)>16384 or not 1<=len(Nazwa.encode('utf-8'))<=63 or any(ord(kod_znaku)<32 for kod_znaku in Nazwa):dane_stanowisko.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nazwa))
for 순번 in range(0,len(dane),64):print(dane[순번:순번+64].hex())
print('.')
