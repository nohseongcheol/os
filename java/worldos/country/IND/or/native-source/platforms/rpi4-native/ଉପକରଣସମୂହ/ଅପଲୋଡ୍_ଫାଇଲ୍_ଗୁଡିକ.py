#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ଡାଟା_ସ୍ଥିତି=argparse.ArgumentParser(description=__doc__);ଡାଟା_ସ୍ଥିତି.add_argument('file',type=Path);ଡାଟା_ସ୍ଥିତି.add_argument('--name',help='guest file name (e.g. package.Class.class)');ଯୁକ୍ତି_ଆରେ=ଡାଟା_ସ୍ଥିତି.parse_args()
ଡାଟା=ଯୁକ୍ତି_ଆରେ.file.read_bytes();ନାମ=ଯୁକ୍ତି_ଆରେ.name or ଯୁକ୍ତି_ଆରେ.file.name
if len(ଡାଟା)>16384 or not 1<=len(ନାମ.encode('utf-8'))<=63 or any(ord(ବର୍ଣ୍ଣ_କୋଡ଼୍)<32 for ବର୍ଣ୍ଣ_କୋଡ଼୍ in ନାମ):ଡାଟା_ସ୍ଥିତି.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ନାମ))
for 순번 in range(0,len(ଡାଟା),64):print(ଡାଟା[순번:순번+64].hex())
print('.')
