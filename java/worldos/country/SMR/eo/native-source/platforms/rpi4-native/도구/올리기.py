#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');인수배열=자료위치.parse_args()
자료=인수배열.file.read_bytes();Nomo=인수배열.name or 인수배열.file.name
if len(자료)>16384 or not 1<=len(Nomo.encode('utf-8'))<=63 or any(ord(문자값)<32 for 문자값 in Nomo):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nomo))
for 순번 in range(0,len(자료),64):print(자료[순번:순번+64].hex())
print('.')
