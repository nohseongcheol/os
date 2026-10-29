#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');Tegtal_TABLO=자료위치.parse_args()
mbir=Tegtal_TABLO.file.read_bytes();tur_253d1510=Tegtal_TABLO.name or Tegtal_TABLO.file.name
if len(mbir)>16384 or not 1<=len(tur_253d1510.encode('utf-8'))<=63 or any(ord(kotu_araf)<32 for kotu_araf in tur_253d1510):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(tur_253d1510))
for 순번 in range(0,len(mbir),64):print(mbir[순번:순번+64].hex())
print('.')
