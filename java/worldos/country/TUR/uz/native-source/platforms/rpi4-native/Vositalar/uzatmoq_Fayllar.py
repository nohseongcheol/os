#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ma_lumotlar_holat=argparse.ArgumentParser(description=__doc__);ma_lumotlar_holat.add_argument('file',type=Path);ma_lumotlar_holat.add_argument('--name',help='guest file name (e.g. package.Class.class)');dalil_ARRAY=ma_lumotlar_holat.parse_args()
ma_lumotlar=dalil_ARRAY.file.read_bytes();Nomi=dalil_ARRAY.name or dalil_ARRAY.file.name
if len(ma_lumotlar)>16384 or not 1<=len(Nomi.encode('utf-8'))<=63 or any(ord(belgi_kodi)<32 for belgi_kodi in Nomi):ma_lumotlar_holat.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Nomi))
for 순번 in range(0,len(ma_lumotlar),64):print(ma_lumotlar[순번:순번+64].hex())
print('.')
