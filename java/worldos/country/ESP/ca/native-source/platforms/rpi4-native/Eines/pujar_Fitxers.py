#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
dades_càrrec=argparse.ArgumentParser(description=__doc__);dades_càrrec.add_argument('file',type=Path);dades_càrrec.add_argument('--name',help='guest file name (e.g. package.Class.class)');arg_MATRIU=dades_càrrec.parse_args()
dades=arg_MATRIU.file.read_bytes();Nom=arg_MATRIU.name or arg_MATRIU.file.name
if len(dades)>16384 or not 1<=len(Nom.encode('utf-8'))<=63 or any(ord(codi_de_caràcter)<32 for codi_de_caràcter in Nom):dades_càrrec.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nom))
for 순번 in range(0,len(dades),64):print(dades[순번:순번+64].hex())
print('.')
