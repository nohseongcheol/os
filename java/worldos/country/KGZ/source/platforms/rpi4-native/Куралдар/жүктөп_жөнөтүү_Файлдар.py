#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_МАССИВ=자료위치.parse_args()
берилмелер=аргумент_МАССИВ.file.read_bytes();Аты=аргумент_МАССИВ.name or аргумент_МАССИВ.file.name
if len(берилмелер)>16384 or not 1<=len(Аты.encode('utf-8'))<=63 or any(ord(символ_коду)<32 for символ_коду in Аты):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Аты))
for 순번 in range(0,len(берилмелер),64):print(берилмелер[순번:순번+64].hex())
print('.')
