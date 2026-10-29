#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ingingo_ARRAY=자료위치.parse_args()
amakurushingiro=ingingo_ARRAY.file.read_bytes();Izina=ingingo_ARRAY.name or ingingo_ARRAY.file.name
if len(amakurushingiro)>16384 or not 1<=len(Izina.encode('utf-8'))<=63 or any(ord(문자값)<32 for 문자값 in Izina):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Izina))
for 순번 in range(0,len(amakurushingiro),64):print(amakurushingiro[순번:순번+64].hex())
print('.')
