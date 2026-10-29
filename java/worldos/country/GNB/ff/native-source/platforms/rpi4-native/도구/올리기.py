#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');인수배열=자료위치.parse_args()
keɓe=인수배열.file.read_bytes();innde=인수배열.name or 인수배열.file.name
if len(keɓe)>16384 or not 1<=len(innde.encode('utf-8'))<=63 or any(ord(문자값)<32 for 문자값 in innde):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(innde))
for 순번 in range(0,len(keɓe),64):print(keɓe[순번:순번+64].hex())
print('.')
