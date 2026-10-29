#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
データ位置=argparse.ArgumentParser(description=__doc__);データ位置.add_argument('file',type=Path);データ位置.add_argument('--name',help='guest file name (e.g. package.Class.class)');引数配列=データ位置.parse_args()
データ=引数配列.file.read_bytes();名前=引数配列.name or 引数配列.file.name
if len(データ)>16384 or not 1<=len(名前.encode('utf-8'))<=63 or any(ord(文字コード)<32 for 文字コード in 名前):データ位置.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(名前))
for 序数添字 in range(0,len(データ),64):print(データ[序数添字:序数添字+64].hex())
print('.')
