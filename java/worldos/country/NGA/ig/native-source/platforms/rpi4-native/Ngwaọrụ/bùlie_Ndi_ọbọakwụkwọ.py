#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');agụment_MKPOKỌTA=자료위치.parse_args()
datà=agụment_MKPOKỌTA.file.read_bytes();Aha=agụment_MKPOKỌTA.name or agụment_MKPOKỌTA.file.name
if len(datà)>16384 or not 1<=len(Aha.encode('utf-8'))<=63 or any(ord(koòdù_nkeakàrà)<32 for koòdù_nkeakàrà in Aha):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Aha))
for 순번 in range(0,len(datà),64):print(datà[순번:순번+64].hex())
print('.')
