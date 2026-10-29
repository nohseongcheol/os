#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_plassere=argparse.ArgumentParser(description=__doc__);data_plassere.add_argument('file',type=Path);data_plassere.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=data_plassere.parse_args()
data=argument_ARRAY.file.read_bytes();Namn=argument_ARRAY.name or argument_ARRAY.file.name
if len(data)>16384 or not 1<=len(Namn.encode('utf-8'))<=63 or any(ord(teiknkode)<32 for teiknkode in Namn):data_plassere.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Namn))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
