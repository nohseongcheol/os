#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');Thulaganyo_setlhopha=자료위치.parse_args()
tshedimosetso=Thulaganyo_setlhopha.file.read_bytes();leina=Thulaganyo_setlhopha.name or Thulaganyo_setlhopha.file.name
if len(tshedimosetso)>16384 or not 1<=len(leina.encode('utf-8'))<=63 or any(ord(khoutuletshwao)<32 for khoutuletshwao in leina):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(leina))
for 순번 in range(0,len(tshedimosetso),64):print(tshedimosetso[순번:순번+64].hex())
print('.')
