#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ارزښتوړى_لړوند=자료위치.parse_args()
اومتوک=ارزښتوړى_لړوند.file.read_bytes();نوم=ارزښتوړى_لړوند.name or ارزښتوړى_لړوند.file.name
if len(اومتوک)>16384 or not 1<=len(نوم.encode('utf-8'))<=63 or any(ord(문자값)<32 for 문자값 in نوم):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(نوم))
for 순번 in range(0,len(اومتوک),64):print(اومتوک[순번:순번+64].hex())
print('.')
