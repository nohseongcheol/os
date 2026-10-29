#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ข้อมูล_ตําแหน่ง=argparse.ArgumentParser(description=__doc__);ข้อมูล_ตําแหน่ง.add_argument('file',type=Path);ข้อมูล_ตําแหน่ง.add_argument('--name',help='guest file name (e.g. package.Class.class)');อาร์กิวเมนต์_อาร์เรย์=ข้อมูล_ตําแหน่ง.parse_args()
ข้อมูล=อาร์กิวเมนต์_อาร์เรย์.file.read_bytes();ชื่อ=อาร์กิวเมนต์_อาร์เรย์.name or อาร์กิวเมนต์_อาร์เรย์.file.name
if len(ข้อมูล)>16384 or not 1<=len(ชื่อ.encode('utf-8'))<=63 or any(ord(รหัสอักขระ)<32 for รหัสอักขระ in ชื่อ):ข้อมูล_ตําแหน่ง.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ชื่อ))
for 순번 in range(0,len(ข้อมูล),64):print(ข้อมูล[순번:순번+64].hex())
print('.')
