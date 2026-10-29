#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');විස්තාරකය_ආරා_ව=자료위치.parse_args()
දත්ත=විස්තාරකය_ආරා_ව.file.read_bytes();නම=විස්තාරකය_ආරා_ව.name or විස්තාරකය_ආරා_ව.file.name
if len(දත්ත)>16384 or not 1<=len(නම.encode('utf-8'))<=63 or any(ord(අනුලකුණු_කේතය)<32 for අනුලකුණු_කේතය in නම):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(නම))
for 순번 in range(0,len(දත්ත),64):print(දත්ත[순번:순번+64].hex())
print('.')
