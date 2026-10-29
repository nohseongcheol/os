#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_safle=argparse.ArgumentParser(description=__doc__);data_safle.add_argument('file',type=Path);data_safle.add_argument('--name',help='guest file name (e.g. package.Class.class)');arg_ARAE=data_safle.parse_args()
data=arg_ARAE.file.read_bytes();Enw=arg_ARAE.name or arg_ARAE.file.name
if len(data)>16384 or not 1<=len(Enw.encode('utf-8'))<=63 or any(ord(cod_nod)<32 for cod_nod in Enw):data_safle.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Enw))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
