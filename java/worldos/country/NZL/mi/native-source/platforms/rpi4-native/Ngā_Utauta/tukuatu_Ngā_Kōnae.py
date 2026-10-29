#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
raraunga_tūranga=argparse.ArgumentParser(description=__doc__);raraunga_tūranga.add_argument('file',type=Path);raraunga_tūranga.add_argument('--name',help='guest file name (e.g. package.Class.class)');tohenga_HUĀNGA=raraunga_tūranga.parse_args()
raraunga=tohenga_HUĀNGA.file.read_bytes();Ingoa=tohenga_HUĀNGA.name or tohenga_HUĀNGA.file.name
if len(raraunga)>16384 or not 1<=len(Ingoa.encode('utf-8'))<=63 or any(ord(waehere_pūāhua)<32 for waehere_pūāhua in Ingoa):raraunga_tūranga.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ingoa))
for 순번 in range(0,len(raraunga),64):print(raraunga[순번:순번+64].hex())
print('.')
