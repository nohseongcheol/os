#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
δεδομένα_θέση=argparse.ArgumentParser(description=__doc__);δεδομένα_θέση.add_argument('file',type=Path);δεδομένα_θέση.add_argument('--name',help='guest file name (e.g. package.Class.class)');όρισμα_πίνακας=δεδομένα_θέση.parse_args()
δεδομένα=όρισμα_πίνακας.file.read_bytes();Όνομα=όρισμα_πίνακας.name or όρισμα_πίνακας.file.name
if len(δεδομένα)>16384 or not 1<=len(Όνομα.encode('utf-8'))<=63 or any(ord(σημείο_κώδικα)<32 for σημείο_κώδικα in Όνομα):δεδομένα_θέση.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Όνομα))
for 순번 in range(0,len(δεδομένα),64):print(δεδομένα[순번:순번+64].hex())
print('.')
