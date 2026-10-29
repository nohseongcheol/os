#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
بيانات_منصب=argparse.ArgumentParser(description=__doc__);بيانات_منصب.add_argument('file',type=Path);بيانات_منصب.add_argument('--name',help='guest file name (e.g. package.Class.class)');وسيطة_صفيف=بيانات_منصب.parse_args()
بيانات=وسيطة_صفيف.file.read_bytes();اسم=وسيطة_صفيف.name or وسيطة_صفيف.file.name
if len(بيانات)>16384 or not 1<=len(اسم.encode('utf-8'))<=63 or any(ord(رمز_الحرف)<32 for رمز_الحرف in اسم):بيانات_منصب.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(اسم))
for 순번 in range(0,len(بيانات),64):print(بيانات[순번:순번+64].hex())
print('.')
