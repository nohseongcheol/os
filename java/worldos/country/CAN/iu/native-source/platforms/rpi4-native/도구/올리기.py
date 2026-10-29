#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');aturniqarnirainiq_array=자료위치.parse_args()
titiqqat=aturniqarnirainiq_array.file.read_bytes();atiq=aturniqarnirainiq_array.name or aturniqarnirainiq_array.file.name
if len(titiqqat)>16384 or not 1<=len(atiq.encode('utf-8'))<=63 or any(ord(immikkuuqtumut_nalunaikkut)<32 for immikkuuqtumut_nalunaikkut in atiq):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(atiq))
for 순번 in range(0,len(titiqqat),64):print(titiqqat[순번:순번+64].hex())
print('.')
