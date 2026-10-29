#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dataPosition=argparse.ArgumentParser(description=__doc__);dataPosition.add_argument('file',type=Path);dataPosition.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumentArray=dataPosition.parse_args()
data=argumentArray.file.read_bytes();name=argumentArray.name or argumentArray.file.name
if len(data)>16384 or not 1<=len(name.encode('utf-8'))<=63 or any(ord(characterCode)<32 for characterCode in name):dataPosition.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(name))
for ordinalIndex in range(0,len(data),64):print(data[ordinalIndex:ordinalIndex+64].hex())
print('.')
