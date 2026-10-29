#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ᏗᏓᎦᏘᎸᏍᏗ_array=자료위치.parse_args()
ᎦᏟᏌᏅᎯ=ᏗᏓᎦᏘᎸᏍᏗ_array.file.read_bytes();ᏚᏙᎥᎢ=ᏗᏓᎦᏘᎸᏍᏗ_array.name or ᏗᏓᎦᏘᎸᏍᏗ_array.file.name
if len(ᎦᏟᏌᏅᎯ)>16384 or not 1<=len(ᏚᏙᎥᎢ.encode('utf-8'))<=63 or any(ord(문자값)<32 for 문자값 in ᏚᏙᎥᎢ):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ᏚᏙᎥᎢ))
for 순번 in range(0,len(ᎦᏟᏌᏅᎯ),64):print(ᎦᏟᏌᏅᎯ[순번:순번+64].hex())
print('.')
