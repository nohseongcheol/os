#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_toimi=argparse.ArgumentParser(description=__doc__);data_toimi.add_argument('file',type=Path);data_toimi.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumentti_MATRIISI=data_toimi.parse_args()
data=argumentti_MATRIISI.file.read_bytes();Nimi=argumentti_MATRIISI.name or argumentti_MATRIISI.file.name
if len(data)>16384 or not 1<=len(Nimi.encode('utf-8'))<=63 or any(ord(merkkikoodi)<32 for merkkikoodi in Nimi):data_toimi.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nimi))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
