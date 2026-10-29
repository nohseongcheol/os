#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');Tubalin_aiki_TSARI=자료위치.parse_args()
Tarin_bayani=Tubalin_aiki_TSARI.file.read_bytes();Suna=Tubalin_aiki_TSARI.name or Tubalin_aiki_TSARI.file.name
if len(Tarin_bayani)>16384 or not 1<=len(Suna.encode('utf-8'))<=63 or any(ord(Lambar_sirrin_harafi)<32 for Lambar_sirrin_harafi in Suna):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Suna))
for 순번 in range(0,len(Tarin_bayani),64):print(Tarin_bayani[순번:순번+64].hex())
print('.')
