#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
adat_pozíció=argparse.ArgumentParser(description=__doc__);adat_pozíció.add_argument('file',type=Path);adat_pozíció.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumentum_TÖMB=adat_pozíció.parse_args()
adat=argumentum_TÖMB.file.read_bytes();Név=argumentum_TÖMB.name or argumentum_TÖMB.file.name
if len(adat)>16384 or not 1<=len(Név.encode('utf-8'))<=63 or any(ord(kódpont)<32 for kódpont in Név):adat_pozíció.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Név))
for 순번 in range(0,len(adat),64):print(adat[순번:순번+64].hex())
print('.')
