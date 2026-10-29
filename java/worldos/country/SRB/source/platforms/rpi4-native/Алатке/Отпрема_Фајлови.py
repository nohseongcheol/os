#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
подаци_позиција=argparse.ArgumentParser(description=__doc__);подаци_позиција.add_argument('file',type=Path);подаци_позиција.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_низ=подаци_позиција.parse_args()
подаци=аргумент_низ.file.read_bytes();Назив=аргумент_низ.name or аргумент_низ.file.name
if len(подаци)>16384 or not 1<=len(Назив.encode('utf-8'))<=63 or any(ord(кôд_знака)<32 for кôд_знака in Назив):подаци_позиција.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Назив))
for 순번 in range(0,len(подаци),64):print(подаци[순번:순번+64].hex())
print('.')
