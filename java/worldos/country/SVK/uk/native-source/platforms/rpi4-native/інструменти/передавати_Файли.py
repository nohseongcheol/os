#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
дані_посада=argparse.ArgumentParser(description=__doc__);дані_посада.add_argument('file',type=Path);дані_посада.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_масив=дані_посада.parse_args()
дані=аргумент_масив.file.read_bytes();Назва=аргумент_масив.name or аргумент_масив.file.name
if len(дані)>16384 or not 1<=len(Назва.encode('utf-8'))<=63 or any(ord(код_символу)<32 for код_символу in Назва):дані_посада.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Назва))
for 순번 in range(0,len(дані),64):print(дані[순번:순번+64].hex())
print('.')
