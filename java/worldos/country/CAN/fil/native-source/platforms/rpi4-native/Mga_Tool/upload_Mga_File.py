#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_posisyon=argparse.ArgumentParser(description=__doc__);data_posisyon.add_argument('file',type=Path);data_posisyon.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumento_ARRAY=data_posisyon.parse_args()
data=argumento_ARRAY.file.read_bytes();pangalan=argumento_ARRAY.name or argumento_ARRAY.file.name
if len(data)>16384 or not 1<=len(pangalan.encode('utf-8'))<=63 or any(ord(character_code)<32 for character_code in pangalan):data_posisyon.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(pangalan))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
