#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_plaas=argparse.ArgumentParser(description=__doc__);data_plaas.add_argument('file',type=Path);data_plaas.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=data_plaas.parse_args()
data=argument_ARRAY.file.read_bytes();Naam=argument_ARRAY.name or argument_ARRAY.file.name
if len(data)>16384 or not 1<=len(Naam.encode('utf-8'))<=63 or any(ord(karakterkode)<32 for karakterkode in Naam):data_plaas.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Naam))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
