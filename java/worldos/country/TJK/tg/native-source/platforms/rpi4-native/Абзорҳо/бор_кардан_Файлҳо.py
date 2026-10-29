#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_қатор=자료위치.parse_args()
иттилоот=аргумент_қатор.file.read_bytes();Ном=аргумент_қатор.name or аргумент_қатор.file.name
if len(иттилоот)>16384 or not 1<=len(Ном.encode('utf-8'))<=63 or any(ord(рамзи_аломат)<32 for рамзи_аломат in Ном):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ном))
for 순번 in range(0,len(иттилоот),64):print(иттилоот[순번:순번+64].hex())
print('.')
