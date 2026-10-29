#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ডাটা_পদ=argparse.ArgumentParser(description=__doc__);ডাটা_পদ.add_argument('file',type=Path);ডাটা_পদ.add_argument('--name',help='guest file name (e.g. package.Class.class)');যুক্তি_অ্যারে=ডাটা_পদ.parse_args()
ডাটা=যুক্তি_অ্যারে.file.read_bytes();নাম=যুক্তি_অ্যারে.name or যুক্তি_অ্যারে.file.name
if len(ডাটা)>16384 or not 1<=len(নাম.encode('utf-8'))<=63 or any(ord(অক্ষর_কোড)<32 for অক্ষর_কোড in নাম):ডাটা_পদ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(নাম))
for 순번 in range(0,len(ডাটা),64):print(ডাটা[순번:순번+64].hex())
print('.')
