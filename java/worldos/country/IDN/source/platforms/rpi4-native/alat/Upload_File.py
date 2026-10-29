#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
data_posisi=argparse.ArgumentParser(description=__doc__);data_posisi.add_argument('file',type=Path);data_posisi.add_argument('--name',help='guest file name (e.g. package.Class.class)');argumen_ARRAY=data_posisi.parse_args()
data=argumen_ARRAY.file.read_bytes();Nama_2=argumen_ARRAY.name or argumen_ARRAY.file.name
if len(data)>16384 or not 1<=len(Nama_2.encode('utf-8'))<=63 or any(ord(kode_karakter)<32 for kode_karakter in Nama_2):data_posisi.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nama_2))
for 순번 in range(0,len(data),64):print(data[순번:순번+64].hex())
print('.')
