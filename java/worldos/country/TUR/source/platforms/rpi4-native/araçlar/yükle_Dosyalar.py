#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
veri_konum=argparse.ArgumentParser(description=__doc__);veri_konum.add_argument('file',type=Path);veri_konum.add_argument('--name',help='guest file name (e.g. package.Class.class)');bağımsız_değişken_DİZİ=veri_konum.parse_args()
veri=bağımsız_değişken_DİZİ.file.read_bytes();İsim=bağımsız_değişken_DİZİ.name or bağımsız_değişken_DİZİ.file.name
if len(veri)>16384 or not 1<=len(İsim.encode('utf-8'))<=63 or any(ord(kod_noktası)<32 for kod_noktası in İsim):veri_konum.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(İsim))
for 순번 in range(0,len(veri),64):print(veri[순번:순번+64].hex())
print('.')
