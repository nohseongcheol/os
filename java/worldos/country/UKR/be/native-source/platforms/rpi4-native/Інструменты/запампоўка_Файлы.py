#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_масіў=자료위치.parse_args()
дадзеныя=аргумент_масіў.file.read_bytes();Назва=аргумент_масіў.name or аргумент_масіў.file.name
if len(дадзеныя)>16384 or not 1<=len(Назва.encode('utf-8'))<=63 or any(ord(код_сімвала)<32 for код_сімвала in Назва):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Назва))
for 순번 in range(0,len(дадзеныя),64):print(дадзеныя[순번:순번+64].hex())
print('.')
