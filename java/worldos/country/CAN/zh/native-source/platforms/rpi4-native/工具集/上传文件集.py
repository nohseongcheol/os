#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
数据位置=argparse.ArgumentParser(description=__doc__);数据位置.add_argument('file',type=Path);数据位置.add_argument('--name',help='guest file name (e.g. package.Class.class)');参数数组=数据位置.parse_args()
数据=参数数组.file.read_bytes();名称=参数数组.name or 参数数组.file.name
if len(数据)>16384 or not 1<=len(名称.encode('utf-8'))<=63 or any(ord(字符代码)<32 for 字符代码 in 名称):数据位置.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(名称))
for 序数索引 in range(0,len(数据),64):print(数据[序数索引:序数索引+64].hex())
print('.')
