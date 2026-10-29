#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_олонлог=자료위치.parse_args()
өгөгдөл=аргумент_олонлог.file.read_bytes();Нэр=аргумент_олонлог.name or аргумент_олонлог.file.name
if len(өгөгдөл)>16384 or not 1<=len(Нэр.encode('utf-8'))<=63 or any(ord(тэмдэгтийн_код)<32 for тэмдэгтийн_код in Нэр):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Нэр))
for 순번 in range(0,len(өгөгдөл),64):print(өгөгдөл[순번:순번+64].hex())
print('.')
