#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
podaci_pozicija=argparse.ArgumentParser(description=__doc__);podaci_pozicija.add_argument('file',type=Path);podaci_pozicija.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_niz=podaci_pozicija.parse_args()
podaci=argument_niz.file.read_bytes();ime=argument_niz.name or argument_niz.file.name
if len(podaci)>16384 or not 1<=len(ime.encode('utf-8'))<=63 or any(ord(kôd_znaka)<32 for kôd_znaka in ime):podaci_pozicija.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ime))
for 순번 in range(0,len(podaci),64):print(podaci[순번:순번+64].hex())
print('.')
