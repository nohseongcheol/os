#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
údaje_pozícia=argparse.ArgumentParser(description=__doc__);údaje_pozícia.add_argument('file',type=Path);údaje_pozícia.add_argument('--name',help='guest file name (e.g. package.Class.class)');argument_pole=údaje_pozícia.parse_args()
údaje=argument_pole.file.read_bytes();Názov=argument_pole.name or argument_pole.file.name
if len(údaje)>16384 or not 1<=len(Názov.encode('utf-8'))<=63 or any(ord(bod_kódu)<32 for bod_kódu in Názov):údaje_pozícia.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Názov))
for 순번 in range(0,len(údaje),64):print(údaje[순번:순번+64].hex())
print('.')
