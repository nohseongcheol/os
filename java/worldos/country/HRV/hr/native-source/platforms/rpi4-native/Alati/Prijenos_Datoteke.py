#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
podaci_položaj=argparse.ArgumentParser(description=__doc__);podaci_položaj.add_argument('file',type=Path);podaci_položaj.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=podaci_položaj.parse_args()
podaci=argument_ARRAY.file.read_bytes();Ime=argument_ARRAY.name or argument_ARRAY.file.name
if len(podaci)>16384 or not 1<=len(Ime.encode('utf-8'))<=63 or any(ord(kodna_točka)<32 for kodna_točka in Ime):podaci_položaj.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ime))
for 순번 in range(0,len(podaci),64):print(podaci[순번:순번+64].hex())
print('.')
