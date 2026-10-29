#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
Daten_positionéieren=argparse.ArgumentParser(description=__doc__);Daten_positionéieren.add_argument('file',type=Path);Daten_positionéieren.add_argument('--name',help='guest file name (e.g. package.Class.class)');Argument_ARRAY=Daten_positionéieren.parse_args()
Daten=Argument_ARRAY.file.read_bytes();Numm=Argument_ARRAY.name or Argument_ARRAY.file.name
if len(Daten)>16384 or not 1<=len(Numm.encode('utf-8'))<=63 or any(ord(Zeechecode)<32 for Zeechecode in Numm):Daten_positionéieren.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Numm))
for 순번 in range(0,len(Daten),64):print(Daten[순번:순번+64].hex())
print('.')
