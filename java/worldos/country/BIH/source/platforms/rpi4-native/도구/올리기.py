#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_низ=자료위치.parse_args()
подаци=аргумент_низ.file.read_bytes();назив=аргумент_низ.name or аргумент_низ.file.name
if len(подаци)>16384 or not 1<=len(назив.encode('utf-8'))<=63 or any(ord(кôд_знака)<32 for кôд_знака in назив):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(назив))
for 순번 in range(0,len(подаци),64):print(подаци[순번:순번+64].hex())
print('.')
