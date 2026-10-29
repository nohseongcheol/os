#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');hoja_ARRAY=자료위치.parse_args()
data=hoja_ARRAY.file.read_bytes();Jina=hoja_ARRAY.name or hoja_ARRAY.file.name
if len(data)>16384 or not 1<=len(Jina.encode('utf-8'))<=63 or any(ord(msimbo_wa_kibambo)<32 for msimbo_wa_kibambo in Jina):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Jina))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
