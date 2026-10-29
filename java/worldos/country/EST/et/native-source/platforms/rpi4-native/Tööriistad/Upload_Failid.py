#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
andmed_ametikoht=argparse.ArgumentParser(description=__doc__);andmed_ametikoht.add_argument('file',type=Path);andmed_ametikoht.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=andmed_ametikoht.parse_args()
andmed=argument_ARRAY.file.read_bytes();Nimi_2=argument_ARRAY.name or argument_ARRAY.file.name
if len(andmed)>16384 or not 1<=len(Nimi_2.encode('utf-8'))<=63 or any(ord(koodipunkt)<32 for koodipunkt in Nimi_2):andmed_ametikoht.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nimi_2))
for 순번 in range(0,len(andmed),64):print(andmed[순번:순번+64].hex())
print('.')
