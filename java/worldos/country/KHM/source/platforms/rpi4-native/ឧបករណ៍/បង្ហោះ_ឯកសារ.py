#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ទិន្នន័យ_កំណត់ទីតាំង=argparse.ArgumentParser(description=__doc__);ទិន្នន័យ_កំណត់ទីតាំង.add_argument('file',type=Path);ទិន្នន័យ_កំណត់ទីតាំង.add_argument('--name',help='guest file name (e.g. package.Class.class)');អាគុយម៉ង់_អារេ=ទិន្នន័យ_កំណត់ទីតាំង.parse_args()
ទិន្នន័យ=អាគុយម៉ង់_អារេ.file.read_bytes();ឈ្មោះ=អាគុយម៉ង់_អារេ.name or អាគុយម៉ង់_អារេ.file.name
if len(ទិន្នន័យ)>16384 or not 1<=len(ឈ្មោះ.encode('utf-8'))<=63 or any(ord(កូដនៃតួអក្សរ)<32 for កូដនៃតួអក្សរ in ឈ្មោះ):ទិន្នន័យ_កំណត់ទីតាំង.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ឈ្មោះ))
for 순번 in range(0,len(ទិន្នន័យ),64):print(ទិន្នន័យ[순번:순번+64].hex())
print('.')
