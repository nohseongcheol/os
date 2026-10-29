#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
datenPosition=argparse.ArgumentParser(description=__doc__);datenPosition.add_argument('file',type=Path);datenPosition.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumentDatenfeld=datenPosition.parse_args()
Daten=argumentDatenfeld.file.read_bytes();Name=argumentDatenfeld.name or argumentDatenfeld.file.name
if len(Daten)>16384 or not 1<=len(Name.encode('utf-8'))<=63 or any(ord(zeichenKode)<32 for zeichenKode in Name):datenPosition.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Name))
for ordnungszahlIndex in range(0,len(Daten),64):print(Daten[ordnungszahlIndex:ordnungszahlIndex+64].hex())
print('.')
