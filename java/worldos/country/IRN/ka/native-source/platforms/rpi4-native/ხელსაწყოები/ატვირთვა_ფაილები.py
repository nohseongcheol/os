#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
მონაცემები_პოზიცია=argparse.ArgumentParser(description=__doc__);მონაცემები_პოზიცია.add_argument('file',type=Path);მონაცემები_პოზიცია.add_argument('--name',help='guest file name (e.g. package.Class.class)');არგუმენტი_მასივი=მონაცემები_პოზიცია.parse_args()
მონაცემები=არგუმენტი_მასივი.file.read_bytes();სახელი=არგუმენტი_მასივი.name or არგუმენტი_მასივი.file.name
if len(მონაცემები)>16384 or not 1<=len(სახელი.encode('utf-8'))<=63 or any(ord(სიმბოლოს_კოდი)<32 for სიმბოლოს_კოდი in სახელი):მონაცემები_პოზიცია.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(სახელი))
for 순번 in range(0,len(მონაცემები),64):print(მონაცემები[순번:순번+64].hex())
print('.')
