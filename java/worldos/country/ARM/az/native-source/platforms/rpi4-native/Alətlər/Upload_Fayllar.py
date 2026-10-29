#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
verilənlər_yerinə_qoymaq=argparse.ArgumentParser(description=__doc__);verilənlər_yerinə_qoymaq.add_argument('file',type=Path);verilənlər_yerinə_qoymaq.add_argument('--name',help='guest file name (e.g. package.Class.class)');arqument_ARRAY=verilənlər_yerinə_qoymaq.parse_args()
verilənlər=arqument_ARRAY.file.read_bytes();Ad=arqument_ARRAY.name or arqument_ARRAY.file.name
if len(verilənlər)>16384 or not 1<=len(Ad.encode('utf-8'))<=63 or any(ord(simvol_kodu)<32 for simvol_kodu in Ad):verilənlər_yerinə_qoymaq.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Ad))
for 순번 in range(0,len(verilənlər),64):print(verilənlər[순번:순번+64].hex())
print('.')
