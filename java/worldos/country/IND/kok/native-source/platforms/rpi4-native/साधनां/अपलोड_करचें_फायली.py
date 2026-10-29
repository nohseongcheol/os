#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
डेटा_स्थिती=argparse.ArgumentParser(description=__doc__);डेटा_स्थिती.add_argument('file',type=Path);डेटा_स्थिती.add_argument('--name',help='guest file name (e.g. package.Class.class)');युक्तीवाद_क्रम=डेटा_स्थिती.parse_args()
डेटा=युक्तीवाद_क्रम.file.read_bytes();नांव=युक्तीवाद_क्रम.name or युक्तीवाद_क्रम.file.name
if len(डेटा)>16384 or not 1<=len(नांव.encode('utf-8'))<=63 or any(ord(वर्ण_कोड)<32 for वर्ण_कोड in नांव):डेटा_स्थिती.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(नांव))
for 순번 in range(0,len(डेटा),64):print(डेटा[순번:순번+64].hex())
print('.')
