#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');akumente_arei=자료위치.parse_args()
data=akumente_arei.file.read_bytes();Leina=akumente_arei.name or akumente_arei.file.name
if len(data)>16384 or not 1<=len(Leina.encode('utf-8'))<=63 or any(ord(khouto_ya_tlhaka)<32 for khouto_ya_tlhaka in Leina):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Leina))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
