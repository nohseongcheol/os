#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
gögn_staða=argparse.ArgumentParser(description=__doc__);gögn_staða.add_argument('file',type=Path);gögn_staða.add_argument('--name',help='guest file name (e.g. package.Class.class)');frumbreyta_ARRAY=gögn_staða.parse_args()
gögn=frumbreyta_ARRAY.file.read_bytes();Heiti=frumbreyta_ARRAY.name or frumbreyta_ARRAY.file.name
if len(gögn)>16384 or not 1<=len(Heiti.encode('utf-8'))<=63 or any(ord(stafkóði)<32 for stafkóði in Heiti):gögn_staða.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Heiti))
for 순번 in range(0,len(gögn),64):print(gögn[순번:순번+64].hex())
print('.')
