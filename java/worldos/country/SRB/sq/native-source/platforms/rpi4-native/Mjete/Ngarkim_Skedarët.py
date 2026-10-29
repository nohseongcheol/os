#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
të_dhëna_pozicioni=argparse.ArgumentParser(description=__doc__);të_dhëna_pozicioni.add_argument('file',type=Path);të_dhëna_pozicioni.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_ARRAY=të_dhëna_pozicioni.parse_args()
të_dhëna=argument_ARRAY.file.read_bytes();Emër=argument_ARRAY.name or argument_ARRAY.file.name
if len(të_dhëna)>16384 or not 1<=len(Emër.encode('utf-8'))<=63 or any(ord(kodi_i_karakterit)<32 for kodi_i_karakterit in Emër):të_dhëna_pozicioni.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Emër))
for 순번 in range(0,len(të_dhëna),64):print(të_dhëna[순번:순번+64].hex())
print('.')
