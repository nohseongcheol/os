#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=자료위치.parse_args()
maglumat=argument_ARRAY.file.read_bytes();Ad=argument_ARRAY.name or argument_ARRAY.file.name
if len(maglumat)>16384 or not 1<=len(Ad.encode('utf-8'))<=63 or any(ord(nyşanyň_kody)<32 for nyşanyň_kody in Ad):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ad))
for 순번 in range(0,len(maglumat),64):print(maglumat[순번:순번+64].hex())
print('.')
