#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_pozice=argparse.ArgumentParser(description=__doc__);data_pozice.add_argument('file',type=Path);data_pozice.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_pole=data_pozice.parse_args()
data=argument_pole.file.read_bytes();Název=argument_pole.name or argument_pole.file.name
if len(data)>16384 or not 1<=len(Název.encode('utf-8'))<=63 or any(ord(bod_kódu)<32 for bod_kódu in Název):data_pozice.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Název))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
