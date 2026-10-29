#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
資料位置=argparse.ArgumentParser(description=__doc__);資料位置.add_argument('file',type=Path);資料位置.add_argument('--name',help='guest file name (e.g. package.Class.class)');實際參數陣列=資料位置.parse_args()
資料=實際參數陣列.file.read_bytes();名稱=實際參數陣列.name or 實際參數陣列.file.name
if len(資料)>16384 or not 1<=len(名稱.encode('utf-8'))<=63 or any(ord(字元程式碼)<32 for 字元程式碼 in 名稱):資料位置.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(名稱))
for 序數索引 in range(0,len(資料),64):print(資料[序數索引:序數索引+64].hex())
print('.')
