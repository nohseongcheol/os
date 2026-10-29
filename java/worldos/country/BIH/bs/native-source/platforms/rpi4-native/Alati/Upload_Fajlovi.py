#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
podaci_položaj=argparse.ArgumentParser(description=__doc__);podaci_položaj.add_argument('file',type=Path);podaci_položaj.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_niz=podaci_položaj.parse_args()
podaci=argument_niz.file.read_bytes();Naziv=argument_niz.name or argument_niz.file.name
if len(podaci)>16384 or not 1<=len(Naziv.encode('utf-8'))<=63 or any(ord(kôd_znaka)<32 for kôd_znaka in Naziv):podaci_položaj.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Naziv))
for 순번 in range(0,len(podaci),64):print(podaci[순번:순번+64].hex())
print('.')
