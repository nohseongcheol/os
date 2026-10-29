#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');i_agumenti_AMALUNGU_AFANAYO=자료위치.parse_args()
imininingwane=i_agumenti_AMALUNGU_AFANAYO.file.read_bytes();Igama=i_agumenti_AMALUNGU_AFANAYO.name or i_agumenti_AMALUNGU_AFANAYO.file.name
if len(imininingwane)>16384 or not 1<=len(Igama.encode('utf-8'))<=63 or any(ord(ikhodi_yohlamvu)<32 for ikhodi_yohlamvu in Igama):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Igama))
for 순번 in range(0,len(imininingwane),64):print(imininingwane[순번:순번+64].hex())
print('.')
