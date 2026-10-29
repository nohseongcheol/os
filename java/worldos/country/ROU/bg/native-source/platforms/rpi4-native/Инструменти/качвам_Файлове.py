#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
данни_позиция=argparse.ArgumentParser(description=__doc__);данни_позиция.add_argument('file',type=Path);данни_позиция.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_масив=данни_позиция.parse_args()
данни=аргумент_масив.file.read_bytes();Име=аргумент_масив.name or аргумент_масив.file.name
if len(данни)>16384 or not 1<=len(Име.encode('utf-8'))<=63 or any(ord(знаков_код)<32 for знаков_код in Име):данни_позиция.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Име))
for 순번 in range(0,len(данни),64):print(данни[순번:순번+64].hex())
print('.')
