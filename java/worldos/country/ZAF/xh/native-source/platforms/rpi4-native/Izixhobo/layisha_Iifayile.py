#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');isiniki_myalelo_ULUHLU=자료위치.parse_args()
iingcombolo=isiniki_myalelo_ULUHLU.file.read_bytes();Igama=isiniki_myalelo_ULUHLU.name or isiniki_myalelo_ULUHLU.file.name
if len(iingcombolo)>16384 or not 1<=len(Igama.encode('utf-8'))<=63 or any(ord(ikhowudi_yekharakhtha)<32 for ikhowudi_yekharakhtha in Igama):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Igama))
for 순번 in range(0,len(iingcombolo),64):print(iingcombolo[순번:순번+64].hex())
print('.')
