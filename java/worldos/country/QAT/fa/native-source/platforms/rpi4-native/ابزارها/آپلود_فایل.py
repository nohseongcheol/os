#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
داده_ها_مرتب_کردن=argparse.ArgumentParser(description=__doc__);داده_ها_مرتب_کردن.add_argument('file',type=Path);داده_ها_مرتب_کردن.add_argument('--name',help='guest file name (e.g. package.Class.class)');آرگومان_آرايه=داده_ها_مرتب_کردن.parse_args()
داده_ها=آرگومان_آرايه.file.read_bytes();نام=آرگومان_آرايه.name or آرگومان_آرايه.file.name
if len(داده_ها)>16384 or not 1<=len(نام.encode('utf-8'))<=63 or any(ord(کد_نویسه)<32 for کد_نویسه in نام):داده_ها_مرتب_کردن.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(نام))
for 순번 in range(0,len(داده_ها),64):print(داده_ها[순번:순번+64].hex())
print('.')
