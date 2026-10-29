#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
деректер_лауазым=argparse.ArgumentParser(description=__doc__);деректер_лауазым.add_argument('file',type=Path);деректер_лауазым.add_argument('--name',help='guest file name (e.g. package.Class.class)');аргумент_массив=деректер_лауазым.parse_args()
деректер=аргумент_массив.file.read_bytes();Аты=аргумент_массив.name or аргумент_массив.file.name
if len(деректер)>16384 or not 1<=len(Аты.encode('utf-8'))<=63 or any(ord(таңба_коды)<32 for таңба_коды in Аты):деректер_лауазым.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Аты))
for 순번 in range(0,len(деректер),64):print(деректер[순번:순번+64].hex())
print('.')
