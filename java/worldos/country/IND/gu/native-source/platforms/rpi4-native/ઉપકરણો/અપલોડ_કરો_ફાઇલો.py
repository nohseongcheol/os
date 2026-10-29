#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ડેટા_સ્થિતિ=argparse.ArgumentParser(description=__doc__);ડેટા_સ્થિતિ.add_argument('file',type=Path);ડેટા_સ્થિતિ.add_argument('--name',help='guest file name (e.g. package.Class.class)');દલીલ_અરે=ડેટા_સ્થિતિ.parse_args()
ડેટા=દલીલ_અરે.file.read_bytes();નામ=દલીલ_અરે.name or દલીલ_અરે.file.name
if len(ડેટા)>16384 or not 1<=len(નામ.encode('utf-8'))<=63 or any(ord(વર્ણ_કોડ)<32 for વર્ણ_કોડ in નામ):ડેટા_સ્થિતિ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(નામ))
for 순번 in range(0,len(ડેટા),64):print(ડેટા[순번:순번+64].hex())
print('.')
