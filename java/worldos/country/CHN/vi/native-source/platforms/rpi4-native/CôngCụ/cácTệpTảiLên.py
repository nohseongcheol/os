#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
vịTríDữLiệu=argparse.ArgumentParser(description=__doc__);vịTríDữLiệu.add_argument('file',type=Path);vịTríDữLiệu.add_argument('--name',help='guest file name (e.g. package.Class.class)');mảngĐốiSố=vịTríDữLiệu.parse_args()
DữLiệu=mảngĐốiSố.file.read_bytes();tên=mảngĐốiSố.name or mảngĐốiSố.file.name
if len(DữLiệu)>16384 or not 1<=len(tên.encode('utf-8'))<=63 or any(ord(mãKýTự)<32 for mãKýTự in tên):vịTríDữLiệu.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(tên))
for chỉSốThứBậc in range(0,len(DữLiệu),64):print(DữLiệu[chỉSốThứBậc:chỉSốThứBậc+64].hex())
print('.')
