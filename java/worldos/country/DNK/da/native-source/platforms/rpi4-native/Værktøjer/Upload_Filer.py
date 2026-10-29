#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_placere=argparse.ArgumentParser(description=__doc__);data_placere.add_argument('file',type=Path);data_placere.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_MATRIX=data_placere.parse_args()
data=argument_MATRIX.file.read_bytes();Navn=argument_MATRIX.name or argument_MATRIX.file.name
if len(data)>16384 or not 1<=len(Navn.encode('utf-8'))<=63 or any(ord(tegnkode)<32 for tegnkode in Navn):data_placere.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Navn))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
