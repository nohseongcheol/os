#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');دلیل_ایرے=자료위치.parse_args()
کوائف=دلیل_ایرے.file.read_bytes();ناں=دلیل_ایرے.name or دلیل_ایرے.file.name
if len(کوائف)>16384 or not 1<=len(ناں.encode('utf-8'))<=63 or any(ord(کیریکٹر_کوڈ)<32 for کیریکٹر_کوڈ in ناں):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ناں))
for 순번 in range(0,len(کوائف),64):print(کوائف[순번:순번+64].hex())
print('.')
