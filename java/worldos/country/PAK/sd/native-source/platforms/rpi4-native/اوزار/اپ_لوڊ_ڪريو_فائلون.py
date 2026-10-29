#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');دليل_ترتيب=자료위치.parse_args()
ڪوائف=دليل_ترتيب.file.read_bytes();نالو=دليل_ترتيب.name or دليل_ترتيب.file.name
if len(ڪوائف)>16384 or not 1<=len(نالو.encode('utf-8'))<=63 or any(ord(ڪئريڪٽر_ڪوڊ)<32 for ڪئريڪٽر_ڪوڊ in نالو):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(نالو))
for 순번 in range(0,len(ڪوائف),64):print(ڪوائف[순번:순번+64].hex())
print('.')
