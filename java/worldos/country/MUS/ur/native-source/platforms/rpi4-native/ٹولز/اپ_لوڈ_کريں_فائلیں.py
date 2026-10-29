#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
کوائف_پوزیشن_ٹھیک_کریں=argparse.ArgumentParser(description=__doc__);کوائف_پوزیشن_ٹھیک_کریں.add_argument('file',type=Path);کوائف_پوزیشن_ٹھیک_کریں.add_argument('--name',help='guest file name (e.g. package.Class.class)');دلائل_لڑی=کوائف_پوزیشن_ٹھیک_کریں.parse_args()
کوائف=دلائل_لڑی.file.read_bytes();نام=دلائل_لڑی.name or دلائل_لڑی.file.name
if len(کوائف)>16384 or not 1<=len(نام.encode('utf-8'))<=63 or any(ord(کریکٹر_ضابطہ)<32 for کریکٹر_ضابطہ in نام):کوائف_پوزیشن_ٹھیک_کریں.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(نام))
for 순번 in range(0,len(کوائف),64):print(کوائف[순번:순번+64].hex())
print('.')
