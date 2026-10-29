#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
мәгълүмат_урнаштыру=argparse.ArgumentParser(description=__doc__);мәгълүмат_урнаштыру.add_argument('file',type=Path);мәгълүмат_урнаштыру.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_МАССИВ=мәгълүмат_урнаштыру.parse_args()
мәгълүмат=аргумент_МАССИВ.file.read_bytes();исем=аргумент_МАССИВ.name or аргумент_МАССИВ.file.name
if len(мәгълүмат)>16384 or not 1<=len(исем.encode('utf-8'))<=63 or any(ord(символ_коды)<32 for символ_коды in исем):мәгълүмат_урнаштыру.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(исем))
for 순번 in range(0,len(мәгълүмат),64):print(мәгълүмат[순번:순번+64].hex())
print('.')
