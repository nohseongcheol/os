#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
sonraí_suíomh=argparse.ArgumentParser(description=__doc__);sonraí_suíomh.add_argument('file',type=Path);sonraí_suíomh.add_argument('--name',help='guest file name (e.g. package.Class.class)');argóint_ARRAY=sonraí_suíomh.parse_args()
sonraí=argóint_ARRAY.file.read_bytes();Ainm=argóint_ARRAY.name or argóint_ARRAY.file.name
if len(sonraí)>16384 or not 1<=len(Ainm.encode('utf-8'))<=63 or any(ord(pointe_cóid)<32 for pointe_cóid in Ainm):sonraí_suíomh.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ainm))
for 순번 in range(0,len(sonraí),64):print(sonraí[순번:순번+64].hex())
print('.')
