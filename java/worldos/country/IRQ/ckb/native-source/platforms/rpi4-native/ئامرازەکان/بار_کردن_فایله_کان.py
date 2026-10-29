#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ئارگیومێنت_ڕیزی_داتا=자료위치.parse_args()
دەیتا=ئارگیومێنت_ڕیزی_داتا.file.read_bytes();ناو=ئارگیومێنت_ڕیزی_داتا.name or ئارگیومێنت_ڕیزی_داتا.file.name
if len(دەیتا)>16384 or not 1<=len(ناو.encode('utf-8'))<=63 or any(ord(کۆدی_نووسە)<32 for کۆدی_نووسە in ناو):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ناو))
for 순번 in range(0,len(دەیتا),64):print(دەیتا[순번:순번+64].hex())
print('.')
