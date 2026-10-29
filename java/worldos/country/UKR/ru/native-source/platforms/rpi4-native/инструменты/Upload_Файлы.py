#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
данные_позиция=argparse.ArgumentParser(description=__doc__);данные_позиция.add_argument('file',type=Path);данные_позиция.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_МАССИВ=данные_позиция.parse_args()
данные=аргумент_МАССИВ.file.read_bytes();Название=аргумент_МАССИВ.name or аргумент_МАССИВ.file.name
if len(данные)>16384 or not 1<=len(Название.encode('utf-8'))<=63 or any(ord(код_знака)<32 for код_знака in Название):данные_позиция.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Название))
for 순번 in range(0,len(данные),64):print(данные[순번:순번+64].hex())
print('.')
