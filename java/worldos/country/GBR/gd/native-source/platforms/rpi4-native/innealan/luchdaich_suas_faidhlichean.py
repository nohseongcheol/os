#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dàta_suidhich=argparse.ArgumentParser(description=__doc__);dàta_suidhich.add_argument('file',type=Path);dàta_suidhich.add_argument('--name',help='guest file name (e.g. package.Class.class)');argamaid_ARRAY=dàta_suidhich.parse_args()
dàta=argamaid_ARRAY.file.read_bytes();Ainm=argamaid_ARRAY.name or argamaid_ARRAY.file.name
if len(dàta)>16384 or not 1<=len(Ainm.encode('utf-8'))<=63 or any(ord(còd_a_charactair)<32 for còd_a_charactair in Ainm):dàta_suidhich.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ainm))
for 순번 in range(0,len(dàta),64):print(dàta[순번:순번+64].hex())
print('.')
