#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ágúmẹ́ntì_ÀRÉÈ=자료위치.parse_args()
détà=ágúmẹ́ntì_ÀRÉÈ.file.read_bytes();Orúkọ=ágúmẹ́ntì_ÀRÉÈ.name or ágúmẹ́ntì_ÀRÉÈ.file.name
if len(détà)>16384 or not 1<=len(Orúkọ.encode('utf-8'))<=63 or any(ord(kóòdù_ẹyọ_ọ̀rọ̀)<32 for kóòdù_ẹyọ_ọ̀rọ̀ in Orúkọ):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Orúkọ))
for 순번 in range(0,len(détà),64):print(détà[순번:순번+64].hex())
print('.')
