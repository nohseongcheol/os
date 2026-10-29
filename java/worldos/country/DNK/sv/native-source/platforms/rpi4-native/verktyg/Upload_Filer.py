#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_placera=argparse.ArgumentParser(description=__doc__);data_placera.add_argument('file',type=Path);data_placera.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_MATRIS=data_placera.parse_args()
data=argument_MATRIS.file.read_bytes();Namn=argument_MATRIS.name or argument_MATRIS.file.name
if len(data)>16384 or not 1<=len(Namn.encode('utf-8'))<=63 or any(ord(kodpunkt)<32 for kodpunkt in Namn):data_placera.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Namn))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
