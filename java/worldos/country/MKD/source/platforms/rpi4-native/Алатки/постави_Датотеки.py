#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
податоци_позиционирање=argparse.ArgumentParser(description=__doc__);податоци_позиционирање.add_argument('file',type=Path);податоци_позиционирање.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_низа=податоци_позиционирање.parse_args()
податоци=аргумент_низа.file.read_bytes();Име=аргумент_низа.name or аргумент_низа.file.name
if len(податоци)>16384 or not 1<=len(Име.encode('utf-8'))<=63 or any(ord(кодна_точка)<32 for кодна_точка in Име):податоци_позиционирање.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Име))
for 순번 in range(0,len(податоци),64):print(податоци[순번:순번+64].hex())
print('.')
